from flask.cli import AppGroup
from flask import Flask
from app.model.codewars_model import Codewars
from click import echo


def cli_routine(app: Flask):
  cli_routine_group = AppGroup("routine")

  @cli_routine_group.command("codewars")
  def cli_routine_codewars():
    Codewars.update_users_and_enablers()

  app.cli.add_command(cli_routine_group)

def init_app(app: Flask):
  cli_routine(app)
