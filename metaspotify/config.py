
# Spotify Metadata API version. Currenlty `1`.
API_VERSION = 1

# Spotify Metedata API url.
API_HOST = 'http://ws.spotify.com'

# Spotify Metedata Search API uri.
API_SEARCH = '/search/{version}/{model}.json'

# Spotify Metedata Lookup API uri.
API_LOOKUP = '/lookup/{version}/.json'

# Default country, as certain tracks and albums are only available in certain
# areas of the world. DEFAULT_COUNTRY takes ISO 3166-1 alpha-2 country codes.
# See: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
DEFAULT_COUNTRY = 'US'

# API call timeout limit, in seconds.
TIMEOUT = 10

# Prints API requests in the console.
TRACE_API_CALLS = False
