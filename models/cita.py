from database import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = 'cita'
    CodCita = db.Column(db.Integer, primary_key=True)
    CodPaciente = db.Column(db.Integer,db.ForeignKey('paciente.paciente_id'),nullable=False)
    CodMedico = db.Column(db.Integer,db.ForeignKey('medico.CodMedico'),nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    Hora = db.Column(db.Time, nullable=False)
    Motivo = db.Column(db.String(255))
    Estado = db.Column(db.String(20),nullable=False,default='Confirmada')
    Origen = db.Column(db.String(20),nullable=False,default='Recepcion')
    FechaRegistro = db.Column(db.DateTime,default=datetime.utcnow)
    paciente = db.relationship('Paciente')
    medico = db.relationship('Medico')