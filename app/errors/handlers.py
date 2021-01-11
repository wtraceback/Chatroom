from flask import render_template
from flask_wtf.csrf import CSRFError
from app import db
from app.errors import errors_bp


@errors_bp.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/errors.html', description=error.description, code=error.code), 400


@errors_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/errors.html', description=error.description, code=error.code), 404


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('errors/errors.html', description='Internal Server Error', code=error.code), 500


@errors_bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template('errors/errors.html', description=error.description, code=error.code), 400
