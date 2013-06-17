
__all__ = ('BaseModel', 'Service')

class BaseModel:

	cache = {}

	def __str__(self):
		return self.name.encode('utf-8')

	def __cmp__(self, other):
		return cmp(self.id, other.id)

	@staticmethod
	def _load_artists(artists, searcher):
		def search_artist(name):
			return list(searcher.search(name, exact=True))[0]

		return [search_artist(i['name']) for i in artists]

	@staticmethod
	def _load_tracks(artists, album, searcher):
		q = {'query': '', 'album': album}
		def search_artist(name):
			q['artist'] = name
			return list(searcher.search(**q))

		tracks = []
		for i in artists:
			if i.name != 'Various Artists':
				tracks.extend(search_artist(i.name))

		return tracks

	@classmethod
	def from_json(cls, data):
		return cls(**data)

class Service:

	@staticmethod
	def _unwrap(data, wrapper):
		data = data.json()
		return data.get('info'), data.get(wrapper)