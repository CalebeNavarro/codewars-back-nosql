from flask import jsonify
from app.model.codewars_model import Codewars


def patch_honor_of_all_users_and_enablers():
  result_searched_api = Codewars.update_users_and_enablers()
  return jsonify({"message": result_searched_api}), 200