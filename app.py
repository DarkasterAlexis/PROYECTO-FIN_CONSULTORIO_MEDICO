from flask import Flask, render_template
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
from models.medico import Medico
from models.personal import Personal

#importar controladores
from controllers.personal_controller import personal_bp
from controllers.medico_controller import medico_bp

#blueprints
app.register_blueprint(personal_bp)
app.register_blueprint(medico_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro_inicio.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)