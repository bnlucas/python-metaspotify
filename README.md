MetaSpotify
===========
Python wrapper for the [Spotify metadata API][meta]

```python
import metaspotify
ms = metaspotify.api()
```

US Spotify metadata for: `spotify:album:3O8Z8r9OcvUJjJCx4be4Xf`
- album `Final Noise`, artists `[Eisley, Simon Dawes, Timmy Curran]`

```python
results = ms.album.search('final noise', artist='timmy curran')

for result in results: # returns generator expression
	for track in result.tracks:
		print track.track_number, ':', track.name # '# : Name'
```

Spotify metadata for: `spotify:artist:4DBi4EYXgiqbkxvWUXUzMi`
- artist `Old Crow Medicine Show`

```python
results = ms.artist.search('old crow medicine show', exact=True)

for result in results: # returns generator expression
	for album in result.albums:
		print result.name, '-', album.name # 'Artist - Album'
```

US Spotify metadata for: `spotify:track:7AvbfnZNXylSfjDgFG5vyW`
- `04. Wooden Heart`, album `Wooden Heart`, artist `Listener`

```python
results = ms.track.search('wooden heart', artist='listener',
	album='wooden heart')

for result in results: # returns generator expression
	print result.popularity # 0.46726
```

US metadata using SpotifyID for: `spotify:track:59KXRDb8kuoRjG5oRTEHgK`
- `08. Letter From Omaha`, album `Josh Ritter`, artist `Josh Ritter`

```python
results = ms.lookup_id('spotify:track:59KXRDb8kuoRjG5oRTEHgK')

for result in results: # returns generator expression
	print result.length # 189.472
```


[meta]: [https://developer.spotify.com/technologies/web-api/]