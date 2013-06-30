from math import ceil

from cache import SimpleCache
from config import API_HOST, API_SEARCH, API_VERSION
from connection import APICall
from base import Service
from util import get_available

__all__ = ('Search')


class Search(Service):

    def __init__(self, model, cache_function, cache_arguments):
        self.model = model

        self.cache_function = cache_function
        if self.cache_function is None:
            cache = SimpleCache()
            self.cache_function = cache.cache
        self.cache_arguments = cache_arguments

        self.url = ''.join([API_HOST, API_SEARCH.format(
            version=API_VERSION, model=model.res_name)])

    def search(self, query, page=1, **options):

        @self.cache_function(**self.cache_arguments)
        def api_call(url, query):
            response = APICall.get(url, q=query)
            return Search._unwrap(response, self.model.wrapper)

        if query != '':
            query = ':'.join([self.model.res_name, query])

        if options and ('album' in options):
            album = ''.join(['album:', options['album']])
            query = ' '.join([album, query])

        if options and ('artist' in options):
            artist = ''.join(['artist:', options['artist']])
            query = ' '.join([artist, query])

        info, result = api_call(self.url, query=query.rstrip())

        if options and ('pages' in options):
            return self.pages(info['num_results'], info['limit'])

        if self.model.res_name == 'track':
            result = get_available(result, 'album')
        else:
            result = get_available(result)

        if options:
            if 'album' in options:
                album = options['album']
                result = (i for i in result if self.is_album(i, album))
            if 'artist' in options:
                artist = options['artist']
                result = (i for i in result if self.is_artist(i, artist))
            if ('exact' in options) and (self.model.res_name == 'artist'):
                result = (i for i in result if self.is_exact(i, query))

        return (self.model.from_json(i) for i in result)

    def is_album(self, item, album):
        if 'album' in item:
            if item['album']['name'].lower() == album.lower():
                return item
        return False

    def is_artist(self, item, artist):
        if 'artists' in item:
            if '/' in item['artists'][0]['name']:
                names = item['artists'][0]['name'].split('/')
                href = item['artists'][0]['href']

                artists = [{'name': i, 'href': href} for i in names]

                item['artists'] = artists

            for i in item['artists']:
                if i['name'].lower() == artist.lower():
                    return item
        return False

    def is_exact(self, item, query):
        return item['name'].lower() == query.split(':')[1].lower()

    def pages(self, results, limit):
        return int(ceil(float(results) / float(limit)))
