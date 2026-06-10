from flask import Blueprint, render_template

personal_bp = Blueprint('personal', __name__)

@personal_bp.route('/registrar_personal')
def registrar_personal():
    return render_template('registrar_personal.html')