import functools
import re

from config import DEFAULT_COUNTRY

__all__ = ('fix_kwargs', 'set_id', 'is_available', 'get_available', 'search')

def fix_kwargs(function):
	@functools.wraps(function)
	def func(*args, **kwargs):
		assert(isinstance(kwargs, dict))
		kwargs = {str(k.replace('-', '_')): v for (k, v) in kwargs.items()}
		return function(*args, **kwargs)
	return func

def set_id(function):
	@functools.wraps(function)
	def func(*args, **kwargs):
		if 'href' in kwargs:
			kwargs['id']: kwargs['href'].split(':')[2]
		return function(*args, **kwargs)
	return func

def is_available(item, node=None):
	_item = item[node] if node else item
	if 'availability' in _item:
		territories = _item['availability']['territories']
		if (DEFAULT_COUNTRY in territories) or (territories == 'worldwide'):
			return item
		return False
	return item

def get_available(data, node=None):
	if not isinstance(data, (list, tuple)):
		return None
	return (i for i in data if is_available(i, node))

def search(query, data):
	sid = re.compile(r'^(?i)([a-z0-9]{22})$')
	lid = re.compile(r'^(?i)(spotify)\:(album|artist|track)\:([a-z0-9]{22})$')
	for i in data:
		if sid.match(query):
			if i.id == query: return i
		elif lid.match(query):
			if i.href == query: return i
		else:
			if i.name.lower() == query.lower(): return i
	return None
