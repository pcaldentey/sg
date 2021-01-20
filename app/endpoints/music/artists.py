from config.database import session
from config.database import Artist
from endpoints.resource import Resource


class ArtistResource(Resource):
    def artist_list(self, request):
        self._get_pagination_params(request)
        result = session.query(Artist).limit(self.size).offset(self.offset).all()
        return [{'id': i.ArtistId, 'name': i.Name} for i in result]
