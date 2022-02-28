import imp
import os

from flask import Flask
from blueprints.main import routes as main_routes
from blueprints.songs import routes as songs_routes
from blueprints.users import routes as user_routes
from blueprints.tags import routes as tag_routes

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(6))

app.register_blueprint(main_routes)
app.register_blueprint(songs_routes)
app.register_blueprint(user_routes)
app.register_blueprint(tag_routes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 3000))
