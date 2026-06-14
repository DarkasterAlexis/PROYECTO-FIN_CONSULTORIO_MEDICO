from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from models.cita import Cita
from models.paciente import Paciente
from models.medico import Medico
from models.usuario import Usuario
from models.historial_clinico import HistorialClinico
from datetime import datetime, date

cita_bp = Blueprint('cita', __name__)
@cita_bp.route('/registrar_cita', methods=['GET', 'POST'])
def registrar_cita():
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    pacientes = Paciente.query.filter_by(estado=True).all()
    medicos = Medico.query.filter_by(Estado='Activo').all()
    if request.method == 'POST':
        paciente_id = request.form['paciente']
        medico_id = request.form['medico']
        fecha = datetime.strptime(request.form['fecha'],'%Y-%m-%d').date()
        hora = datetime.strptime(request.form['hora'],'%H:%M').time()
        motivo = request.form['motivo']
        nueva_cita = Cita(CodPaciente=paciente_id,CodMedico=medico_id,Fecha=fecha,Hora=hora,Motivo=motivo,Estado='Confirmada',Origen='Recepcion')
        db.session.add(nueva_cita)
        db.session.commit()
        return redirect(url_for('cita.listar_citas'))
    return render_template('citas/registrar_cita.html',pacientes=pacientes,medicos=medicos)

@cita_bp.route('/listar_citas')
def listar_citas():
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    citas = Cita.query.order_by(Cita.Fecha,Cita.Hora).all()
    return render_template('citas/listar_citas.html',citas=citas)

@cita_bp.route('/editar_cita/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    cita = Cita.query.get_or_404(id)
    medicos = Medico.query.filter_by(Estado='Activo').all()
    if request.method == 'POST':
        cita.CodMedico = request.form['medico']
        cita.Fecha = datetime.strptime(request.form['fecha'],'%Y-%m-%d').date()
        cita.Hora = datetime.strptime(request.form['hora'],'%H:%M').time()
        cita.Motivo = request.form['motivo']
        db.session.commit()
        return redirect(url_for('cita.listar_citas'))
    return render_template('citas/editar_cita.html',cita=cita,medicos=medicos)

@cita_bp.route('/cancelar_cita/<int:id>')
def cancelar_cita(id):
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    cita = Cita.query.get_or_404(id)
    cita.Estado = 'Cancelada'
    db.session.commit()
    return redirect(url_for('cita.listar_citas'))

@cita_bp.route('/confirmar_cita/<int:id>')
def confirmar_cita(id):
    if session.get('rol') not in ['Administrador', 'Recepcionista']:
        return "Acceso denegado"

    cita = Cita.query.get_or_404(id)
    cita.Estado = 'Confirmada'
    db.session.commit()
    return redirect(url_for('cita.listar_citas'))

@cita_bp.route('/agenda_medica')
def agenda_medica():
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    usuario = Usuario.query.get(session.get('usuario_id'))
    medico = Medico.query.filter_by(CodPersonal=usuario.CodPersonal).first()
    hoy = date.today()
    citas = Cita.query.filter(Cita.CodMedico == medico.CodMedico,Cita.Fecha == hoy,Cita.Estado == 'Confirmada').order_by(Cita.Hora).all()
    return render_template('citas/agenda_medica.html',citas=citas)

@cita_bp.route('/iniciar_atencion/<int:id>', methods=['GET','POST'])
def iniciar_atencion(id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"
    cita = Cita.query.get_or_404(id)
    if request.method == 'POST':
        nuevo_historial = HistorialClinico(
            paciente_id=cita.CodPaciente,
            CodMedico=cita.CodMedico,
            CodCita=cita.CodCita,
            MotivoConsulta=request.form['motivo_consulta'],
            Diagnostico=request.form['diagnostico'],
            Tratamiento=request.form['tratamiento'],
            Observaciones=request.form['observaciones']
        )
        db.session.add(nuevo_historial)
        # cambia la cita de Confirmada a Atendida
        cita.Estado = "Atendida"
        db.session.commit()
        return redirect(url_for('cita.finalizar_atencion',id=cita.CodCita))
    return render_template('citas/iniciar_atencion.html',cita=cita)

@cita_bp.route('/historial_paciente/<int:id>')
def historial_paciente(id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    paciente = Paciente.query.get_or_404(id)
    historial = HistorialClinico.query.filter_by(paciente_id=id).order_by(HistorialClinico.FechaAtencion.desc()).all()
    return render_template('citas/historial_paciente.html',paciente=paciente,historial=historial)

@cita_bp.route('/finalizar_atencion/<int:id>')
def finalizar_atencion(id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    cita = Cita.query.get_or_404(id)
    return render_template('citas/finalizar_atencion.html',cita=cita)

@cita_bp.route('/crear_cita_control/<int:paciente_id>/<int:medico_id>',methods=['GET','POST'])
def crear_cita_control(paciente_id, medico_id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    paciente = Paciente.query.get_or_404(paciente_id)
    medico = Medico.query.get_or_404(medico_id)
    if request.method == 'POST':
        nueva_cita = Cita(
            CodPaciente=paciente_id,
            CodMedico=medico_id,
            Fecha=datetime.strptime(request.form['fecha'],'%Y-%m-%d').date(),
            Hora=datetime.strptime(request.form['hora'],'%H:%M').time(),
            Motivo=request.form['motivo'],
            Estado='Pendiente',
            Origen='Medico'
        )
        db.session.add(nueva_cita)
        db.session.commit()
        return redirect(url_for('cita.agenda_medica'))
    return render_template('citas/crear_cita_control.html',paciente=paciente,medico=medico)

@cita_bp.route('/historial_atenciones')
def historial_atenciones():
    # Solo médicos
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    medico_id = session.get('medico_id')
    lista_atenciones = HistorialClinico.query.filter_by(CodMedico=medico_id).order_by(HistorialClinico.FechaAtencion.desc()).all()
    return render_template('medico/historial_atenciones.html',atenciones=lista_atenciones)

@cita_bp.route('/agenda_recepcion')
def agenda_recepcion():
    # Solo Recepción y Administrador pueden acceder
    if session.get('rol') not in ['Recepcionista', 'Administrador']:
        return "Acceso denegado"

    hoy = date.today()
    citas = Cita.query.filter(Cita.Fecha == hoy).order_by(Cita.Hora).all()
    total = len(citas)
    confirmadas = sum(1 for cita in citas if cita.Estado == 'Confirmada')
    pendientes = sum(1 for cita in citas if cita.Estado == 'Pendiente')
    atendidas = sum(1 for cita in citas if cita.Estado == 'Atendida')
    canceladas = sum(1 for cita in citas if cita.Estado == 'Cancelada')
    return render_template('citas/agenda_recepcion.html',citas=citas,total=total,confirmadas=confirmadas,
        pendientes=pendientes,atendidas=atendidas,canceladas=canceladas,fecha=hoy)