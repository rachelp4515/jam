from flask import Blueprint, render_template, redirect, url_for, flash, request
from bson.objectid import ObjectId
import db

routes = Blueprint("tags", __name__, url_prefix="/tags")



#.....none of this has been remotly tested in anyway yet..... sh

# i just need to figure a few things out so that adding on the next feature doesnt take 
# ungodly amounts of time. The big thing is that tags needs to have a list of songs, instead 
# of songs having a list of tags. This makes sense when you think about how generating a playlist.
# I figured itd still be displayed like songs have a list of tags like when you view 
# one song itd have a list
# just needs to be back end stuff. msg me if this doesnt make sense bc it is a tad vital to the app




#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ index

@routes.route("/tags/")
def all_tags():
    tags = db.tags.find({})
    return render_template("all_tags.html", tags=tags) 

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ show one

@routes.route("/tags/<string:tag_id>/")
def show(tag_id):
    if not ObjectId.is_valid(tag_id):
        flash("Invalid tag!")
        return redirect(url_for("tags.all_tags"))

    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        flash("That tag does not exist!")
        return redirect(url_for("tags.all_tags"))
    return render_template("all_tags.html", tag=tag)

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ make new

@routes.route("/tags/new/")
def new():
    return render_template("new_tag.html")

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ post new

@routes.route("/", methods=["POST"])
def create():
    tag_title = request.form.get("title")

    if not tag_title:
        flash("Missing info!")
        return redirect(url_for("tags.new"))

    tag = {
        "name": tag_title,
    }
    db.tags.insert_one(tag)
    return redirect(url_for("tags.show", tag_id=tag["_id"]))

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ delete song

@routes.route("/<string:tag_id>/delete", methods=["POST"])
def destroy(tag_id):
    db.tags.delete_one({"_id": ObjectId(tag_id)})
    return "Deleted", 200

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ edit song

@routes.route("/<string:tag_id>/edit/")
def edit(tag_id):
    if not ObjectId.is_valid(tag_id):
        flash("Invalid tag!")
        return redirect(url_for("songs.index"))

    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        flash("That tag does not exist!")
        return redirect(url_for("tags.all_tags"))

    return render_template("edit_tag.html", tag=tag)


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_/ update song

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
                                "name": request.form.get("name"),
                                "artist": request.form.get("artist")
                            }})

    return redirect(url_for("tags.show", tag_id=tag["_id"]))
