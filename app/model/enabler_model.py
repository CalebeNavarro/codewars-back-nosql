from flask import current_app
from app.controllers.db_controllers import DbController
import ipdb
from app.exc.enabler_exception import InvalidFields, EnablerNotFound, EnalberByFieldNotFound, ConflitUserName
import requests

class Enabler():
  validate_fields = ['username', 'name']
  
  def __init__(self, id: int, name: str, username: str) -> None:
    self.id = id
    self.name = name
    self.username = username
    self.current_honor = 0
    self.honors = []
    self.users = []

  @staticmethod
  def id_increment(data: dict):
    DbController.id_increment(data, "enabler")

  @staticmethod
  def get_all_enablers():
    all_enablers = list(current_app.db.enablers.find())
    for enabler in all_enablers:
      del enabler['_id']
    return all_enablers

  @staticmethod
  def find_enabler_by_id(id_enabler: int):
    enabler = current_app.db.enablers.find_one({"id": id_enabler})
    if not enabler:
      raise EnablerNotFound("enabler not found")
    del enabler['_id']
    return enabler


  def create_enabler(self):
    is_already_created = current_app.db.enablers.find_one({"username": self.username})
    if is_already_created:
      raise ConflitUserName(f"{self.username} already exist in systeam.")

    _id = current_app.db.enablers.insert_one(self.__dict__).inserted_id
    enabler = current_app.db.enablers.find_one({"_id": _id})
    del enabler['_id']
    return enabler

  @classmethod
  def update_enabler(clt, data: dict, id_enabler: int):
    try:
      is_already_created = current_app.db.enablers.find_one({"username": data['username']})
      if is_already_created:
        raise ConflitUserName(f"{data['username']} already exist in systeam.")
    except KeyError:
      ...
    
    for property in data:
      if property not in clt.validate_fields:
        raise InvalidFields("Invalid fields")

    enabler = current_app.db.enablers.find_one_and_update(
      {"id": id_enabler},
      {"$set": data}
    )
    enabler_updated = current_app.db.enablers.find_one({"_id": enabler['_id']})
    del enabler_updated["_id"]
    return enabler_updated

  @staticmethod
  def delete_enabler(id_enabler: int):
    is_enabler_deleted = DbController.delete_person(id_enabler, 'enablers')
    if not is_enabler_deleted:
      raise EnablerNotFound("Enabler not found")
  
  @staticmethod
  def find_enabler_by_parameter(field: str, name: str):
    enabler_found = current_app.db.enablers.find_one({field: name})
    if not enabler_found:
      raise EnalberByFieldNotFound(f'{name} is not in field {field}.')
    del enabler_found["_id"]
    return enabler_found