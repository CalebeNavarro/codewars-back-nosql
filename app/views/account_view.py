from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.controllers.db_controllers import DbController


def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)

  password_in_system = DbController.access_db(username, password)

  if not password_in_system:
    return jsonify({"msg": "Bad username or password"}), 401

  access_token = create_access_token(identity=username)
  return jsonify(access_token=access_token)


@jwt_required()
def protected():

  # A função get_jwt_identity retorna a identidade do dono 
  # do token quando necessário
  current_user = get_jwt_identity()
  return jsonify(logged_in_as=current_user), 200
