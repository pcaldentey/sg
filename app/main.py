from flask import Flask
from flask import json
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.exceptions import HTTPException

from common.authentication import authenticate, identity
from config import constants
from config import routes

app = Flask(__name__)
app.config['SECRET_KEY'] = constants.SECRET_KEY

app.register_blueprint(routes.root_api)
app.register_blueprint(routes.artist_api)
app.register_blueprint(routes.album_api)

# passphrase endpoints
app.register_blueprint(routes.pp_api)

jwt = JWT(app, authenticate, identity)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
