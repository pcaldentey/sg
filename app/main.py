from flask import Flask

from config import routes

app = Flask(__name__)
app.register_blueprint(routes.health_check_api)
app.register_blueprint(routes.root_api)




if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
