from pymongo import MongoClient
from flask import Flask

from dotenv import load_dotenv
import os
load_dotenv()

password_mongodb_atlas_user = os.getenv("PASSWORD_MONGO_ATLAS_USER")

client = MongoClient(f"mongodb+srv://calebe-navarro:{password_mongodb_atlas_user}@cluster0.zuv0r.mongodb.net/codewars-kenzie?retryWrites=true&w=majority")


db = client.test

def init_app(app: Flask):
  app.db = db
