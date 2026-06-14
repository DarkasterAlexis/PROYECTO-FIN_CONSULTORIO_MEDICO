from flask import Blueprint, render_template, session
from database import db
from models.paciente import Paciente
from models.personal import Personal
from models.medico import Medico
from models.cita import Cita
from models.historial_clinico import HistorialClinico
from models.receta import Receta

reporte_bp = Blueprint('reporte',__name__)

@reporte_bp.route('/reportes_admin')
def reportes_admin():
    if session.get('rol') != 'Administrador':
        return "Acceso denegado"

    total_pacientes = Paciente.query.count()
    pacientes_activos = Paciente.query.filter_by(estado=True).count()
    total_personal = Personal.query.count()
    total_medicos = Medico.query.count()
    total_citas = Cita.query.count()
    citas_confirmadas = Cita.query.filter_by(Estado='Confirmada').count()
    citas_canceladas = Cita.query.filter_by(Estado='Cancelada').count()
    return render_template(
        'reportes/reportes_admin.html',
        total_pacientes=total_pacientes,
        pacientes_activos=pacientes_activos,
        total_personal=total_personal,
        total_medicos=total_medicos,
        total_citas=total_citas,
        citas_confirmadas=citas_confirmadas,
        citas_canceladas=citas_canceladas
    )

@reporte_bp.route('/reportes_medico')
def reportes_medico():
    if session.get('rol') != 'Medico':
        return "Acceso denegado"

    medico_id = session.get('medico_id')
    atenciones = HistorialClinico.query.filter_by(CodMedico=medico_id).all()
    recetas = Receta.query.filter_by(CodMedico=medico_id).all()
    return render_template('reportes/reportes_medico.html',atenciones=atenciones,recetas=recetas)