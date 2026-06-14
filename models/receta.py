from database import db
from datetime import datetime


class Receta(db.Model):
    __tablename__ = 'receta'
    RecetaID = db.Column(db.Integer,primary_key=True)
    HistorialID = db.Column(db.Integer,db.ForeignKey('historial_clinico.HistorialID'),nullable=False)
    paciente_id = db.Column(db.Integer,db.ForeignKey('paciente.paciente_id'),nullable=False)
    CodMedico = db.Column(db.Integer,db.ForeignKey('medico.CodMedico'),nullable=False)
    Fecha = db.Column(db.DateTime,default=datetime.utcnow)
    Observaciones = db.Column(db.Text)
    Estado = db.Column(db.String(20),default='Activo')
    historial = db.relationship('HistorialClinico')
    paciente = db.relationship('Paciente')
    medico = db.relationship('Medico')
    detalles = db.relationship('DetalleReceta',cascade="all, delete")