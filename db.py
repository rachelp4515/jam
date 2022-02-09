import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI")
client = MongoClient(host=host)
db = client.jam

playlists = db.playlists
users = db.users
