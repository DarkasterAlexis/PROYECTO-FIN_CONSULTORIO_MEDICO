from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from models.cita import Cita
from models.paciente import Paciente
from models.medico import Medico
from datetime import datetime

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