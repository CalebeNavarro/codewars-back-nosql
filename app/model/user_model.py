from flask import current_app
from app.controllers.db_controllers import DbController
import ipdb
from app.exc.person_exception import PersonNotFound
from app.exc.user_exception import InvalidFields, UserNotFound, UserByFieldNotFound, ConflitUserName, UserNameInvalid
from app.exc.enabler_exception import EnablerNotFound


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
    return DbController.find_all_person('users')

  @staticmethod
  def find_user_by_id(id_user: int):
    try:
      return DbController.find_one_person_by_id('users', id_user)
    except PersonNotFound:
      raise PersonNotFound("User not found")


  def create_user(self):
    if self.username == "":
      raise UserNameInvalid("Username invalido")
    is_already_created = current_app.db.users.find_one({"username": self.username})
    if is_already_created:
      raise ConflitUserName(f"{self.username} already exist in systeam.")

    user = DbController.insert_one_person('users', self.__dict__)
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
      except (ConflitUserName, UserNameInvalid):
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
        raise ConflitUserName(f"{data['username']} already exist in system")
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
    is_user_deleted = DbController.delete_person('users', id_user)
    if not is_user_deleted:
      raise UserNotFound("User not found")
    return None
  
  @staticmethod
  def find_user_by_parameter(field: str, value: str):
    user_found = DbController.find_one_person_by_parameter('users', field, value)
    if not user_found:
      raise UserByFieldNotFound(f'{value} is not in field {field}.')
    del user_found["_id"]
    return user_found
