from flask import Blueprint
from app.views.user_view import get_all_users, post_user, update_user, delete_user, patch_all_users, get_user_by_id, post_users_in_enabler, hielol

bp = Blueprint('users_bp', __name__, url_prefix='/users')

bp.get('')(get_all_users)
bp.get('/another')(hielol)
bp.get('/<int:id_user>')(get_user_by_id)
bp.post('')(post_user)
bp.post('/<int:id_enabler>')(post_users_in_enabler)
bp.patch('/<int:id_user>')(update_user)
bp.patch('/refresh')(patch_all_users)
bp.delete('/<int:id_user>')(delete_user)
