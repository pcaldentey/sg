import werkzeug


class ArtistNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Artist not found.'
