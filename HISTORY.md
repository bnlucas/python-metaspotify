0.9.0 (2013-06-30)
==================

- Added cache.py, SimpleCache.

- This was a big jump from 0.2.0. Most of the code has stayed the same after
  trying different cache methods. Settled on a simplified version of the
  [Flask-Cache][fc] and [Werkzeug][wz] SimpleCache modules. I am a great fan of
  these two packages, as they cover a wide range of caching methods. I'd like to
  implement a form of this within MetaSpotify, but the [Werkzeug][wz] is far to
  large for this simple of a package.

- Moving towards implementing existing caching libraries over adding one for
  MetaSpotify. For instance, if an application utilizing MetaSpotify is built on
  [Flask][fl] and [Flask-Cache][fc], allow the use of [Flask-Cache][fc].

- One step closer to adding outside cache support, one step to v1.0.0 and push
  to the master branch.

0.2.0 (2013-06-28)
==================

- PEP8 compliance. Preparing for caching system backend. I chose to go with PEP8
  because it forces you to write better code. The SublimeLinter Python support
  really helps with this.

- Caching backends in consideration. Something small, light, easy to configure/
  extend.

0.1.0 (2013-06-16)
==================

- Released code to GitHub repository python-metaspotify
  https://github.com/bnlucas/python-metaspotify/tree/0.1.0

0.0.1 (2013-06-09)
==================

- Initialization


[fc]: http://pythonhosted.org/Flask-Cache/
[wz]: http://werkzeug.pocoo.org/
[fl]: http://flask.pocoo.org/
