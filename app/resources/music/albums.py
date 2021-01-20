from config.database import session
from config.database import Album
from config.database import Artist
from resources.resource import Resource


class AlbumResource(Resource):
    def album_list(self, request):
        """ List of albums with songs """
        self._get_pagination_params(request)

        # We paginate result around album table. A bit tricky but just in one query
        query = ("SELECT tr.Name, tr.AlbumId, alb.Title FROM tracks AS tr, (select AlbumId, Title from albums order by "
                 "AlbumId limit {limit} offset {offset}) AS alb WHERE tr.AlbumId = alb.AlbumId ORDER BY tr.AlbumId"
                 ).format(limit=self.size, offset=self.offset)
        result = session.execute(query)

        return {'data': [{'album': key, 'tracks': value} for key, value in self._group_by_album(result).items()]}

    def _group_by_album(self, rows):
        """ Group track in their album """
        albums = {}
        for i in rows:
            if i.Title in albums:
                albums[i.Title].append(i.Name)
            else:
                albums[i.Title] = [i.Name]
        return albums

    def artists_album_list(self, request, artist_obj):
        """ List of albums for one artist """
        result = session.query(Album).join(Artist).filter(Artist.ArtistId == artist_obj.ArtistId)
        artist_name = artist_obj.Name

        return {'artist name': artist_name, 'albums': [i.Title for i in result]}

    def album_advanced_list(self, request):
        """
        List of albums, including artist name, track count, total album duration (sum of
        tracks duration), longest track duration and shortest track duration. (restricted
        to authenticated users)
        """
        self._get_pagination_params(request)

        query = ("SELECT albums.AlbumId, albums.Title, artists.Name, MIN(tracks.Milliseconds) as shortest,"
                 "MAX(tracks.Milliseconds) longest, SUM(tracks.Milliseconds) total "
                 "FROM albums JOIN artists ON albums.ArtistId = artists.ArtistId "
                 "JOIN tracks ON albums.AlbumId = tracks.AlbumId "
                 "GROUP BY albums.AlbumId, albums.Title, artists.Name ORDER BY albums.AlbumId "
                 "limit {limit} offset {offset}"
                 ).format(limit=self.size, offset=self.offset)
        result = session.execute(query)

        return {'data': [
                    {'album': row.Title,
                     'artist': row.Name,
                     'total duration': row.total,
                     'longest duration': row.longest,
                     'shortest duration': row.shortest} for row in result]
                }
