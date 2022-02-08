from flask import Blueprint
from app.views.account_view import login, protected, refresh as identity 

bp = Blueprint('account_bp', __name__, url_prefix='/account')

bp.post('/auth')(login)
bp.get('/protected')(protected)
bp.get('/refresh')(identity)
