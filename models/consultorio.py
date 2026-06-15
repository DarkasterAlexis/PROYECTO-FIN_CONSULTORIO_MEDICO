from database import db

class Consultorio(db.Model):
    __tablename__ = 'consultorio'
    consultorio_id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))