memcached client for asyncio
============================

asyncio (PEP 3156) library to work with memcached.

.. image:: https://travis-ci.org/aio-libs/aiomcache.svg?branch=master
   :target: https://travis-ci.org/aio-libs/aiomcache


Getting started
---------------

The API looks very similar to the other memcache clients:

.. code:: python

    import asyncio
    import aiomcache

    loop = asyncio.get_event_loop()

    async def hello_aiomcache():
        mc = aiomcache.Client("127.0.0.1", 11211, loop=loop)
        await mc.set(b"some_key", b"Some value")
        value = await mc.get(b"some_key")
        print(value)
        values = await mc.multi_get(b"some_key", b"other_key")
        print(values)
        await mc.delete(b"another_key")

    loop.run_until_complete(hello_aiomcache())


Requirements
------------

- Python >= 3.3
- asyncio https://pypi.python.org/pypi/asyncio/

CHANGES
=======

0.6.0 (2017-12-03)
------------------

- Drop python 3.3 support

0.5.2 (2017-05-27)
------------------

- Fix issue with pool concurrency and task cancellation

0.5.1 (2017-03-08)
------------------

- Added MANIFEST.in

0.5.0 (2017-02-08)
------------------

- Added gets and cas commands

0.4.0 (2016-09-26)
------------------

- Make max_size strict #14

0.3.0 (2016-03-11)
------------------

- Dockerize tests

- Reuse memcached connections in Client Pool #4

- Fix stats parse to compatible more mc class software #5

0.2 (2015-12-15)
----------------

- Make the library Python 3.5 compatible

0.1 (2014-06-18)
----------------

- Initial release

