import re

from lookup import Lookup
from search import Search

from models import *

class SpotifyIDError(ValueError):

	def __init__(self, id):
		message = '{id} is not a valid Spotify ID.'.format(id=id)
		ValueError.__init__(self, message)

class api:

	album  = Search(Album)
	artist = Search(Artist)
	track  = Search(Track)

	@classmethod
	def lookup_id(cls, id):
		try:
			_, model, sid = cls.validate_id(id)
		except SpotifyIDError:
			raise

		search = cls.__dict__[model]

		return Lookup.by_id(id, search)

	@classmethod
	def validate_id(cls, id):
		e = re.compile(r'^(?i)(spotify)\:(album|artist|track)\:([a-z0-9]{22})$')
		r = e.search(id)
		if r:
			return r.groups()
		raise SpotifyIDError(id)