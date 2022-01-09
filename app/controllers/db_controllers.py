from flask import current_app

from app.controllers.datetime_controllers import DatetimeControllers
from app.exc.person_exception import PersonNotFound

class DbController():
  def __init__(self) -> None:
      pass
  
  @staticmethod
  def id_increment(data: dict, person: str):
    current_app.db.id_count.find_one_and_update(
      {"id": person},
      {"$inc": {"count": 1}}
    )
    data['id'] = current_app.db.id_count.find_one({"id": person})['count']

  @staticmethod
  def delete_person(collection: str, id_user: int):
    return current_app.db[collection].find_one_and_delete({"id": id_user})

  @staticmethod
  def find_all_person(collection: str):
    all_person = list(current_app.db[collection].find())
    for user in all_person:
      del user['_id']
    return all_person

  @staticmethod
  def find_one_person_by_id(collection: str, id_person: int):
    person = current_app.db[collection].find_one({"id": id_person})
    if not person:
      raise PersonNotFound()
    del person['_id']
    return person

  def find_one_person_by_parameter(collection: str, field: str, value: str):
    user_found = current_app.db[collection].find_one({field: value})
    return user_found

  @staticmethod
  def insert_one_person(collection: str, data: dict):
    _id = current_app.db[collection].insert_one(data).inserted_id
    user = current_app.db.users.find_one({"_id": _id})
    return user

  @staticmethod
  def update_increment_object_honor_person(person, collection: str, honor: int):
    now_brasil = DatetimeControllers.time_now_brasil()

    data_and_honor_obj = {
      "date": now_brasil,
      "honor": honor
    }
    current_app.db[collection].find_one_and_update(
      {"id": person['id']},
      {
        "$set": {
          "current_honor": honor
        },
        "$push": {
          "honors": data_and_honor_obj
        }
      }
    )
    return None

  @staticmethod
  def update_current_honor_person(person: str, collection: str, honor: int):
    current_app.db[collection].find_one_and_update(
      {"id": person['id']},
      {
        "$set": {
          "current_honor": honor
        }
      }
    )
    return None