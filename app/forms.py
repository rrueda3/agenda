from flask_wtf import FlaskForm
from wtforms import DateField,  StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo,Regexp, Optional, ValidationError
from datetime import date, datetime


def lt_actual_year(form, field):
    year = int(field.data.split('/')[1])
    if  year > date.today().year:
        raise ValidationError('No es posible que el año del procedimiento sea posterior al actual')
    
def interval_error(form, field):
    if field.data < form.inicial.data:
        raise ValidationError('El intervalo de fechas no es correcto')


class ApunteForm(FlaskForm):
    dia = DateField('Fecha', format='%Y-%m-%d', validators=[InputRequired(message='Campo obligatorio')])
    comision = SelectField('Comisión', validators=[InputRequired(message='Campo obligatorio')], choices=['comisión',1,2,3,4,5,6,7])
    juzgado = SelectField('Juzgado' ,validators=[InputRequired(message='Campo obligatorio')], 
                          choices=['juzgado',
                                   'Primera Instancia 1',
                                   'Primera Instancia 2',
                                   'Primera Instancia 3',
                                   'Primera Instancia 4',
                                   'Primera Instancia 5',
                                   'Primera Instancia 6',
                                   'Instrucción 1',
                                   'Instrucción 2',
                                   'Instrucción 3',
                                   'Instrucción 4',
                                   'Mercantil 1',
                                   'Mercantil 2'
                                   ]
                          )
    representante = StringField('Representante')
    procedimiento = StringField('Procedimiento', validators=[InputRequired(message='Campo obligatorio'), Regexp('^[1-9]{1}\d+/2\d{3}$',
                                                            message='El formato debe ser nº/año(4 dígitos)'), lt_actual_year])
    submit = SubmitField('Anotar')


class ComprobarForm(FlaskForm):
    fecha = DateField('Fecha', validators=[InputRequired(message='Campo obligatorio')])
    submit = SubmitField('Comprobar')


class ModificarForm(FlaskForm):
    fecha = DateField('Fecha del señalamiento', validators=[InputRequired()])
    comision = SelectField('¿Qué comisión?', validators=[InputRequired()], choices=['comision', '1', '2', '3', '4', '5', '6', '7'])
    bool_proc = BooleanField('Procedimiento', default=False)
    bool_juzg = BooleanField('Juzgado', default=False)
    bool_repr = BooleanField('Representante', default=False)
    procedimiento = StringField('Procedimiento', validators=[Optional(), Regexp('^[1-9]{1}\d+/2\d{3}$',
                                                            message='El formato debe ser nº/año(4 dígitos)')])
    juzgado = SelectField('Juzgado',choices=['juzgado',
                                   'Primera Instancia 1',
                                   'Primera Instancia 2',
                                   'Primera Instancia 3',
                                   'Primera Instancia 4',
                                   'Primera Instancia 5',
                                   'Primera Instancia 6',
                                   'Instrucción 1',
                                   'Instrucción 2',
                                   'Instrucción 3',
                                   'Instrucción 4',
                                   'Mercantil 1',
                                   'Mercantil 2'
                                   ])
    representante = StringField('Representante')
    submit = SubmitField('Modificar')


class BorrarForm(FlaskForm):
    fecha = DateField('Fecha señalada', validators=[InputRequired()])
    procedimiento = StringField('Procedimiento', validators=[InputRequired()])
    submit = SubmitField('Borrar señalamiento')

class MostrarApuntesForm(FlaskForm):
    inicial = DateField('Desde', validators=[InputRequired()])
    final = DateField('Hasta', validators=[InputRequired(), interval_error])
    comision = StringField('Mostrar por comisión', render_kw={"placeholder": "Indicar número"})
    submit = SubmitField('Mostrar')

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Contraseña', validators=[InputRequired(),Length(min=8)])
    repetir_password = PasswordField('Repetir contraseña', validators=[InputRequired()])
    role_admin = BooleanField('Rol_admin?')
    submit = SubmitField('Registro')


class ProfileForm(FlaskForm):
    username = StringField('Nombre de usuario')
    password = PasswordField('Contraseña')
    submit = SubmitField('Cambiar contraseña')


class PasswordForm(FlaskForm):
    actual = StringField('Contraseña actual', validators=[InputRequired()])
    nueva = PasswordField('Nueva contraseña', validators=[InputRequired()])
    repetir = PasswordField('Repita contraseña', validators=[EqualTo('nueva', 'Las contraseñas no coinciden')])
    submit = SubmitField('Cambiar contraseña')

class PageForm(FlaskForm):
    fecha = DateField('Fecha', validators=[InputRequired()])
    submit = SubmitField('Mostrar')

class AdminPasswordForm(FlaskForm):
    usuario = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])
    re_password = PasswordField('Repetir contraseña', validators=[EqualTo('password', 'Las contraseñas no coinciden')])
    submit = SubmitField('Recuperar contraseña')

class AdminFillForm(FlaskForm):
    fecha_final = DateField('Rellenar agenda hasta', validators=[InputRequired()])
    submit = SubmitField('Rellenar')

class DeletePageForm(FlaskForm):
    submit = SubmitField('Borrar páginas pasadas')
