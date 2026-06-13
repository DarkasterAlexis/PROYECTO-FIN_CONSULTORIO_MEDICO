from flask import Blueprint, render_template, request, session, redirect, url_for
from database import db
from models.paciente import Paciente
from datetime import datetime

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    # Solo Administrador y Recepcionista
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    if request.method == 'POST':
        ci = request.form['ci']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        sexo = request.form['sexo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        # Verificar CI duplicado
        paciente_existente = Paciente.query.filter_by(ci=ci).first()
        if paciente_existente:
            return "Error: Ya existe un paciente registrado con ese CI."
        try:
            nuevo_paciente = Paciente(ci=ci,nombres=nombres,apellidos=apellidos,
                fecha_nacimiento=datetime.strptime(fecha_nacimiento,'%Y-%m-%d').date() 
                if fecha_nacimiento else None,
                sexo=sexo,telefono=telefono,direccion=direccion,correo=correo,estado=True)
            db.session.add(nuevo_paciente)
            db.session.commit()
            return render_template('pacientes/registro_exitoso_paciente.html',nombres=nombres,apellidos=apellidos)
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar paciente: {str(e)}"
    return render_template('pacientes/registrar_paciente.html')

@paciente_bp.route('/listar_pacientes')
def listar_pacientes():
    # Solo Administrador y Recepcionista
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    lista_pacientes = Paciente.query.filter_by(estado=True).all()
    return render_template('pacientes/listar_pacientes.html',lista_pacientes=lista_pacientes)

@paciente_bp.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"
    
    paciente = Paciente.query.get_or_404(id)
    if request.method == 'POST':
        nuevo_ci = request.form['ci']
        paciente_existente = Paciente.query.filter(Paciente.ci == nuevo_ci,Paciente.paciente_id != id).first()
        if paciente_existente:
            return "Error: Ya existe otro paciente con ese CI."

        paciente.ci = nuevo_ci
        paciente.nombres = request.form['nombres']
        paciente.apellidos = request.form['apellidos']
        fecha = request.form['fecha_nacimiento']
        paciente.fecha_nacimiento = (datetime.strptime(fecha, '%Y-%m-%d').date()if fecha else None)
        paciente.sexo = request.form['sexo']
        paciente.telefono = request.form['telefono']
        paciente.direccion = request.form['direccion']
        paciente.correo = request.form['correo']
        db.session.commit()
        return redirect(url_for('paciente.listar_pacientes'))
    return render_template('pacientes/editar_paciente.html',paciente=paciente)

@paciente_bp.route('/eliminar_paciente/<int:id>')
def eliminar_paciente(id):
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    paciente = Paciente.query.get_or_404(id)
    paciente.estado = False
    db.session.commit()
    return redirect(url_for('paciente.listar_pacientes'))