from flask import Blueprint, render_template, redirect, url_for, request, session
from bson.objectid import ObjectId
from flask_login import login_required
import db

routes = Blueprint("gen", __name__, url_prefix="/gen")


@routes.route("/")
def index():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
    tags = db.tags.find()
    songs = db.songs.find({"user_id": user["_id"]})
    return render_template("gen/create.html", tags=tags, songs=songs)


@routes.route("/create/", methods=["POST"])
def generate():
    tags = request.form.getlist("tags")
    if not request.form.get("length"):
        return redirect(url_for("gen.index"))

    song_num = int(request.form.get("length"))
    if song_num <= 0:
        return redirect(url_for("gen.index"))

    ids = [ObjectId(id) for id in tags]
    sampled_songs = list(db.tags.aggregate([
        {"$match": {"_id": {"$in": ids}}},
        {"$unwind": "$songs"},
        {"$sample": {"size": song_num}},
        {"$group": {"_id": None, "songs": {
            "$addToSet": {"$toObjectId": "$songs"},
        }}},
        {"$lookup": {
            "from": "songs",
            "localField": "songs",
            "foreignField": "_id",
            "as": "songs"
        }},
        {"$project": {
            "_id": 0,
            "songs": 1
        }}
    ]))[0]["songs"]
    return render_template("/gen/new_list.html", song_list=sampled_songs)
