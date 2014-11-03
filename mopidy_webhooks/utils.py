# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def send_webhook(config, payload):
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
