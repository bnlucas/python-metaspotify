import requests

from time import time

from config import TIMEOUT, TRACE_API_CALLS

__all__ = ('APICall')

cache = {}

class APICallError(Exception):
	
	def __init__(self, status_code, url, text):
		message ='{c}: could not load {u}: {r}'.format(c=status_code, u=url,
			r=text)
		Exception.__init__(self, message)

class APICall:

	@classmethod
	def get(cls, url, **kwargs):
		qs = ['{k}={v}'.format(k=k, v=v) for k, v in kwargs.iteritems()]
		cache_key = '?'.join([url, '&'.join(qs)])
		if cache_key not in cache:
			t1 = time()
			response = requests.get(url, params=kwargs, timeout=TIMEOUT)
			t2 = time()

			if response and TRACE_API_CALLS:
				print '{c}: {u} took {s:.4f}s.'.format(c=response.status_code,
					u=response.url, s=(t2 - t1))

			if response.status_code != 200:
				raise APICallError(response.status_code, response.url,
					response.text)

			cache[cache_key] = response

		return cache[cache_key]
