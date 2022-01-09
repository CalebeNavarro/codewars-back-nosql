from flask import current_app
import ipdb

from app.controllers.datetime_controllers import DatetimeControllers
from app.controllers.codewars_controllers import CodewarsControllers
from app.controllers.db_controllers import DbController


class Codewars():
  
  def __init__(self) -> None:
      pass

  @staticmethod
  def request_codewars(collection: str, result_searched_api: dict):
    for current_person in current_app.db[collection].find():
      request = CodewarsControllers.response_by_username(current_person['username'])

      try:
        is_update = DatetimeControllers.is_person_already_been_updated_today(current_person)

        if not is_update:
          DbController.update_increment_object_honor_person(current_person, collection, request['honor'])
        else:
          DbController.update_current_honor_person(current_person, collection, request['honor'])

        result_searched_api.get("updated").get("people").append(current_person.get("username"))
        result_searched_api.get("updated")["count"] += 1

      except KeyError:
        del current_person['_id']
        result_searched_api.get("incorrect_usernames").get("people").append(current_person)
        result_searched_api.get("incorrect_usernames")["count"] += 1
        pass
  
  @classmethod
  def update_users_and_enablers(clt):
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
    clt.request_codewars('users', result_searched_api)
    clt.request_codewars('enablers', result_searched_api)
    return result_searched_api
