import requests

from time import time

import config

__all__ = ('APICall')

cache = {}

class APICallException(Exception):
	pass

class APICall:

	@classmethod
	def get(cls, url, **kwargs):
		qs = ['{k}={v}'.format(k=k, v=v) for k, v in kwargs.iteritems()]
		cache_key = '?'.join([url, '&'.join(qs)])
		if cache_key not in cache:
			t1 = time()
			response = requests.get(url, params=kwargs, timeout=config.TIMEOUT)
			t2 = time()

			if response and config.TRACE_API_CALLS:
				print '{c}: {u} took {s:.4f}s.'.format(c=response.status_code,
					u=response.url, s=(t2 - t1))

			if response.status_code != 200:
				raise APICallException('{c}: could not load {u}: {r}'.format(
					c=response.status_code, u=response.url, r=response.text))

			cache[cache_key] = response

		return cache[cache_key]