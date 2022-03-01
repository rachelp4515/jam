from flask import Blueprint, render_template, redirect, url_for, request, session
from bson.objectid import ObjectId
import db
import math
from random import randrange

routes = Blueprint("gen", __name__, url_prefix="/gen")

@routes.route('/')
def index():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
    tags = db.tags.find()
    songs = db.songs.find({"user_id": user["_id"]})
    return render_template('gen/create.html', tags=tags, songs=songs)



"""

def generate()
    tags = request.form.get('tags') --> returns a list of tags?
    library = db.songs.find()
    length = request.form.get('length') --> returns num, which will be amount of songs sampled
    samplelist = []

    for song in library
        if song_id in tags[songs]
        append song to samplelist
        playlist = samplelist.aggregate( [ { "$sample": {"size": length } } ] )

<--------------------------------------------------->
"""
@routes.route('/create/', methods=["POST"])
def generate():
    tags = request.form.getlist('tags')
    print(tags, '-----------------------------')
    library = db.songs.find()
    song_num = int(request.form.get('length'))
    amount_per_tag = int(song_num / len(tags) + .5)

    song_list = []
    for tag_index in range(len(tags) - 1):
        tag = tags[tag_index]
        print(tag, "TAG")
        for i in range(amount_per_tag):
            added = False
            tag_obj = db.tags.find_one({"_id": ObjectId(tag)})
            while(not added):
                print(tag_obj)
                song = tag_obj["songs"][randrange(0, len(tag_obj["songs"]))]
                if(song not in song_list):
                    song_list.append(song)
                    added = True

    for i in range(song_num - len(song_list)):
        tag = tags[-1]
        added = False
        while(not added):
            tag_obj = db.tags.find_one({"_id": ObjectId(tag)})
            print(tag_obj)
            song = tag_obj["songs"][randrange(0, len(tag_obj["songs"]))]
            if(song not in song_list):
                song_list.append(song)
                added=True

        # get the song names from ids, so song name is returned instead of the id 
    return render_template('/gen/new_list.html', song_list=song_list)
        



