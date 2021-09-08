from __future__ import annotations

import logging

import pykka

from .reporters import events, status


logger = logging.getLogger(__name__)


class WebhookFrontend(pykka.ThreadingActor):
    def __init__(self, config, core):
        super().__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.status_reporter = None

    def on_start(self):
        self.event_reporter = events.EventReporter.start(self.config)

        if self.config["webhooks"]["status_update_interval"] > 0:
            self.status_reporter = status.StatusReporter.start(self.config, self.core)
        else:
            logger.info("Webhooks StatusReporter disabled by configuration.")

    def _stop_children(self):
        self.event_reporter.stop()

        if self.status_reporter:
            self.status_reporter.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
