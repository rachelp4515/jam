from flask import Blueprint, render_template
import db

routes = Blueprint("main", __name__)


@routes.route("/")
def index():
    tags = db.tags.find()
    return render_template("index.html", tags=tags)
