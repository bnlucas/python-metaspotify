from config import API_HOST, API_LOOKUP, API_VERSION
from connection import APICall
from base import Service

__all__ = ('Lookup')


class Lookup(Service):

    url = ''.join([API_HOST, API_LOOKUP.format(version=API_VERSION)])

    @classmethod
    def by_id(cls, id, searcher):
        response = APICall.get(cls.url, uri=id)
        info, result = Lookup._unwrap(response, searcher.model.res_name)

        q = {'query': result['name']}

        if searcher.model.res_name == 'album':
            q.update({'artist': result['artist']})
        if searcher.model.res_name == 'artist':
            q.update({'exact': True})
        if searcher.model.res_name == 'track':
            q.update({'album': result['album']['name']})

        return searcher.search(**q)
