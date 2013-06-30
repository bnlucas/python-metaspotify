from config import API_HOST, API_LOOKUP, API_VERSION
from connection import APICall
from base import Service

__all__ = ('Lookup')


class Lookup(Service):

    url = ''.join([API_HOST, API_LOOKUP.format(version=API_VERSION)])

    @classmethod
    def by_id(cls, id, searcher):

        @searcher.cache.cache(timeout=searcher.cache_timeout)
        def api_call(url, id):
            response = APICall.get(url, uri=id)
            return Lookup._unwrap(response, searcher.model.res_name)

        info, result = api_call(cls.url, id=id)

        q = {'query': result['name']}

        if searcher.model.res_name == 'album':
            q.update({'artist': result['artist']})
        if searcher.model.res_name == 'artist':
            q.update({'exact': True})
        if searcher.model.res_name == 'track':
            q.update({'album': result['album']['name']})

        return searcher.search(**q)
