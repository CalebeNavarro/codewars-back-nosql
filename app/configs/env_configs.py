from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
import os
load_dotenv()

def init_app(app: Flask):
    CORS(app, origins=["http://localhost:3001", "https://codewars-app-calebekenzie.vercel.app"])
    app.config["JSON_SORT_KEYS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("PASSWORD_AUTH")
