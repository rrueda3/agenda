from flask import Blueprint, render_template, request, url_for, flash, redirect
from .forms import AdminPasswordForm, AdminFillForm
from .models import Usuario, db, Agenda
from werkzeug.security import generate_password_hash
from datetime import date, timedelta, datetime


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    form_password = AdminPasswordForm()
    form_fill = AdminFillForm()
    if form_password.validate_on_submit():
        user = request.form['usuario']
        pw = request.form['password']
        Usuario.query.filter_by(username=user).first().password = generate_password_hash(pw)
        db.session.commit()
        flash('Se ha reestablecido la contraseña', 'success')
        return redirect(url_for('main.index'))
    if form_fill.validate_on_submit():
        ultima_pagina = Agenda.query.all()[-1]
        fecha_inicial = ultima_pagina.fecha + timedelta(days=1)
        comision = int(ultima_pagina.comision) + 1
        if comision == 8:
            comision = 1
        fecha_final = datetime.strptime(request.form['fecha_final'], '%Y-%m-%d')
        if fecha_final.date() <= ultima_pagina.fecha:
            flash('La fecha final debe ser posterior a ' + datetime.strftime(ultima_pagina.fecha, '%d-%m-%Y'))
            return redirect(url_for('admin.admin'))
        if fecha_final.date() > ultima_pagina.fecha + timedelta(days=365):
            flash('Sólo se permite rellenar hasta un máximo de un año desde la última página rellena ('
                  + datetime.strftime(ultima_pagina.fecha, '%d-%m-%Y') + ')', 'error')
            return redirect(url_for('admin.admin'))
        while fecha_inicial <= fecha_final.date():
            if fecha_inicial.isoweekday() > 5:
                fecha_inicial += timedelta(days=2)
            for i in range(4):
                nueva = Agenda(comision=str(comision), fecha=fecha_inicial)
                db.session.add(nueva)
                db.session.commit()
                comision += 1
                if comision == 8:
                    comision = 1
            fecha_inicial += timedelta(days=1)
        flash('La agenda se ha rellenado hasta el día ' + datetime.strftime(fecha_final, '%d-%m-%Y'), 'success')
        return redirect(url_for('main.index'))
        
    return render_template('admin.html', form_password=form_password, form_fill=form_fill)
