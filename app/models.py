from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()


class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comision = db.Column(db.String, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    

class Apuntes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.Date, nullable=False)
    comision = db.Column(db.String, nullable=False)
    juzgado = db.Column(db.String, nullable=False) 
    representante = db.Column(db.String)
    procedimiento = db.Column(db.String, nullable=False)


class Turno(db.Model):
    __tablename__ ='turno_comision'
    id = db.Column(db.Integer, primary_key=True)
    turno = db.Column(db.String, nullable=False)
    salta_turno = db.Column(db.String)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='user')