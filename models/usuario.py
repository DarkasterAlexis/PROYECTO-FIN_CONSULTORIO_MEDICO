from database import db
from models.rol import Rol
from models.personal import Personal

class Usuario(db.Model):
    __tablename__ = 'usuario'
    usuario_id = db.Column(db.Integer,primary_key=True)
    nombre_usuario = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    estado = db.Column(db.Boolean,default=True)
    rol_id = db.Column(db.Integer,db.ForeignKey('rol.rol_id'))
    CodPersonal = db.Column(db.Integer,db.ForeignKey('personal.CodPersonal'),nullable=False)
    rol = db.relationship('Rol')
    personal = db.relationship('Personal')