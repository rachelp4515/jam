from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from bson.objectid import ObjectId
import db

routes = Blueprint("tags", __name__, url_prefix="/tags")





#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ index

@routes.route("/")
def all_tags():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
    tags = db.tags.find()
    songs = db.songs.find({"user_id": user["_id"]})
    return render_template("tags/all_tags.html", tags=tags, songs=songs) 

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ show one

@routes.route("/<string:tag_id>/")
def show(tag_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    if not ObjectId.is_valid(tag_id):
        flash("Invalid tag!")
        return redirect(url_for("tags.all_tags"))

    tag = db.tags.find_one({"_id": ObjectId(tag_id), "user_id": user["_id"]})
    if not tag:
        flash("That tag does not exist!")
        return redirect(url_for("tags.all_tags"))
    return render_template("tags/one_tag.html", tag=tag)

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ make new

@routes.route("/new/")
def new():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
    songs = db.songs.find()
    return render_template("tags/new_tag.html", songs= songs)

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ post new

@routes.route("/", methods=["POST"])
def create():
    tag_title = request.form.get("title")
    if not tag_title:
        flash("Missing info!")
        return redirect(url_for("tags.new"))

    tag = {
        # "song_id" : ObjectId(request.form.get('song_id')),
        "title": tag_title,
        "songs": request.form.getlist("songs")
    }
    songs = db.songs.find()
    db.tags.insert_one(tag)
    return redirect(url_for("tags.all_tags",song_id=request.form.get('song_id'), songs=songs))

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ delete tag

@routes.route("/<string:tag_id>/delete", methods=["POST"])
def destroy(tag_id):
    db.tags.delete_one({"_id": ObjectId(tag_id)})
    return redirect(url_for('tags.all_tags'))

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ edit tag

@routes.route("/<string:tag_id>/edit/")
def edit(tag_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))
        
    if not ObjectId.is_valid(tag_id):
        flash("Invalid tag!")
        return redirect(url_for("tags.index"))

    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        flash("That tag does not exist!")
        return redirect(url_for("tags.all_tags"))
    songs = db.songs.find({"user_id": user["_id"]})
    return render_template("tags/edit_tag.html", tag=tag, songs=songs, tags = db.tags.find())


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ update tag

@routes.route("/<string:tag_id>/update/", methods=["POST"])
def update(tag_id):
    if not ObjectId.is_valid(tag_id):
        flash("Invalid tag!")
        return redirect(url_for("tags.index"))

    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        flash("That tag does not exist!")
        return redirect(url_for("tags.index"))

    db.tags.update_one({"_id": tag["_id"]},
                            {"$set": {
                                "title": request.form.get("title"),
                                "songs": request.form.get("songs")
                            }})

    return redirect(url_for("tags.show", tag_id=tag["_id"]))
