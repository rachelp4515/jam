from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from bson.objectid import ObjectId
import db

routes = Blueprint("songs", __name__, url_prefix="/songs")


# Index
@routes.route("/")
def index():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    tags = db.tags.find()
    songs = db.songs.find({"user_id": user["_id"]})
    return render_template("songs/library.html", songs=songs, tags=tags)


# Show one
@routes.route("/<string:song_id>/")
def show(song_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    if not ObjectId.is_valid(song_id):
        flash("Invalid song!")
        return redirect(url_for("songs.index"))

    song = db.songs.find_one({"_id": ObjectId(song_id), "user_id": user["_id"]})
    if not song:
        flash("That song does not exist!")
        return redirect(url_for("songs.index"))

    tags = db.tags.aggregate([
        {"$match": {"songs": {"$in": [song_id]}}}
    ])
    return render_template("songs/song.html", song=song, tags=tags)


# New song form
@routes.route("/new/")
def new():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
    tags = db.tags.find()
    return render_template("songs/new_song.html", tags=tags)


# Create song
@routes.route("/", methods=["POST"])
def create():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    song_name = request.form.get("name")
    song_artist = request.form.get("artist")

    if not song_name or not song_artist:
        flash("Missing info!")
        return redirect(url_for("songs.new"))

    song = {
        "user_id": user["_id"],
        "name": song_name,
        "artist": song_artist
    }
    db.songs.insert_one(song)
    checked_tags = [ObjectId(tag) for tag in request.form.getlist("tags")]
    if checked_tags:
        db.tags.update_many({"_id": {"$in": checked_tags}}, {"$push": {"songs": str(song["_id"])}})
    return redirect(url_for("songs.index", song_id=song["_id"]))


# Delete song
@routes.route("/<string:song_id>/delete", methods=["POST"])
def destroy(song_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    db.songs.delete_one({"_id": ObjectId(song_id), "user_id": user["_id"]})
    flash("Song deleted")
    return redirect(url_for('songs.index'))


# Edit song form
@routes.route("/<string:song_id>/edit/")
def edit(song_id):
    tags = db.tags.find()
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    if not ObjectId.is_valid(song_id):
        flash("Invalid song!")
        return redirect(url_for("songs.index"))

    song = db.songs.find_one({"_id": ObjectId(song_id), "user_id": user["_id"]})
    if not song:
        flash("That song does not exist!")
        return redirect(url_for("songs.index"))

    return render_template("songs/edit_song.html", song=song, tags=tags)


# Update song
@routes.route("/<string:song_id>/update/", methods=["POST"])
def update(song_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    if not ObjectId.is_valid(song_id):
        flash("Invalid song!")
        return redirect(url_for("songs.index"))

    song = db.songs.find_one({"_id": ObjectId(song_id)})
    if not song:
        flash("That song does not exist!")
        return redirect(url_for("songs.index"))

    db.songs.update_one({"_id": song["_id"]},
                        {"$set": {
                            "name": request.form.get("name"),
                            "artist": request.form.get("artist")
                        }})
    checked_tags = [ObjectId(tag) for tag in request.form.getlist("tags")]
    if checked_tags:
        db.tags.update_many({"_id": {"$in": checked_tags}}, {"$push": {"songs": str(song["_id"])}})

    return redirect(url_for("songs.show", song_id=song["_id"]))
