from database import db

class DetalleReceta(db.Model):
    __tablename__ = 'detalle_receta'
    DetalleID = db.Column(db.Integer,primary_key=True)
    RecetaID = db.Column(db.Integer,db.ForeignKey('receta.RecetaID'),nullable=False)
    Medicamento = db.Column(db.String(100),nullable=False)
    Dosis = db.Column(db.String(100))
    Frecuencia = db.Column(db.String(100))
    Duracion = db.Column(db.String(100))
    Indicaciones = db.Column(db.Text)
    receta = db.relationship('Receta')