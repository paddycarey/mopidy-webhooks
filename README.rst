***************
Mopidy-Webhooks
***************

.. image:: https://img.shields.io/pypi/v/Mopidy-Webhooks.svg?style=flat
    :target: https://pypi.org/project/Mopidy-Webhooks
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Webhooks.svg?style=flat
    :target: https://pypi.org/project/Mopidy-Webhooks
    :alt: Number of PyPI downloads

.. image:: https://github.com/paddycarey/mopidy-webhooks/workflows/CI/badge.svg?branch=master
    :target: https://github.com/paddycarey/mopidy-webhooks/actions?query=branch%3Amaster+workflow%3ACI
    :alt: Github Actions CI build status


Mopidy-Webhooks is a frontend extension for `Mopidy <https://github.com/mopidy/mopidy>`_ that sends
webhook requests (regular JSON over HTTP POST requests) to a remote server. Mopidy-Webhooks sends a
webhook any time Mopidy core triggers an event, and also periodically sends player status updates to
the remote server.


Installation
============

Install by running::

    pip install Mopidy-Webhooks


Configuration
=============

Before starting Mopidy, you must add configuration for Mopidy-Webhooks to your Mopidy configuration file::

    [webhooks]
    webhook_url = http://localhost:8080/api/webhooks/ ; required
    api_key = my-api-key                              ; optional
    api_key_header_name = X-MOPIDY-WEBHOOKS-API-KEY   ; optional
    status_update_interval = 1000                     ; optional


``webhook_url`` should be a URL (accessible to the Mopidy server). The provided URL must accept HTTP
POST requests, the body of which will contain JSON data. Requests will contain either periodic
status updates (currently active track, playback state and time position) or JSON serialised event
data emitted by Mopidy core.

``api_key`` and ``api_key_header_name`` must both be specified together for the header to be sent.

``status_update_interval`` controls the interval between the sending of status update webhooks (in
milliseconds).
Set to `0` to disable the sending of periodic status updates. If you want continuous status updates,
just use a very very small value.


Project resources
=================

- `Source code <https://github.com/paddycarey/mopidy-webhooks>`_
- `Issue tracker <https://github.com/paddycarey/mopidy-webhooks/issues>`_
