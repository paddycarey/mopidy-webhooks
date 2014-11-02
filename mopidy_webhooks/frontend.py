# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka

# local imports
from .reporters import events
from .reporters import status

logger = logging.getLogger(__name__)


class WebhookFrontend(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.status_reporter = None

    def on_start(self):
        self.event_reporter = events.EventReporter.start(self.config)
        self.status_reporter = status.StatusReporter.start(self.config, self.core)

    def _stop_children(self):
        self.event_reporter.stop()
        self.status_reporter.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
