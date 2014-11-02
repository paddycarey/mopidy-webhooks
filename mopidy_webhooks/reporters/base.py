# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def _send_webhook(api_key_header_name, api_key, webhook_url, data):
    logger.debug('Webhook URL: {0}'.format(webhook_url))
    headers = {api_key_header_name: api_key}
    logger.debug('Webhook headers: {0}'.format(json.dumps(headers)))
    payload = json.dumps(data, cls=ModelJSONEncoder)
    logger.debug('Webhook data: {0}'.format(json.dumps(payload)))
    try:
        response = requests.post(webhook_url, data=payload, headers=headers)
    except Exception as e:
        logger.warning('Unable to send webhook: ({1}) {2}'.format(
            e.__class__.__name__,
            e.message,
        ))
    else:
        logger.debug('Webhook Response Status: {0}'.format(response.status_code))
        logger.debug('Webhook Response Body: {0}'.format(response.text))


class BaseReporter(object):

    def on_start(self):
        logger.info('{0} started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} stopped.'.format(self.__class__.__name__))

    def send_webhook(self, data):
        api_key = self.config['api_key']
        api_key_header_name = self.config['api_key_header_name']
        webhook_url = self.config['webhook_url']
        _send_webhook(api_key_header_name, api_key, webhook_url, data)
