from flask import Blueprint
from app.views.user_view import get_all_users, post_user, update_user, delete_user, get_user_by_id, post_users_in_enabler

bp = Blueprint('users_bp', __name__, url_prefix='/users')

bp.get('')(get_all_users)
bp.get('/<string:id_user>')(get_user_by_id)
bp.post('')(post_user)
bp.post('/<string:id_enabler>')(post_users_in_enabler)
bp.patch('/<string:id_user>')(update_user)
bp.delete('/<string:id_user>')(delete_user)
