import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI")
client = MongoClient(host=host)
db = client.jam


songs = db.songs
users = db.users
tags = db.tags