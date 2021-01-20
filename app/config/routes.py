from flask import Blueprint
from flask import jsonify
from flask import request

from common.exceptions import ArtistNotFound
from common.exceptions import PassPhraseInvalid, PassPhraseNotFound
from config.database import Artist
from config.database import session
from endpoints.music.artists import ArtistResource
from endpoints.music.albums import AlbumResource
from endpoints.passphrase.passphrase import PassphraseResource


ARTISTS = '/artists'
ALBUMS = '/albums'
ADVANCED = '/advanced'
ARTIST_ALBUMS = '/artists/<int:artist_id>/albums'
PASSPHRASE = '/passphrase'
BASIC = '/basic'

root_api = Blueprint('root', __name__, url_prefix='/')
artist_api = Blueprint('artists', __name__, url_prefix='/')
album_api = Blueprint('albums', __name__, url_prefix='/')
artist_album_api = Blueprint('artistalbums', __name__, url_prefix='/')
album_complete_api = Blueprint('albumscomplete', __name__, url_prefix=ALBUMS)

pp_basic_api = Blueprint('passphrasebasic', __name__, url_prefix=PASSPHRASE)
pp_advanced_api = Blueprint('passphraseadvanced', __name__, url_prefix=PASSPHRASE)


@pp_basic_api.route(rule=BASIC, methods=['POST'])
def passphrase_basic():
    if 'passphrase' not in request.json \
            or request.json['passphrase'] is None:
        raise PassPhraseNotFound()


    resource = PassphraseResource(request)
    return jsonify(resource.basic())


@pp_basic_api.route(rule=ADVANCED, methods=['POST'])
def passphrase_advanced():
    if 'passphrase' not in request.json \
            or request.json['passphrase'] is None:
        raise PassPhraseNotFound()

    resource = PassphraseResource(request)
    return jsonify(resource.advanced())


# List of albums, including artist name, track count, total album duration (sum of
# tracks duration), longest track duration and shortest track duration. (restricted
# to authenticated users) /albums/advanced
@album_complete_api.route(rule=ADVANCED, methods=['GET'])
def album_complete():
    resource = AlbumResource()
    return jsonify(resource.album_advanced_list(request))


# List of albums for one artist (restricted to authenticated users) /artists/%artist_id/albums
@artist_album_api.route(rule=ARTIST_ALBUMS, methods=['GET'])
def artist_album(artist_id):
    exists = session.query(Artist).filter_by(ArtistId=artist_id).scalar() is not None
    if not exists:
        raise ArtistNotFound

    resource = AlbumResource()
    return jsonify(resource.artists_album_list(request, artist_id))


# List of artists (public endpoint) /artists
@artist_api.route(rule=ARTISTS, methods=['GET'])
def artists():
    resource = ArtistResource()
    return jsonify(resource.artist_list(request))


# List of albums with songs (restricted to authenticated users) /albums
@album_api.route(rule=ALBUMS, methods=['GET'])
def albums():
    resource = AlbumResource()
    return jsonify(resource.album_list(request))


@root_api.route("/")
def hello():
    return "Hello World!"
