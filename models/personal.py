from database import db

class Personal(db.Model):
    __tablename__ = 'personal'
    CodPersonal = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Apellidos = db.Column(db.String(100), nullable=False)
    Telefono = db.Column(db.String(20))
    Estado = db.Column(db.String(20), default='Activo')