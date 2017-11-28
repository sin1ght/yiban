from . import main_blueprint
from flask import redirect,send_from_directory,current_app
from ..decorators import login_required


@main_blueprint.route('/stu_index')
@login_required
def stu_index():
    url='http://127.0.0.1:8098/index.html'
    return redirect(url)


@main_blueprint.route('/tea_index')
@login_required
def tea_index():
    url = 'http://127.0.0.1:8098/pages/teacher.html'
    return redirect(url)


@main_blueprint.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)