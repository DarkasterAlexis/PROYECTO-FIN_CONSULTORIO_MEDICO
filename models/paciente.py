from database import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    paciente_id = db.Column(db.Integer,primary_key=True)
    ci = db.Column(db.String(20),unique=True,nullable=False)
    nombres = db.Column(db.String(100),nullable=False)
    apellidos = db.Column(db.String(100),nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    correo = db.Column(db.String(100))
    estado = db.Column(db.Boolean,default=True)