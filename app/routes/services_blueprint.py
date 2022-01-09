from flask import Blueprint
from app.views.codewars_view import patch_honor_of_all_users_and_enablers

bp = Blueprint('services_bp', __name__, url_prefix='/services')

bp.patch('/codewars')(patch_honor_of_all_users_and_enablers)