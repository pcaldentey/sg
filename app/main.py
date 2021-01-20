from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import database


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
