from database import db

class Rol(db.Model):
    __tablename__ = 'rol'
    rol_id = db.Column(db.Integer,primary_key=True)
    nombre_rol = db.Column(db.String(50),unique=True,nullable=False)
    def __repr__(self):
        return self.nombre_rol