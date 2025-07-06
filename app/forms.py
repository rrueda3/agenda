from flask_wtf import FlaskForm
from wtforms import DateField,  StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
class ApunteForm(FlaskForm):
    dia = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    comision = SelectField('Comisión', validators=[DataRequired()], choices=['comisión',1,2,3,4,5,6,7])
    juzgado = SelectField('Juzgado' ,validators=[DataRequired()], 
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
    procedimiento = StringField('Procedimiento', validators=[DataRequired()])
    submit = SubmitField('Anotar')


class ComprobarForm(FlaskForm):
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Comprobar')

class BorrarForm(FlaskForm):
    fecha = DateField('Fecha señalada', validators=[DataRequired()])
    procedimiento = StringField('Procedimiento', validators=[DataRequired()])
    submit = SubmitField('Borrar señalamiento')

class MostrarApuntesForm(FlaskForm):
    inicial = DateField('Desde', validators=[DataRequired()])
    final = DateField('Hasta', validators=[DataRequired()])
    comision = StringField('Mostrar por comisión', render_kw={"placeholder": "Indicar número de comisión"})
    submit = SubmitField('Mostrar')

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Contraseña', validators=[DataRequired(),Length(min=8)])
    repetir_password = PasswordField('Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField('Registro')


class ProfileForm(FlaskForm):
    username = StringField('Nombre de usuario')
    password = PasswordField('Contraseña')
    submit = SubmitField('Cambiar contraseña')


class PasswordForm(FlaskForm):
    actual = StringField('Contraseña actual', validators=[DataRequired()])
    nueva = PasswordField('Nueva contraseña', validators=[DataRequired()])
    repetir = PasswordField('Repita contraseña', validators=[EqualTo('nueva', 'Las contraseñas no coinciden')])
    submit = SubmitField('Cambiar contraseña')

class PageForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired()])
    submit = SubmitField('Mostrar')

class AdminPasswordForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    re_password = PasswordField('Repetir contraseña', validators=[EqualTo('password', 'Las contraseñas no coinciden')])
    submit = SubmitField('Recuperar contraseña')

class AdminFillForm(FlaskForm):
    fecha_final = DateField('Rellenar agenda hasta', validators=[DataRequired()])
    submit = SubmitField('Rellenar')

class DeletePageForm(FlaskForm):
    submit = SubmitField('Borrar páginas pasadas')
