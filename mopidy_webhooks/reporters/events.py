# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from ..utils import send_webhook


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config):
        super(EventReporter, self).__init__()
        self.config = config['webhooks']

    def on_start(self):
        logger.info('EventReporter started.')

    def on_event(self, event, **kwargs):
        send_webhook(self.config, {event: kwargs})
