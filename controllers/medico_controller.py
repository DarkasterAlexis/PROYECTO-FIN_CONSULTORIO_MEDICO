from flask import Blueprint, render_template

medico_bp = Blueprint('medico', __name__)

@medico_bp.route('/registrar_medico')
def registrar_medico():

    return render_template(
        'registrar_medico.html'
    )