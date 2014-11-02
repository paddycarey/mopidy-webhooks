# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from . import base


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener, base.BaseReporter):

    def __init__(self, config):
        super(EventReporter, self).__init__()
        self.config = config['webhooks']

    def on_event(self, event, **kwargs):
        self.send_webhook({event: kwargs})
