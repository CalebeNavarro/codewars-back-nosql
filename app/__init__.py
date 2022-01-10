from flask import Flask, request, jsonify
from app.configs import database, env_configs, jwt
from app.routes import api_blueprint


def create_app():
  app = Flask(__name__)

  env_configs.init_app(app)
  database.init_app(app)
  jwt.init_app(app)

  app.register_blueprint(api_blueprint.bp)

  return app