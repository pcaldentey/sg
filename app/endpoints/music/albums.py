from config.database import session
from config.database import Album
from endpoints.resource import Resource


class AlbumResource(Resource):
    def album_list(self, request):
        self._get_pagination_params(request)

        # We paginate result around album table. A bit tricky but just in one query
        query = ("SELECT tr.Name, tr.AlbumId, alb.Title FROM tracks AS tr, (select AlbumId, Title from albums order by "
                 "AlbumId limit {limit} offset {offset}) AS alb WHERE tr.AlbumId = alb.AlbumId ORDER BY tr.AlbumId"
                 ).format(limit=self.size, offset=self.offset)
        result = session.execute(query)

        return [{'Album': key, 'tracks': value} for key, value in self._group_albums(result).items()]

    def _group_albums(self, rows):
        albums = {}
        for i in rows:
            if i.Title in albums:
                albums[i.Title].append(i.Name)
            else:
                albums[i.Title] = [i.Name]
        return albums
