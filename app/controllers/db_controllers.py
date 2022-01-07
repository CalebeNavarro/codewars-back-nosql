from flask import current_app

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