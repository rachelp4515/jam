from flask import Blueprint, render_template, redirect, url_for, flash, request
from bson.objectid import ObjectId
import db

routes = Blueprint("playlists", __name__, url_prefix="/playlists")


@routes.route("/")
def index():
    playlists = db.playlists.find({})
    return render_template("playlists.html", playlists=playlists)


@routes.route("/<string:playlist_id>/")
def show(playlist_id):
    if not ObjectId.is_valid(playlist_id):
        flash("Invalid playlist!")
        return redirect(url_for("playlists.index"))

    playlist = db.playlists.find_one({"_id": ObjectId(playlist_id)})
    if not playlist:
        flash("That playlist does not exist!")
        return redirect(url_for("playlists.index"))
    return render_template("playlist.html", playlist=playlist)


@routes.route("/new/")
def new():
    return render_template("new_playlist.html")


@routes.route("/", methods=["POST"])
def create():
    playlist_name = request.form.get("name")
    playlist_description = request.form.get("description")

    playlist = {
        "user_id": "",
        "name": playlist_name,
        "description": playlist_description,
        "songs": []
    }
    db.playlists.insert_one(playlist)
    return redirect(url_for("playlists.show", playlist_id=playlist["_id"]))


@routes.route("/<string:playlist_id>", methods=["DELETE"])
def destroy(playlist_id):
    db.playlists.delete_one({"_id": ObjectId(playlist_id)})
    return "Deleted", 200
