from time import sleep
from flask import Flask
from app.configs import database, env_configs, jwt
from app.routes import api_blueprint
from app.configs import commands
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from app.model.codewars_model import Codewars
import asyncio


def create_app():
  app = Flask(__name__)
  
  env_configs.init_app(app)
  database.init_app(app)
  jwt.init_app(app)

  app.register_blueprint(api_blueprint.bp)

  commands.init_app(app)

  return app
