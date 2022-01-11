from flask import Blueprint
from app.views.enabler_view import delete_enabler, get_all_enablers, post_enabler, patch_user, delete_enabler, get_enabler_by_id

bp = Blueprint('enablers_bp', __name__, url_prefix='/enablers')

bp.get('')(get_all_enablers)
bp.get('/<string:id_enabler>')(get_enabler_by_id)
bp.post('')(post_enabler)
bp.patch('/<string:id_enabler>')(patch_user)
bp.delete('/<string:id_enabler>')(delete_enabler)
