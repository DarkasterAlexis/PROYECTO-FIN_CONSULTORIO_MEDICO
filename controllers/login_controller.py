from flask import Blueprint, render_template, request, redirect, session
from models.usuario import Usuario
from models.medico import Medico

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['usuario']
        password = request.form['password']
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario,password=password,estado=True).first()
        if usuario:
            # ==========================
            # DATOS GENERALES DE SESIÓN
            # ==========================
            session['usuario_id'] = usuario.usuario_id
            session['nombre'] = usuario.personal.Nombre
            session['rol'] = usuario.rol.nombre_rol
            session['personal_id'] = usuario.CodPersonal
            # ==========================
            # SI ES MÉDICO
            # ==========================
            if usuario.rol.nombre_rol == 'Medico':
                medico = Medico.query.filter_by(CodPersonal=usuario.CodPersonal).first()
                if medico:
                    session['medico_id'] = medico.CodMedico
                return redirect('/dashboard_medico')
            # ==========================
            # ADMINISTRADOR
            # ==========================
            elif usuario.rol.nombre_rol == 'Administrador':
                return redirect('/dashboard_admin')
            # ==========================
            # RECEPCIONISTA
            # ==========================
            elif usuario.rol.nombre_rol == 'Recepcionista':
                return redirect('/dashboard_recepcionista')
            else:
                return "Rol no reconocido."
        else:
            return render_template('auth/login.html',error='Usuario o contraseña incorrectos.')
    return render_template('auth/login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@login_bp.route('/dashboard_admin')
def dashboard_admin():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"
    return render_template('dashboard/dashboard_admin.html')

@login_bp.route('/dashboard_recepcionista')
def dashboard_recepcionista():
    if session.get('rol') != 'Recepcionista':
        return "Acceso denegado"
    return render_template('dashboard/dashboard_recepcionista.html')

@login_bp.route('/dashboard_medico')
def dashboard_medico():
    if session.get('rol') != 'Medico':
        return "Acceso denegado"
    return render_template('dashboard/dashboard_medico.html')