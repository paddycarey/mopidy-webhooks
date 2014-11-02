****************************
Mopidy-Webhooks
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Webhooks.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Webhooks/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Webhooks.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Webhooks/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/paddycarey/mopidy-webhooks/master.png?style=flat
    :target: https://travis-ci.org/paddycarey/mopidy-webhooks
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/paddycarey/mopidy-webhooks/master.svg?style=flat
   :target: https://coveralls.io/r/paddycarey/mopidy-webhooks?branch=master
   :alt: Test coverage


Mopidy-Webhooks is a frontend extension for mopidy that sends webhook requests (regular JSON over HTTP POST requests) to a remote server. Mopidy-Webhooks sends a webhook any time mopidy core triggers an event, and also periodically sends player status updates to the remote server.

This is very much a work in progress. Please treat it as such and file issues where appropriate.


Installation
============

Install by running::

    pip install Mopidy-Webhooks


Configuration
=============

Before starting Mopidy, you must add configuration for Mopidy-Webhooks to your Mopidy configuration file::

    [webhooks]
    api_key = my-api-key                              ; optional
    api_key_header_name = X-MOPIDY-WEBHOOKS-API-KEY   ; optional
    status_update_interval = 5                        ; optional
    webhook_url = http://localhost:8080/api/webhooks/ ; required

``api_key`` if present, will be sent as a HTTP header using the key ``X-API-KEY``.  If you'd rather use a different header name, this can be customised with the configuration value ``api_key_header_name``.

``status_update_interval`` controls the interval between the sending of status update webhooks (in milliseconds). Set to `0` to disable the sending of periodic status updates. If you want continuous status updates, just use a very very small value.

``webhook_url`` should be a URL (accessible to the mopidy client). The provided URL should accept HTTP POST requests, the body of which will contain JSON data. Requests will contain either periodic status updates (currently active track, playback state and time position) or JSON serialised event data emitted by Mopidy core.


Project resources
=================

- `Source code <https://github.com/paddycarey/mopidy-webhooks>`_
- `Issue tracker <https://github.com/paddycarey/mopidy-webhooks/issues>`_
- `Download development snapshot <https://github.com/paddycarey/mopidy-webhooks/archive/master.tar.gz#egg=Mopidy-Webhooks-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
