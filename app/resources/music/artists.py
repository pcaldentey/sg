from config.database import session
from config.database import Artist
from resources.resource import Resource


class ArtistResource(Resource):
    def artist_list(self, request):
        self._get_pagination_params(request)
        result = session.query(Artist).limit(self.size).offset(self.offset).all()
        return {'data': [{'id': i.ArtistId, 'name': i.Name} for i in result],
                'meta': {
                        'page': self.page,
                        'size': self.size
                    }
                }
