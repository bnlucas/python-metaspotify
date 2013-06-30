import hashlib

from functools import wraps
from time import time

try:
    import cPickle as pickle
except ImportError:
    import pickle


class SimpleCache():

    def __init__(self, threshold=500, default_timeout=300):
        self._cache = {}
        self.clear = self._cache.clear
        self._threshold = threshold
        self.default_timeout = default_timeout

    def _prune(self):
        if len(self._cache) > self._threshold:
            now = time()
            for i, (key, (expires, _)) in enumerate(self._cache.items()):
                if (expires <= now) or (i % 3 == 0):
                    self._cache.pop(key, None)

    def get(self, key):
        expires, value = self._cache.get(key, (0, None))
        if expires > time():
            return pickle.loads(value)

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        self._prune()
        self._cache[key] = (time() + timeout), pickle.dumps(
            value, pickle.HIGHEST_PROTOCOL)

    def cache(self, timeout=None):
        def wrapper(function):
            @wraps(function)
            def func(*args, **kwargs):
                cache_key = hashlib.md5()
                key = '{f}_{a}_{k}'.format(
                    f=function.__name__,
                    a='_'.join(v.encode('utf-8') for v in args),
                    k='_'.join(v.encode('utf-8') for (k, v) in kwargs.items())
                )
                cache_key.update(key)
                cache_key = cache_key.digest().encode('base64')[:16]
                rv = self.get(cache_key)
                if rv is None:
                    rv = function(*args, **kwargs)
                    self.set(cache_key, rv, timeout)
                return rv
            return func
        return wrapper
