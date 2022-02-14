from flask import Blueprint, render_template, redirect, url_for, flash, request
from bson.objectid import ObjectId
import db

routes = Blueprint("songs", __name__, url_prefix="/songs")


@routes.route("/")
def index():
    songs = db.songs.find({})
    return render_template("library.html", songs=songs)


@routes.route("/<string:song_id>/")
def show(song_id):
    if not ObjectId.is_valid(song_id):
        flash("Invalid song!")
        return redirect(url_for("songs.index"))

    song = db.songs.find_one({"_id": ObjectId(song_id)})
    if not song:
        flash("That song does not exist!")
        return redirect(url_for("songs.index"))
    return render_template("song.html", song=song)


@routes.route("/new/")
def new():
    return render_template("new_song.html")


@routes.route("/", methods=["POST"])
def create():
    song_name = request.form.get("name")
    song_artist = request.form.get("artist")

    if not song_name or not song_artist:
        flash("Missing info!")
        return redirect(url_for("songs.new"))

    song = {
        "name": song_name,
        "artist": song_artist
    }
    db.songs.insert_one(song)
    return redirect(url_for("songs.show", song_id=song["_id"]))


@routes.route("/<string:song_id>/delete", methods=["POST"])
def destroy(song_id):
    db.songs.delete_one({"_id": ObjectId(song_id)})
    return "Deleted", 200


@routes.route("/<string:song_id>/edit/")
def edit(song_id):
    if not ObjectId.is_valid(song_id):
        flash("Invalid song!")
        return redirect(url_for("songs.index"))

    song = db.songs.find_one({"_id": ObjectId(song_id)})
    if not song:
        flash("That song does not exist!")
        return redirect(url_for("songs.index"))

    return render_template("edit_song.html", song=song)


@routes.route("/<string:song_id>/update/", methods=["POST"])
def update(song_id):
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

    return redirect(url_for("songs.show", song_id=song["_id"]))
