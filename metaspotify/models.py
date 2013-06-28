from base import BaseModel
from search import Search
from util import fix_kwargs, search, set_id

__all__ = ('Album', 'Artist', 'Track')


class Album(BaseModel):

    res_name = 'album'
    wrapper = 'albums'

    @fix_kwargs
    @set_id
    def __init__(self, name, **kwargs):
        self.name = name

        kwargs['artists'] = self._load_artists(
            kwargs['artists'], Search(Artist))

        self.__dict__.update(kwargs)

    def track(self, track):
        return search(track, self.tracks)

    @property
    def tracks(self):
        if 'tracks' not in self.cache:
            tracks = self._load_tracks(self.artists, self.name, Search(Track))

            self.cache['tracks'] = sorted(
                tracks, key=lambda t: int(t.track_number))

        return self.cache['tracks']

    def __repr__(self):
        if self.artists[0].name == 'Various Artists':
            artist = self.artists[0]['name']
        else:
            artist = ', '.join([i.name.encode('utf-8') for i in self.artists])

        album = self.name.encode('utf-8')
        return '<Album - {artist}: {album}>'.format(artist=artist, album=album)


class Artist(BaseModel):

    res_name = 'artist'
    wrapper = 'artists'

    @fix_kwargs
    @set_id
    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<Artist - {name}>'.format(name=self.name.encode('utf-8'))

    def album(self, album):
        return search(album, self.albums)

    @property
    def albums(self):
        if 'albums' not in self.cache:
            self.cache['albums'] = Search(Album).search('', artist=self.name)

        return self.cache['albums']


class Track(BaseModel):

    res_name = 'track'
    wrapper = 'tracks'

    @fix_kwargs
    @set_id
    def __init__(self, name, **kwargs):
        self.name = name

        kwargs['artists'] = self._load_artists(
            kwargs['artists'], Search(Artist))

        self.__dict__.update(kwargs)

    def __repr__(self):
        if self.artists[0].name == 'Various Artists':
            artist = self.artists[0]['name']
        else:
            artist = ', '.join([i.name.encode('utf-8') for i in self.artists])
        track = self.name.encode('utf-8')
        return '<Track - {artist}: {track}>'.format(artist=artist, track=track)
