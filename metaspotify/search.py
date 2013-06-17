from math import ceil

from config import API_HOST, API_SEARCH, API_VERSION
from connection import APICall
from base import Service
from util import is_available, get_available

__all__ = ('Search')

class Search(Service):

	def __init__(self, model):
		self.model = model
		self.url = ''.join([API_HOST, API_SEARCH.format(version=API_VERSION,
			model=model.res_name)])
	
	def search(self, query, page=1, **options):
		if query != '':
			query = ':'.join([self.model.res_name, query])

		if options and ('album' in options):
			album = ''.join(['album:', options['album']])
			query = ' '.join([album, query])

		if options and ('artist' in options):
			artist = ''.join(['artist:', options['artist']])
			query = ' '.join([artist, query])

		response = APICall.get(self.url, q=query.rstrip())
		info, result = Search._unwrap(response, self.model.wrapper)

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
				name = item['artists'][0]['name']
				href = item['artists'][0]['href']

				artists = [{'name':a, 'href':href} for a in name.split('/')]

				item['artists'] = artists

			for i in item['artists']:
				if i['name'].lower() == artist.lower():
					return item
		return False

	def is_exact(self, item, query):
		return item['name'].lower() == query.split(':')[1].lower()

	def pages(self, results, limit):
		return int(ceil(float(results) / float(limit)))