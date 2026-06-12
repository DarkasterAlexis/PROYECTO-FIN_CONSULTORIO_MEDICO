from database import db

class Medico(db.Model):
    __tablename__ = 'medico'
    CodMedico = db.Column(db.Integer, primary_key=True)
    Especialidad = db.Column(db.String(100),nullable=False)
    MatriculaProfesional = db.Column(db.String(50),unique=True,nullable=False)
    Estado = db.Column(db.String(20),default='Activo')
    CodPersonal = db.Column(db.Integer,db.ForeignKey('personal.CodPersonal'),nullable=False)
    personal = db.relationship('Personal')