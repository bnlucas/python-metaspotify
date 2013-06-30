MetaSpotify
===========
Python wrapper for the [Spotify metadata API][sm]

The Spotify metadata API limitations are 10 requests per second per IP. Spotify
pushes use of a `If-Modified-Since` header using the original request's
`Last-Modified` header. See [Spotify's Caching][sc] requests for more
information. As this would require a backend to store this information, and with
most applications already having a caching system implemented, MetaSpotify takes
the caching function as an argument within `metaspotify.api()` to cache these
results, not store them.

```python
import metaspotify

ms = metaspotify.api() # Without any parameters, the MetaSpotify SimpleCache is
                       # loaded.
```
```python
# This is an example of using Flask-Cache with MetaSpotify inside a Flask app.
from flask import Flask
from flask_cache import Cache

app = Flask('application')
cache = Cache(app)

# ...

ms = metaspotify.api(
    cache_function=cache.memoize, cache_arguments={'timeout': 60})

# Works like @cache.memoize(timeout=60)
```

What the example using [Flask-Cache][fc] does is tell MetaSpotify to use the
`cache.memoize` decorator with `kwargs` `timeout=60`. MetaSpotify calls a given
decorator, as most caching libraries use decorators for this.

The caching functions are called within [search][ms] and [lookup][ml]

----------------------

US Spotify metadata for: `spotify:album:3O8Z8r9OcvUJjJCx4be4Xf`
- album `Final Noise`, artists `[Eisley, Simon Dawes, Timmy Curran]`

```python
results = ms.album.search('final noise', artist='timmy curran')

for result in results: # returns generator expression
	for track in result.tracks:
		print track.track_number, ':', track.name # '# : Track'
```

Output:

```
1 : Escaping Song - Non-Album Track
2 : They All Surrounded Me - Non-Album Track
3 : If You Were A Girl - EP Version
4 : The Awful Things - EP Version
5 : Comatose
6 : Blue Eyes
```

Spotify metadata for: `spotify:artist:4DBi4EYXgiqbkxvWUXUzMi`
- artist `Old Crow Medicine Show`

```python
results = ms.artist.search('old crow medicine show', exact=True)

for result in results: # returns generator expression
	for album in result.albums:
		print result.name, '-', album.name # 'Artist - Album'
```

Output:

```
Old Crow Medicine Show - O.C.M.S.
Old Crow Medicine Show - Carry Me Back
Old Crow Medicine Show - Tennessee Pusher
Old Crow Medicine Show - Big Iron World
Old Crow Medicine Show - World Cafe Old Crow Medicine Show - EP
Old Crow Medicine Show - Caroline - EP
Old Crow Medicine Show - Down Home Girl - EP
```

US Spotify metadata for: `spotify:track:7AvbfnZNXylSfjDgFG5vyW`
- `04. Wooden Heart`, album `Wooden Heart`, artist `Listener`

```python
results = ms.track.search('wooden heart', artist='listener',
	album='wooden heart')

for result in results: # returns generator expression
	print result.popularity # 0.46726
```

Output:

```
0.46726
```

US metadata using SpotifyID for: `spotify:track:59KXRDb8kuoRjG5oRTEHgK`
- `08. Letter From Omaha`, album `Josh Ritter`, artist `Josh Ritter`

```python
results = ms.lookup_id('spotify:track:59KXRDb8kuoRjG5oRTEHgK')

for result in results: # returns generator expression
	print result.length # 189.472
```

Output:

```
189.472
```

[sm]: https://developer.spotify.com/technologies/web-api/
[sc]: https://developer.spotify.com/technologies/web-api/#caching
[fc]: http://pythonhosted.org/Flask-Cache/
[ms]: https://github.com/bnlucas/python-metaspotify/blob/master/metaspotify/search.py
[ml]: https://github.com/bnlucas/python-metaspotify/blob/master/metaspotify/lookup.py
