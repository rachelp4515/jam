from flask import Blueprint, render_template

routes = Blueprint("playlists", __name__, url_prefix="/playlists")


@routes.route("/")
def index():
    return render_template("playlists.html")


@routes.route("/<string:id>")
def show(playlist_id):
    return render_template("playlist.html")


@routes.route("/new")
def new():
    return render_template("new_playlist.html")


@routes.route("/", methods=["POST"])
def create():
    return "Create playlist"
