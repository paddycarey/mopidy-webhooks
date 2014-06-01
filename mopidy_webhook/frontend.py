# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging
import time

# third-party imports
import pykka
import requests
from mopidy.core import CoreListener
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def _send_webhook(class_name, webhook_url, event=None, **kwargs):
    logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

    payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
    logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

    try:
        response = requests.post(webhook_url, data=payload)
    except Exception as e:
        logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
            class_name,
            e.__class__.__name__,
            e.message,
        ))
    else:
        logger.info('{0} Webhook Response Status: {1}'.format(class_name, response.status_code))
        logger.info('{0} Webhook Response Body: {1}'.format(class_name, response.text))


class StatusReporter(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(StatusReporter, self).__init__()
        self.config = config
        self.core = core
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.report_status()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def report_status(self):
        webhook_url = self.config['webhook']['webhook']
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': self.core.playback.state.get(),
            'time_position': self.core.playback.time_position.get(),
        }
        _send_webhook(self.__class__.__name__, webhook_url, **kwargs)
        time.sleep(2)
        self.in_future.report_status()


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core):
        super(EventReporter, self).__init__()
        self.config = config

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        webhook_url = self.config['webhook']['webhook'] + event + '/'
        _send_webhook(self.__class__.__name__, webhook_url, event, **kwargs)


class WebhookFrontend(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.status_reporter = None

    def on_start(self):
        self.event_reporter = EventReporter.start(self.config, self.core)
        self.status_reporter = StatusReporter.start(self.config, self.core)

    def _stop_children(self):
        self.event_reporter.stop()
        self.status_reporter.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
