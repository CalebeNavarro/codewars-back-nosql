from flask import current_app

from app.controllers.datetime_controllers import DatetimeControllers

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
  def delete_person(id_user: int, collection):
    return current_app.db[collection].find_one_and_delete({"id": id_user})

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