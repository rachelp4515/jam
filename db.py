import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI")
client = MongoClient(host=host)
db = client.get_database('PLMs')


songs = db.songs
users = db.users
tags = db.tags
playlists = db.playlists
lists = db.lists
