from __future__ import annotations

import logging

import pykka
from mopidy.core import CoreListener

from mopidy_webhooks.utils import send_webhook


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener):
    def __init__(self, config):
        super().__init__()
        self.config = config["webhooks"]

    def on_start(self):
        logger.info("Webhooks EventReporter started.")

    def on_event(self, event, **kwargs):
        payload = {
            "type": "event",
            "event": event,
            "data": kwargs,
        }
        send_webhook(self.config, payload)
