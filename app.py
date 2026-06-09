from flask import Flask
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'consultorio_aranda'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultorio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# importar modelos DESPUÉS
from models.rol import Rol
from models.usuario import Usuario
from models.paciente import Paciente

with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return "Sistema Consultorio Médico ARANDA"

if __name__ == '__main__':
    app.run(debug=True)