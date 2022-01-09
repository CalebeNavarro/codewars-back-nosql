from flask import Blueprint
from . import user_blueprint, enabler_blueprint, services_blueprint

bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(user_blueprint.bp)
bp.register_blueprint(enabler_blueprint.bp)
bp.register_blueprint(services_blueprint.bp)
