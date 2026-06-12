from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models.personal import Personal
from models.usuario import Usuario
from models.medico import Medico
from models.rol import Rol

medico_bp = Blueprint('medico', __name__)

@medico_bp.route('/registrar_medico', methods=['GET', 'POST'])
def registrar_medico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = request.form['password']
        especialidad = request.form['especialidad']
        matricula = request.form['matricula']
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(nombre_usuario=usuario).first()
        if usuario_existente:
            return "Error: El nombre de usuario ya existe."

        # Verificar matrícula repetida
        matricula_existente = Medico.query.filter_by(MatriculaProfesional=matricula).first()
        if matricula_existente:
            return "Error: La matrícula profesional ya existe."

        # Buscar rol Médico
        rol_medico = Rol.query.filter_by(nombre_rol='Medico').first()
        if not rol_medico:
            return "Error: No existe el rol Médico."
        try:
            # Crear PERSONAL
            nuevo_personal = Personal(Nombre=nombre,Apellidos=apellidos,Telefono=telefono,Estado='Activo')
            db.session.add(nuevo_personal)
            # Obtener CodPersonal
            db.session.flush()
            # Crear USUARIO
            nuevo_usuario = Usuario(nombre_usuario=usuario,password=password,rol_id=rol_medico.rol_id,CodPersonal=nuevo_personal.CodPersonal)
            db.session.add(nuevo_usuario)
            # Crear MEDICO
            nuevo_medico = Medico(Especialidad=especialidad,MatriculaProfesional=matricula,Estado='Activo',CodPersonal=nuevo_personal.CodPersonal)
            db.session.add(nuevo_medico)
            # Guardar todo junto
            db.session.commit()
            return redirect(url_for('medico.listar_medicos'))
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar: {str(e)}"
    return render_template('registrar_medico.html')

@medico_bp.route('/listar_medicos')
def listar_medicos():
    lista_medicos = Medico.query.filter_by(Estado='Activo').all()
    return render_template('listar_medicos.html',lista_medicos=lista_medicos)

@medico_bp.route('/editar_medico/<int:id>', methods=['GET', 'POST'])
def editar_medico(id):
    medico = Medico.query.get_or_404(id)
    personal = Personal.query.get_or_404(medico.CodPersonal)
    if request.method == 'POST':
        personal.Nombre = request.form['nombre']
        personal.Apellidos = request.form['apellidos']
        personal.Telefono = request.form['telefono']
        medico.Especialidad = request.form['especialidad']
        medico.MatriculaProfesional = request.form['matricula']
        try:
            db.session.commit()
            return redirect(url_for('medico.listar_medicos'))
        except Exception as e:
            db.session.rollback()
            return f"Error al actualizar: {str(e)}"
    return render_template('editar_medico.html',medico=medico,personal=personal)

@medico_bp.route('/eliminar_medico/<int:id>')
def eliminar_medico(id):
    medico = Medico.query.get_or_404(id)
    try:
        # Desactivar médico
        medico.Estado = 'Inactivo'
        # Desactivar personal asociado
        personal = Personal.query.get(medico.CodPersonal)
        if personal:
            personal.Estado = 'Inactivo'

        # Desactivar usuario asociado
        usuario = Usuario.query.filter_by(CodPersonal=medico.CodPersonal).first()
        if usuario:
            usuario.estado = False

        db.session.commit()
        return redirect(url_for('medico.listar_medicos'))

    except Exception as e:
        db.session.rollback()
        return f"Error al desactivar médico: {str(e)}"