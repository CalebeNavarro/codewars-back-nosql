from flask import current_app
from app.controllers.db_controllers import DbController
import ipdb
from app.exc.user_exception import InvalidFields, UserNotFound, UserByFieldNotFound, ConflitUserName, UserNameInvalid
from app.exc.enabler_exception import EnablerNotFound

import requests

from datetime import datetime
from pytz import timezone


class User():
  validate_fields = ['username', 'name']

  def __init__(self, id: int, name: str, username: str) -> None:
    self.id = id
    self.name = name
    self.username = username
    self.current_honor = 0
    self.honors = []

  @staticmethod
  def id_increment(data: dict):
    DbController.id_increment(data, "user")

  @staticmethod
  def get_all_users():
    all_users = list(current_app.db.users.find())
    for user in all_users:
      del user['_id']
    return all_users

  @staticmethod
  def find_user_by_id(id_user: int):
    user = current_app.db.users.find_one({"id": id_user})
    if not user:
      raise UserNotFound("User not found")
    del user['_id']
    return user

  def create_user(self):
    if self.username == "":
      raise UserNameInvalid("Username invalido")
    is_already_created = current_app.db.users.find_one({"username": self.username})
    if is_already_created:
      raise ConflitUserName(f"{self.username} already exist in systeam.")

    _id = current_app.db.users.insert_one(self.__dict__).inserted_id
    user = current_app.db.users.find_one({"_id": _id})
    del user['_id']
    return user

  @classmethod
  def create_user_already_in_enabler(clt, id_enabler: int, data: dict):
    result_searched_api = {
      "not_generated": {
        "message": "username already in system",
        "count": 0,
        "username": []
      },
      "generated": {
        "count": 0,
        "people": []
      }
    }

    enabler = current_app.db.enablers.find_one({"id": id_enabler})
    if not enabler:
      raise EnablerNotFound("enabler not found")
    del enabler['_id']
    
    for user_data in data["users"]:
      User.id_increment(user_data)
      user = User(**user_data)
      try:
        user_created = user.create_user()
        result_searched_api.get("generated").get("people").append(user_created)
        result_searched_api.get("generated")["count"] += 1
        enabler.get("users").append(user_created.get("id"))
      except ConflitUserName:
        result_searched_api.get("not_generated").get("username").append(user_data.get("username"))
        result_searched_api.get("not_generated")["count"] += 1
    
    current_app.db.enablers.find_one_and_update(
      {"id": id_enabler},
      {"$set": {"users": enabler.get("users")}}
      )
    return result_searched_api

  @classmethod
  def update_user(clt, data: dict, id_user: int):
    try:
      is_already_created = current_app.db.users.find_one({"username": data['username']})
      if is_already_created:
        raise ConflitUserName(f"{data['username']} already exist in systeam.")
    except KeyError:
      ...
    for property in data:
      if property not in clt.validate_fields:
        raise InvalidFields("Invalid fields")
    
    user = current_app.db.users.find_one_and_update(
      {"id": id_user},
      {"$set": data}
    )
    user_updated = current_app.db.users.find_one({"_id": user['_id']})
    del user_updated["_id"]
    return user_updated

  @staticmethod
  def delete_user(id_user: int):
    is_user_deleted = DbController.delete_person(id_user, 'users')
    if not is_user_deleted:
      raise UserNotFound("User not found")
  
  @staticmethod
  def find_user_by_parameter(field: str, name: str):
    user_found = current_app.db.users.find_one({field: name})
    if not user_found:
      raise UserByFieldNotFound(f'{name} is not in field {field}.')
    del user_found["_id"]
    return user_found

  @staticmethod
  def request_codewars_api_of_all_users():
    result_searched_api = {
      "incorrect_usernames": {
        "count": 0,
        "people": []
      },
      "updated": {
        "count": 0,
        "people": []
      }
    }

    for user in current_app.db.users.find():
      r = requests.get(f'https://www.codewars.com/api/v1/users/{user["username"]}').json()
      try:
        format = "%d/%m/%Y"
        now_utc = datetime.now(timezone('UTC'))
        now_brasil = now_utc.astimezone(timezone('Brazil/East'))

        data_and_honor_obj = {
          "date": now_brasil.strftime(format),
          "honor": r["honor"]
        }

        honors = user['honors']
        is_update = True
        for honor in honors:
          if honor['date'] == now_brasil.strftime(format):
            is_update = False

        if is_update:
          current_app.db.users.find_one_and_update(
            {"id": user['id']},
            {
              "$set": {
                "current_honor": r['honor']
              },
              "$push": {
                "honors": data_and_honor_obj
              }
            }
          )
        else:
          current_app.db.users.find_one_and_update(
            {"id": user['id']},
            {
              "$set": {
                "current_honor": r['honor']
              }
            }
          )
        result_searched_api.get("updated").get("people").append(user.get("username"))
        result_searched_api.get("updated")["count"] += 1

      except KeyError:
        del user['_id']
        result_searched_api.get("incorrect_usernames").get("people").append(user)
        result_searched_api.get("incorrect_usernames")["count"] += 1
        pass

    return result_searched_api
