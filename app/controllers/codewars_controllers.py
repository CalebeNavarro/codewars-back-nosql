import requests


class CodewarsControllers():
  def __init__(self) -> None:
      pass

  @staticmethod
  def response_by_username(username: str):
    return requests.get(f'https://www.codewars.com/api/v1/users/{username}').json()