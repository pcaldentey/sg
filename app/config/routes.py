from http import HTTPStatus
from flask import Blueprint


from config.database import session
from config.database import Artist

HEALTH_CHECK = '/_health-check'

health_check_api = Blueprint('health_check', __name__, url_prefix='/')
root_api = Blueprint('root', __name__, url_prefix='/')


@health_check_api.route(rule=HEALTH_CHECK)
def health_check():
    return "alive"


@root_api.route("/")
def hello():
    result = session.query(Artist).all()
    return "Hello World!"
