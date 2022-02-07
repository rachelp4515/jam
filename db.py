import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI")
client = MongoClient(host=host)
db = client.get_default_database()

playlists = db.playlists
