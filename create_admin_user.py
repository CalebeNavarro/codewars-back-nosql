from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

import bson

import uuid

uri = os.environ.get("MONGODB_URI")
client = MongoClient(uri)
db = client.test

password = "senha fraca"
username = "Calebe"

def create_admin_user(username: str, password: str):
  user_uuid = uuid.uuid4()

  db.accounts.insert_one({
    "id": str(user_uuid),
    "username": username,
    "password": password
  })
  return None
# create_admin_user(username, password)
a = db.accounts.find_one({
  "password": "RjwZUNmfyaY5R9GU"
})
print(a['username'])
# print(list(db.accounts.find()))
# db.accounts.drop
# print(bson.Binary.from_uuid(uuid.uuid4()))

