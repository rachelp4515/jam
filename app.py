import os

from flask import Flask
from blueprints.main import routes as main_routes
from blueprints.playlists import routes as playlist_routes

app = Flask(__name__)

app.register_blueprint(main_routes)
app.register_blueprint(playlist_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 3000))
