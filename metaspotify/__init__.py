<<<<<<< HEAD
=======
import re

from lookup import Lookup
from search import Search

from models import *

__all__ = ('api')


class SpotifyIDError(ValueError):

    def __init__(self, id):
        message = '{id} is not a valid Spotify ID.'.format(id=id)
        ValueError.__init__(self, message)


class api:

    def __init__(self, cache_function=None, cache_arguments={}):
        self.album = Search(Album, cache_function, cache_arguments)
        self.artist = Search(Artist, cache_function, cache_arguments)
        self.track = Search(Track, cache_function, cache_arguments)

        self.cache_function = cache_function
        self.cache_arguments = cache_arguments

    @classmethod
    def lookup_id(cls, id):
        try:
            model = cls.validate_id(id)
        except SpotifyIDError:
            raise

        search = cls.__dict__[model]

        return Lookup.by_id(
            id, search, self.cache_function, self.cache_arguments)

    @staticmethod
    def validate_id(id):
        e = re.compile(r'^(?i)spotify:(album|artist|track):[a-z0-9]{22}$')
        r = e.search(id)
        if r:
            return r.groups()[0]
        raise SpotifyIDError(id)
>>>>>>> 0.9.0
