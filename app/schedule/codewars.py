from app.model.codewars_model import Codewars


def execute_codewars():
  print("beginning")
  r = Codewars.update_users_and_enablers()
  print(r)
  print("finish")
