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

[meta]: https://developer.spotify.com/technologies/web-api/