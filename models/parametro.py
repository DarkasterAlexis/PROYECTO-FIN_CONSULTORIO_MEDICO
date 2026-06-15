from database import db

class Parametro(db.Model):
    __tablename__ = 'parametro'
    parametro_id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    valor = db.Column(db.String(255))