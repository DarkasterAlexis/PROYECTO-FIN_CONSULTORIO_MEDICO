from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from models.usuario import Usuario
from models.consultorio import Consultorio
from models.parametro import Parametro

config_bp = Blueprint('config',__name__)

@config_bp.route('/configuracion')
def configuracion():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    return render_template('configuracion/configuracion.html')

@config_bp.route('/configuracion/usuarios')
def usuarios_config():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    usuarios = Usuario.query.all()
    return render_template('configuracion/usuarios.html',usuarios=usuarios)

@config_bp.route('/configuracion/usuario_estado/<int:id>')
def cambiar_estado_usuario(id):
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    usuario = Usuario.query.get_or_404(id)
    usuario.estado = not usuario.estado
    db.session.commit()
    return redirect(url_for('config.usuarios_config'))

@config_bp.route('/configuracion/consultorio', methods=['GET','POST'])
def consultorio_config():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    consultorio = Consultorio.query.first()
    if request.method == 'POST':
        if consultorio:
            consultorio.nombre = request.form['nombre']
            consultorio.direccion = request.form['direccion']
            consultorio.telefono = request.form['telefono']
            consultorio.correo = request.form['correo']
        else:
            consultorio = Consultorio(
                nombre=request.form['nombre'],
                direccion=request.form['direccion'],
                telefono=request.form['telefono'],
                correo=request.form['correo']
            )
            db.session.add(consultorio)

        db.session.commit()
        return redirect(url_for('config.configuracion'))

    return render_template('configuracion/consultorio.html',consultorio=consultorio)

@config_bp.route('/configuracion/parametros')
def parametros_config():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    parametros = Parametro.query.all()
    return render_template('configuracion/parametros.html',parametros=parametros)