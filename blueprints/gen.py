from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from bson.objectid import ObjectId
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


#----------------------------------------------/ CREATE

@routes.route("/create/", methods=["POST"])
def generate():
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

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
    plist = {
        "user_id": user["_id"],
        'name': '',
        'desc': '',
        'songs': sampled_songs,
    }
    
    db.playlists.insert_one(plist)
    print(plist, '-------------------------')

    return render_template("/gen/new_list.html", song_list=sampled_songs, list=plist)


# #----------------------------------------------/ SAVE

# @routes.route('/create/save/', methods=['GET', 'POST'])
# def save(list_id):
#     user = db.users.find_one({"name": session.get("username")})
#     if not user:
#         return redirect(url_for("users.login"))

#     list = db.playlists.find_one({"_id": ObjectId(list_id), "user_id": user["_id"]})
#     if not list:
#         flash("List Not Found")
#         return redirect(url_for('gen.index'))
#     return redirect(url_for('gen.index', list_id=list['_id']))


#----------------------------------------------/ ADD

@routes.route('/<string:list_id>/add', methods=['POST'])
def add(list_id):
    user = db.users.find_one({"name": session.get("username")})
    if not user:
        return redirect(url_for("users.login"))

    plist = db.playlists.find_one({"_id": ObjectId(list_id)})
    print('-------------------------------------')
    db.playlists.update_one({'_id': plist["_id"]},
                            {"$set":{
                                 "name": request.form.get("name"),
                                 "desc": request.form.get('desc')
                             }})
    return render_template('/gen/all_list.html', list=plist)



#----------------------------------------------/ DELETE

@routes.route("/<string:list_id>/delete", methods=["POST"])
def delete(list_id):
    db.playlists.delete_one({"_id": ObjectId(list_id)})
    return render_template('gen/all_list.html', list=db.playlists.find())
