# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def _send_webhook(config, payload):
    """Sends a HTTP request to the configured server.

    All exceptions are suppressed but emit a warning message in the log.
    """
    try:
        response = requests.post(
            config['webhook_url'],
            data=json.dumps(payload, cls=ModelJSONEncoder),
            headers={config['api_key_header_name']: config['api_key']},
        )
    except Exception as e:
        logger.warning('Unable to send webhook: ({1}) {2}'.format(
            e.__class__.__name__,
            e.message,
        ))
    else:
        logger.debug('Webhook response: ({0}) {1}'.format(
            response.status_code,
            response.text,
        ))


class ReporterMixin(object):
    """Mixin that provides common reporter functionality
    """
    def on_start(self):
        logger.info('{0} started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} stopped.'.format(self.__class__.__name__))

    def send_webhook(self, payload):
        """Given a serializable object, encode `data` as JSON and send to
        remote server using a HTTP POST request.
        """
        _send_webhook(self.config, payload)
