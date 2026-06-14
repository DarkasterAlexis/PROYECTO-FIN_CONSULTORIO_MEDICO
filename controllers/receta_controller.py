from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from models.receta import Receta
from models.detalle_receta import DetalleReceta
from models.historial_clinico import HistorialClinico
from models.paciente import Paciente
from models.medico import Medico

receta_bp = Blueprint('receta',__name__)

@receta_bp.route('/crear_receta/<int:historial_id>', methods=['GET','POST'])
def crear_receta(historial_id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"
    historial = HistorialClinico.query.get_or_404(historial_id)
    paciente = Paciente.query.get_or_404(historial.CodPaciente)
    medico = Medico.query.get_or_404(historial.CodMedico)
    if request.method == 'POST':
        receta = Receta(
            HistorialID=historial_id,
            paciente_id=paciente.paciente_id,
            CodMedico=medico.CodMedico,
            Observaciones=request.form['observaciones']
        )
        db.session.add(receta)
        db.session.commit()
        detalle = DetalleReceta(
            RecetaID=receta.RecetaID,
            Medicamento=request.form['medicamento'],
            Dosis=request.form['dosis'],
            Frecuencia=request.form['frecuencia'],
            Duracion=request.form['duracion'],
            Indicaciones=request.form['indicaciones']
        )
        db.session.add(detalle)
        db.session.commit()
        return redirect(url_for('receta.ver_receta',receta_id=receta.RecetaID))
    return render_template('recetas/crear_receta.html',paciente=paciente,medico=medico)

@receta_bp.route('/recetas_medicas')
def recetas_medicas():
    if session.get('rol') != 'Medico':
        return "Acceso denegado"
    medico_id = session.get('medico_id')
    recetas = Receta.query.filter_by(CodMedico=medico_id).order_by(Receta.Fecha.desc()).all()
    return render_template('recetas/listar_recetas.html',recetas=recetas)

@receta_bp.route('/ver_receta/<int:receta_id>')
def ver_receta(receta_id):
    if session.get('rol') != 'Medico':
        return "Acceso denegado"
    
    receta = Receta.query.get_or_404(receta_id)
    return render_template('recetas/ver_receta.html',receta=receta)