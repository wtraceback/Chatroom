from flask import render_template
from app import db
from app.errors import errors_bp


@errors_bp.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


@errors_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
