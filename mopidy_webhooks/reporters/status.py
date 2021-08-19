from __future__ import annotations

import logging
import time

import pykka

from mopidy_webhooks.utils import send_webhook


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor):
    """Periodically sends webhook notifications to the configured server
    containing data on the player's current status.
    """

    def __init__(self, config, core):
        super().__init__()
        self.config = config["webhooks"]
        self.core = core
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        """Runs when the actor is started and schedules a status update"""
        logger.info("Webhooks StatusReporter started.")

        self.in_future.report_status()

    def report_again(self, playback_state):
        """Computes a sleep interval, sleeps for the specified amount of time
        then kicks off another status report.
        """
        # Calculate sleep interval based on current playback state and configured interval.
        _m = {"playing": 1, "paused": 2, "stopped": 5}[playback_state]
        interval = (self.config["status_update_interval"] * _m) / 1000.0

        # Sleep for computed interval, then kickoff another webhook.
        time.sleep(interval)
        self.in_future.report_status()

    def report_status(self):
        """Get status of player from Mopidy core and send webhook."""
        playback_state_future = self.core.playback.get_state()
        current_track_future = self.core.playback.get_current_track()
        time_position = self.core.playback.get_time_position()

        playback_state = playback_state_future.get()

        current_status = {
            "state": playback_state,
            "current_track": current_track_future.get(),
            "time_position": time_position.get(),
        }
        payload = {
            "type": "status",
            "data": current_status,
        }

        send_webhook(self.config, payload)
        self.report_again(playback_state)
