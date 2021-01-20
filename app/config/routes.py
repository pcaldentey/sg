from http import HTTPStatus
from flask import Blueprint
from flask import jsonify
from flask import request

from endpoints.music.artists import ArtistResource

#from endpoints.music,artists import artists_resource

HEALTH_CHECK = '/_health-check'
ARTISTS = '/artists'
ALBUMS = '/albums'
COMPLETE = '/advanced'
ARTIST_ALBUMS = '/albums/<int:artist_id>'

health_check_api = Blueprint('health_check', __name__, url_prefix='/')
root_api = Blueprint('root', __name__, url_prefix='/')
artist_api = Blueprint('artists', __name__, url_prefix='/')
album_api = Blueprint('albums', __name__, url_prefix='/')
artist_album_api = Blueprint('artistalbums', __name__, url_prefix='/')
album_complete_api = Blueprint('albumscomplete', __name__, url_prefix=ALBUMS)

# List of albums, including artist name, track count, total album duration (sum of
# tracks duration), longest track duration and shortest track duration. (restricted
# to authenticated users) /albums/advanced
@album_complete_api.route(rule=COMPLETE, methods=['GET'])
def album_complete():
    return "artistss album complete list "


# List of albums for one artist /albums/%artist_id
@artist_album_api.route(rule=ARTIST_ALBUMS, methods=['GET'])
def artist_album(artist_id):
    return "artistss album  list {}".format(artist_id)


# List of artists (public endpoint) //artists
@artist_api.route(rule=ARTISTS, methods=['GET'])
def artists():
    resource = ArtistResource()
    return jsonify(resource.artist_list(request))

# List of albums with songs (restricted to authenticated users) /albums
@album_api.route(rule=ALBUMS, methods=['GET'])
def albums():
    return "albumss list "


@health_check_api.route(rule=HEALTH_CHECK)
def health_check():
    return "alive"


@root_api.route("/")
def hello():
    return "Hello World!"
