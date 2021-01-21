from config.database import session
from config.database import Artist
from common.exceptions import PageNumberInvalid
from resources.resource import Resource


class ArtistResource(Resource):
    def artist_list(self, request):
        self._get_pagination_params(request)
        result = session.query(Artist).limit(self.size).offset(self.offset).all()

        # Checking pagination limits, is valid because of the type of query
        if int(len(result)) == 0:
            raise PageNumberInvalid()

        return {'data': [{'id': i.ArtistId, 'name': i.Name} for i in result],
                'meta': {
                        'page': self.page,
                        'size': self.size
                    }
                }
