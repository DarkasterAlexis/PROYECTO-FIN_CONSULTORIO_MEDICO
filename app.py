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
from models.cita import Cita

#importar controladores
from controllers.personal_controller import personal_bp
from controllers.medico_controller import medico_bp
from controllers.login_controller import login_bp
from controllers.paciente_controller import paciente_bp

#blueprints
app.register_blueprint(personal_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(login_bp)
app.register_blueprint(paciente_bp)

with app.app_context():
    db.create_all()
    if Rol.query.count() == 0:
        rol1 = Rol(nombre_rol='Administrador')
        rol2 = Rol(nombre_rol='Recepcionista')
        rol3 = Rol(nombre_rol='Medico')
        db.session.add(rol1)
        db.session.add(rol2)
        db.session.add(rol3)
        db.session.commit()

@app.route('/')
def inicio():
    return render_template('principal/index.html')

@app.route('/registro')
def registro():
    return render_template('principal/registro_inicio.html')

@app.route('/login')
def login():
    return render_template('auth/login.html')

if __name__ == '__main__':
    app.run(debug=True)