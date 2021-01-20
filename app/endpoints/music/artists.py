from config.database import session
from config.database import Artist
from config import constants


class ArtistResource():
    def _get_pagination_params(self, request):
        page = request.args.get('page')
        size = request.args.get('size')

        self.page = page if page else constants.PAGE_NUMBER
        self.size = size if size else constants.PAGE_SIZE
        self.offset = int(self.page) * int(self.size)

    def artist_list(self, request):
        self._get_pagination_params(request)
        result = session.query(Artist).limit(self.size).offset(self.offset).all()
        return [{'id': i.ArtistId, 'name': i.Name} for i in result]
