from flask import Blueprint, render_template, request, url_for, flash, redirect
from .forms import LoginForm, RegisterForm, ProfileForm, PasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, db
from flask_login import  login_user, login_required, current_user, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and  check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Nombre de usuario o contraseña incorrecto', 'error')
    
    return render_template('login.html', form=form)

def admin_required(f):
    def wrapper(*args, **kwargs):

        if current_user.role != 'admin':
            flash('Sólo el administrador puede acceder al Registro', 'warning')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
        
    return wrapper


@auth_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@admin_required
def registro():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['repetir_password']
        if password == re_password:
            nuevo_usuario = Usuario(username=username, password=generate_password_hash(password))
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('Las contraseñas no coinciden', 'error')
    return render_template('registro.html', form=form)
    

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    form = ProfileForm()
    if form.validate_on_submit():
        return redirect(url_for('auth.cambiar_password'))
    return render_template('perfil.html', form=form, name=current_user.username)


@auth_bp.route('/cambiar_password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = PasswordForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=current_user.username).first()
        actual = request.form['actual']
        if check_password_hash(usuario.password, actual):
            usuario.password = generate_password_hash(request.form['nueva'])
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('La contraseña actual no es correcta', 'error')
    return render_template('cambiar_password.html', form=form)