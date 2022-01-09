from pymongo import MongoClient
from flask import Flask

from dotenv import load_dotenv
import os
load_dotenv()

uri = os.environ.get("MONGODB_URI")
client = MongoClient(uri)
db = client.test

def init_app(app: Flask):
  app.db = db
