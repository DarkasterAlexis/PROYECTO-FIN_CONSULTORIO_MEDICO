from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models.personal import Personal
from models.usuario import Usuario
from models.rol import Rol

personal_bp = Blueprint('personal', __name__)

@personal_bp.route('/registrar_personal', methods=['GET', 'POST'])
def registrar_personal():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = request.form['password']
        rol_id = request.form['rol_id']

        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(nombre_usuario=usuario).first()
        if usuario_existente:
            return "Error: El nombre de usuario ya existe."
        try:
            nuevo_personal = Personal(Nombre=nombre,Apellidos=apellidos,Telefono=telefono,Estado='Activo')
            db.session.add(nuevo_personal)

            # Obtiene el CodPersonal sin guardar todavía
            db.session.flush()
            nuevo_usuario = Usuario(nombre_usuario=usuario,password=password,rol_id=int(rol_id),CodPersonal=nuevo_personal.CodPersonal)
            db.session.add(nuevo_usuario)
            # Guarda ambas tablas juntas
            db.session.commit()
            return render_template('registro_exitoso.html',nombre=nombre, apellidos=apellidos)
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar: {str(e)}"
    return render_template('registrar_personal.html')

@personal_bp.route('/listar_personal')
def listar_personal():
    lista_usuarios = Usuario.query.filter_by(estado=True).all()
    return render_template('listar_personal.html',lista_personal=lista_usuarios)

@personal_bp.route('/editar_personal/<int:id>', methods=['GET', 'POST'])
def editar_personal(id):
    personal = Personal.query.get_or_404(id)
    if request.method == 'POST':
        personal.Nombre = request.form['nombre']
        personal.Apellidos = request.form['apellidos']
        personal.Telefono = request.form['telefono']
        db.session.commit()
        return redirect(url_for('personal.listar_personal'))
    return render_template('editar_personal.html',personal=personal)

@personal_bp.route('/eliminar_personal/<int:id>')
def eliminar_personal(id):
    # Buscar al personal
    personal = Personal.query.get_or_404(id)
    # Buscar el usuario asociado
    usuario = Usuario.query.filter_by(CodPersonal=id).first()
    # Eliminación lógica
    personal.Estado = 'Inactivo'
    # Desactivar acceso al sistema
    if usuario:
        usuario.estado = False
    db.session.commit()
    return redirect(url_for('personal.listar_personal'))