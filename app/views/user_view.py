from app.exc.enabler_exception import EnablerNotFound
from app.model.user_model import User
from flask import jsonify, request
import ipdb
from app.exc.user_exception import InvalidFields, UserNotFound, UserByFieldNotFound, ConflitUserName, UserNameInvalid

from pymongo import MongoClient

from dotenv import load_dotenv
import os
load_dotenv()

uri = os.environ.get("MONGODB_URI")

client = MongoClient(uri)

db = client.test

def hielol():
  aa = db.users.find_one({"id": 1})
  del aa['_id']
  return jsonify({"message": aa})


def get_all_users():
  name = request.args.get("name", "")
  username = request.args.get("username", "")
  if name:
    try:
      user_found = User.find_user_by_parameter("name", name)
      return jsonify(user_found)
    except UserByFieldNotFound as e:
      return {"message": str(e)}, 404
  elif username:
    try:
      user_found = User.find_user_by_parameter("username", username)
      return jsonify(user_found)
    except UserByFieldNotFound as e:
      return {"message": str(e)}, 404

  user_list = User.get_all_users()
  return jsonify(user_list)


def get_user_by_id(id_user: int):
  try:
    user = User.find_user_by_id(id_user)
  except UserNotFound as e:
    return {"message": str(e)}, 404
  return jsonify({'user': user})


def post_user():
  data = request.json
  if not data:
    return {'message': 'Missing Json'}, 400

  try:
    User.id_increment(data)
    user = User(**data)
    user_created = user.create_user()
  except TypeError as e:
    return {'message': str(e).split('an ')[1]}, 400
  except ConflitUserName as e:
    return {"message": str(e)}, 409
  except UserNameInvalid as e:
    return {"message": str(e)}, 400

  return jsonify(user_created), 201


def post_users_in_enabler(id_enabler: int):
  data = request.json
  if not data:
    return {'message': 'Missing Json'}
  
  try:
    result_searched_api = User.create_user_already_in_enabler(id_enabler, data)
  except EnablerNotFound as e:
    return {"message": str(e)}, 404
  except TypeError as e:
    return {'message': str(e).split('an ')[1]}
  except KeyError as e:
    return {"message": f"missing field {e}"}, 400

  return jsonify({"message": result_searched_api}), 200


def update_user(id_user: int):
  data = request.json
  if not data:
    return {'message': 'Missing Json'}

  try:
    user_updated = User.update_user(data, id_user)
  except InvalidFields as e:
    return {"message": str(e)}, 400
  except TypeError:
    return {"message": "User not found"}, 404
  except ConflitUserName as e:
    return {"message": str(e)}, 409
  except UserNameInvalid as e:
    return {"message": str(e)}, 400

  return {"message": user_updated}, 200


def delete_user(id_user: int):
  try:
    User.delete_user(id_user)
  except UserNotFound as e:
    return {"message": str(e)}, 404
  return {}, 204


def patch_all_users():
  result_searched_api = User.request_codewars_api_of_all_users()
  return jsonify({"message": result_searched_api}), 200

