import werkzeug


class ArtistNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Artist not found.'


class PassPhraseNotFound(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'passphrase parameter not found.'


class PassPhraseInvalid(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'passphrase parameter invalid.'
