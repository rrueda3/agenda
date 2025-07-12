from flask import Blueprint, make_response, render_template, request, flash, url_for, redirect
from .forms import ApunteForm, PageForm, ComprobarForm, BorrarForm, MostrarApuntesForm, ModificarForm
from .models import db, Apuntes, Agenda, Turno
from datetime import datetime, timedelta
from fpdf import FPDF
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def conectar():
    return redirect(url_for('auth.login'))

@main_bp.route('/index')
@login_required
def index():
    return render_template('index.html')


# Apuntar lanzamiento y comprobar días disponibles para la comisión

@main_bp.route('/apunte', methods=['GET', 'POST'])
@login_required
def apunte ():
    form = ApunteForm()
    subform = ComprobarForm()
    turno = Turno.query.get(1).turno

    # Comprobar fechas para la comisión de turno

    if subform.validate_on_submit():
        data = request.form['fecha']
        turno = Turno.query.get(1).turno
        inicial = (datetime.strptime(data, '%Y-%m-%d')).date() - timedelta(days=5)
        final = (datetime.strptime(data, '%Y-%m-%d')).date() + timedelta(days=5)
        disponibilidades =Agenda.query.filter(Agenda.fecha >= inicial,
                            Agenda.fecha <= final, Agenda.comision==turno, Agenda.disponible==True).all()
        fechas_disponibles = []
        for disponible in disponibilidades:
            if disponible.fecha.isoweekday() == 5:
                continue
            fechas_disponibles.append(datetime.strftime(disponible.fecha, '%d-%m-%Y'))
        
        representantes = []
        for fecha in fechas_disponibles:
            reps = Apuntes.query.filter_by(dia=datetime.strptime(fecha, '%d-%m-%Y')).all()
            for rep in reps:
                representantes.append((rep.representante, datetime.strftime(rep.dia, '%d-%m-%Y')))

        flash('Fechas disponibles para la comisión '
              + turno + ':' + ' ' + str(fechas_disponibles), 'info')
        if len(representantes) > 0:
            flash('Atención, los siguientes representantes tienen señalamientos en los días que se indican ' + str(representantes), 'warning')
        if datetime.strptime(data, '%Y-%m-%d').isoweekday() == 5:
            flash('Atención, este día es VIERNES', 'warning')

    # Apuntar lanzamiento

    if form.validate_on_submit():
        fecha = request.form['dia']
        comision = request.form['comision']
        juzgado = request.form['juzgado']
        representante = request.form['representante'].title()
        procedimiento = request.form['procedimiento']
        comisiones = Agenda.query.filter_by(fecha=fecha).all()
        disponibles = []
        for com in comisiones:
             if com.disponible:
                  disponibles.append(com.comision)
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
        
        if comision in disponibles:
            apuntado = Apuntes(dia=fecha, comision=comision, juzgado=juzgado, representante=representante, procedimiento= procedimiento)
            no_disponible = Agenda.query.filter(Agenda.comision==comision, Agenda.fecha==datetime.strftime(fecha, '%Y-%m-%d')).first()
            no_disponible.disponible = False
            
            if comision != Turno.query.get(1).turno:
                Turno.query.get(1).salta_turno += (comision + ' ')
            else:
                t = int(Turno.query.get(1).turno) + 1
                if t == 8:
                    t = 1
                array_saltos = Turno.query.get(1).salta_turno.strip().split()
                while str(t) in array_saltos:
                    t += 1
                    array_saltos.remove(str(t-1))
                saltos = ' '.join(array_saltos) + ' '
                Turno.query.get(1).turno = str(t)
                Turno.query.get(1).salta_turno = saltos
                db.session.commit()
            db.session.add(apuntado)
            db.session.commit()
            flash('Se ha apuntado el lanzamiento', 'success')
            return redirect(url_for('main.apunte'))
        else:
            flash('La comisión elegida no está disponible para ese día', 'error')

    return render_template('apunte.html', form=form, subform=subform, turno=turno)


# Modificar un señalamiento

@main_bp.route('/modificar', methods=['GET', 'POST'])
def modificar():
    form = ModificarForm()
    if form.validate_on_submit():
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        comision = request.form['comision']
        proc = form.bool_proc.data
        juzg = form.bool_juzg.data
        repr = form.bool_repr.data
        apunte = Apuntes.query.filter(Apuntes.dia==fecha, Apuntes.comision==comision).first()
        if proc:
            procedimiento = request.form['procedimiento']
            apunte.procedimiento = procedimiento
        if juzg:
            juzgado = request.form['juzgado']
            if juzgado != 'juzgado':
                apunte.juzgado = juzgado
        if repr:
            representante = request.form['representante']
            if representante:
                apunte.representante = representante
        db.session.commit()
        flash('Se han realizado las modificaciones indicadas', 'success')
        return redirect(url_for('main.index'))
    return render_template('modificar.html', form=form)


# Borrar señalamiento de la agenda

@main_bp.route('/borrar', methods=['GET', 'POST'])
@login_required
def borrar():
    form = BorrarForm()
    if form.validate_on_submit():
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        procedimiento = request.form['procedimiento']
        apunte = Apuntes.query.where(Apuntes.dia==datetime.strftime(fecha, '%Y-%m-%d'),
                                     Apuntes.procedimiento==procedimiento).first()
        if apunte:
            flash('Juzgado: ' + apunte.juzgado + ' ------ Comision: ' + apunte.comision, 'info')
            Agenda.query.where(Agenda.fecha==datetime.strftime(fecha, '%Y-%m-%d'), 
                            Agenda.comision==apunte.comision).first().disponible=True
            db.session.delete(apunte)
            db.session.commit()
            flash('Se ha borrado el señalamiento', 'success')
            return redirect(url_for('main.apunte'))
        else:
            flash('No hay ningún señalamiento para ese día con los datos introducidos', 'error')
        
    return render_template('borrar.html', form=form)


# Mostrar todos los señalamientos de fecha a fecha

@main_bp.route('/mostrar_apuntes', methods=['GET','POST'])
@login_required
def mostrar_apuntes():
    form = MostrarApuntesForm()
    if form.validate_on_submit():
        inicial = datetime.strptime(request.form['inicial'], '%Y-%m-%d')
        final = datetime.strptime(request.form['final'], '%Y-%m-%d')
        comision_filtrada = request.form['comision']
        apuntes = Apuntes.query.filter(Apuntes.dia >= datetime.strftime(inicial, '%Y-%m-%d'), Apuntes.dia <= datetime.strftime(final, '%Y-%m-%d')).order_by(Apuntes.dia).all()
        if not apuntes:
            flash('En esas fechas no figuran señalamientos', 'warning')
        else:
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Times', 'BU', 14)
            pdf.ln(10)
            if comision_filtrada:
                pdf.cell(190, 10, 'Lanzamientos señalados por comisión', 0, 1, 'C')
            else:
                pdf.cell(190, 10, 'Lanzamientos señalados por fechas', 0, 1, 'C')

            pdf.set_line_width(0.1)
            pdf.ln(10)
            pdf.set_font('Arial', '', 14)
            pdf.cell(10)
            pdf.cell(10, 10, 'Del ', 0, 0)
            pdf.cell(25, 10, datetime.strftime(inicial, '%d-%m-%Y'), 0, 0)
            pdf.cell(7, 10, ' al', 0, 0)
            pdf.cell(25, 10, datetime.strftime(final, '%d-%m-%Y'), 0, 0)
            if comision_filtrada:
                pdf.cell(70, 10, ' para la comisión ' + comision_filtrada, 0, 0)
            pdf.ln(15)
            pdf.cell(10)
            pdf.cell(30, 10, 'Fecha', 1, 0, 'C')
            if  not comision_filtrada:
                pdf.cell(30, 10, 'Comisión', 1, 0, 'C')
            pdf.cell(40, 10, 'Juzgado', 1, 0, 'C')
            pdf.cell(40, 10, 'Procedimiento', 1, 0, 'C')
            pdf.cell(40, 10, 'Representante', 1, 1, 'C')
            pdf.set_font('Arial', '', 12)
            for apunte in apuntes:
                if comision_filtrada:
                    if apunte.comision == comision_filtrada:
                        pdf.cell(10)
                        pdf.cell(30, 10, datetime.strftime(apunte.dia, '%d-%m-%Y'), 0, 0, 'C')
                        pdf.cell(40, 10, apunte.juzgado, 0, 0, 'C')
                        pdf.cell(40, 10, apunte.procedimiento, 0, 0, 'C')
                        pdf.cell(40, 10, apunte.representante, 0, 1, 'C')
                        pdf.line(20, pdf.get_y(), 170, pdf.get_y())
                else:
                        pdf.cell(10)        
                        pdf.cell(30, 10, datetime.strftime(apunte.dia, '%d-%m-%Y'), 0, 0, 'C')
                        pdf.cell(30, 10, apunte.comision, 0, 0, 'C')
                        pdf.cell(40, 10, apunte.juzgado, 0, 0, 'C')
                        pdf.cell(40, 10, apunte.procedimiento, 0, 0, 'C')
                        pdf.cell(40, 10, apunte.representante, 0, 1, 'C')
                        pdf.line(20, pdf.get_y(), 200, pdf.get_y())
                
            output = pdf.output('respaldo.pdf', dest='S').encode('latin-1')
            response = make_response(output)
            response.headers.set('Content-Type', 'application/pdf')
            response.headers.set('Content-Disposition', 'inline; filename=doc.pdf')
            return response

    return render_template('mostrar_apuntes.html', form=form)

# Mostrar una página de la agenda

@main_bp.route('/pagina', methods=['GET', 'POST'])
@login_required
def pagina():
    form = PageForm()
    ultima = db.session.query(Agenda).order_by(Agenda.fecha.desc()).first().fecha
    if form.validate_on_submit():
        date = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        pagina = Agenda.query.filter_by(fecha=date.date()).all()
        if len(pagina) == 0:
            flash('La página de esa fecha no está rellena', 'warning')
            return redirect(url_for('main.pagina'))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'BU', 14)
        pdf.ln(10)
        pdf.cell(190, 10, 'Página de la Agenda del día ' + datetime.strftime(date, '%d-%m-%Y'), 0, 1, 'C')
        pdf.ln(20)
        pdf.cell(20)
        pdf.set_font('Arial', '', 12)
        pdf.cell(30, 10, 'Comisión', 1, 0, 'C')
        pdf.cell(40, 10, 'Juzgado', 1, 0, 'C')
        pdf.cell(40, 10, 'Procedimiento', 1, 0, 'C')
        pdf.cell(40, 10, 'Representante', 1, 1, 'C')
      
        apuntes = Apuntes.query.filter(Apuntes.dia==datetime.strftime(date, '%Y-%m-%d')).all()
        comisiones = Agenda.query.filter(Agenda.fecha==datetime.strftime(date, '%Y-%m-%d')).order_by('id').all()
        
        com_dia = []
        i = 0
        for apunte in apuntes:
            com_dia.append(apunte.comision)
        for comision in comisiones:
            pdf.cell(20) 
            if  len(apuntes) > i and comision.comision in com_dia:
                pdf.cell(30, 10, comision.comision, 0, 0, 'C')
                pdf.cell(40, 10, apuntes[com_dia.index(comision.comision)].juzgado, 0, 0, 'C')
                pdf.cell(40, 10, apuntes[com_dia.index(comision.comision)].procedimiento, 0, 0, 'C')
                pdf.cell(40, 10, apuntes[com_dia.index(comision.comision)].representante, 0, 1, 'C')
                i += 1
            else:
                pdf.cell(30, 10, comision.comision, 0, 1, 'C')
                  
            pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(10)
        pdf.cell(20)
        permanencia = str(int(comisiones[3].comision) + 1)
        if permanencia == '8':
            permanencia = '1'
        pdf.cell(50, 10, 'Permanencia ' + permanencia)
        output = pdf.output(dest='S').encode('latin-1')
        response = make_response(output)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'inline; filename=doc.pdf')
        return response
    return render_template('hoja.html',form=form, ultima=ultima)






