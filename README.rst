****************************
Mopidy-Webhook
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Webhook.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Webhook/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Webhook.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Webhook/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/paddycarey/mopidy-webhook/master.png?style=flat
    :target: https://travis-ci.org/paddycarey/mopidy-webhook
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/paddycarey/mopidy-webhook/master.svg?style=flat
   :target: https://coveralls.io/r/paddycarey/mopidy-webhook?branch=master
   :alt: Test coverage

Mopidy webhook extension

This is very much a work in progress. Please treat it as such and file issues where appropriate.


Installation
============

Install by running::

    pip install Mopidy-Webhook


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Webhook to your Mopidy configuration file::

    [webhook]
    username = your_username
    password = your_password
    webhook = http://localhost:8080/webhook/

``username`` and ``password`` if present, will be encoded and sent as HTTP Basic Auth headers. ``webhook`` should be a URL (accessible to the mopidy client).

The provided URL should accept HTTP POST requests, of which the body will contain JSON.  Requests to the bare endpoint will contain periodic status updates (currently active track, playback state and time position). Requests will also be sent to a sub-URL that looks like ``<webhook_url><event_name>/`` which will contain JSON serialised event data emitted by Mopidy core.


Project resources
=================

- `Source code <https://github.com/paddycarey/mopidy-webhook>`_
- `Issue tracker <https://github.com/paddycarey/mopidy-webhook/issues>`_
- `Download development snapshot <https://github.com/paddycarey/mopidy-webhook/archive/master.tar.gz#egg=Mopidy-Webhook-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
