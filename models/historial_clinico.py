from database import db
from datetime import datetime

class HistorialClinico(db.Model):
    __tablename__ = 'historial_clinico'
    HistorialID = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer,db.ForeignKey('paciente.paciente_id'),nullable=False)
    CodMedico = db.Column(db.Integer,db.ForeignKey('medico.CodMedico'),nullable=False)
    CodCita = db.Column(db.Integer,db.ForeignKey('cita.CodCita'),nullable=False,unique=True)
    FechaAtencion = db.Column(db.DateTime,default=datetime.utcnow)
    MotivoConsulta = db.Column(db.Text,nullable=False)
    Diagnostico = db.Column(db.Text,nullable=False)
    Tratamiento = db.Column(db.Text,nullable=False)
    Observaciones = db.Column(db.Text)
    paciente = db.relationship('Paciente')
    medico = db.relationship('Medico')
    cita = db.relationship('Cita')