from flask import jsonify, request
import ipdb

from app.model.enabler_model import Enabler
from app.exc.enabler_exception import InvalidFields, EnablerNotFound, EnalberByFieldNotFound, ConflitUserName
from app.exc.person_exception import PersonNotFound
from flask_jwt_extended import jwt_required

def get_all_enablers():
  name = request.args.get("name", "")
  username = request.args.get("username", "")
  
  if name:
    try:
      enabler_found = Enabler.find_enabler_by_parameter("name", name)
      return jsonify(enabler_found), 200
    except EnalberByFieldNotFound as e:
      return {"message": str(e)}, 404
  elif username:
    try:
      enabler_found = Enabler.find_enabler_by_parameter("username", username)
      return jsonify(enabler_found), 200
    except EnalberByFieldNotFound as e:
      return {"message": str(e)}, 404

  enabler_list = Enabler.get_all_enablers()
  return jsonify(enabler_list), 200


def get_enabler_by_id(id_enabler: str):
  try:
    enabler = Enabler.find_enabler_by_id(id_enabler)
  except PersonNotFound as e:
    return {"message": str(e)}, 404
  return jsonify({'enabler': enabler}), 200


@jwt_required()
def post_enabler():
  data = request.json
  try:
    if not data or not data['username']:
      return {'message': 'Missing Json'}, 403
  except KeyError:
    return {"message": "Missing Key"}, 404

  try:
    enabler = Enabler(**data)
    enabler_created = enabler.create_enabler()
  except TypeError as e:
    return {'message': str(e).split('an ')[1]}, 400
  except ConflitUserName as e:
    return {"message": str(e)}, 409

  return jsonify(enabler_created), 201


@jwt_required()
def patch_user(id_enabler: int):
  data = request.json
  if not data:
    return {'message': 'Missing Json'}, 400

  try:
    enabler_updated = Enabler.update_enabler(data, id_enabler)
  except InvalidFields as e:
    return {"message": str(e)}, 400
  except TypeError:
    return {"message": "Enabler not found"}, 404
  except ConflitUserName as e:
    return {"message": str(e)}, 409
  
  return {"message": enabler_updated}, 201


@jwt_required()
def delete_enabler(id_enabler: int):
  try:
    Enabler.delete_enabler(id_enabler)
  except EnablerNotFound as e:
    return {"message": str(e)}, 404
  return {}, 204
