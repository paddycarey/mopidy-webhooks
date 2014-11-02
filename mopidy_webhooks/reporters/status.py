# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging
import time

# third-party imports
import pykka

# local imports
from . import base


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor, base.BaseReporter):

    def __init__(self, config, core):
        super(StatusReporter, self).__init__()
        self.config = config['webhooks']
        self.core = core
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        base.BaseReporter.on_start(self)
        # if configured not to report status then return immediately
        if self.config['status_update_interval'] == 0:
            logger.info('StatusReporter disabled by configuration.')
            return
        self.in_future.report_status()

    def report_again(self, current_status):
        # calculate sleep interval based on current status and configured interval
        _m = {'playing': 1, 'paused': 2, 'stopped': 5}[current_status['state']]
        interval = (self.config['status_update_interval'] * _m) / 1000.0
        # sleep for computed interval and kickoff another webhook
        time.sleep(interval)
        self.in_future.report_status()

    def report_status(self):
        current_status = {
            'current_track': self.core.playback.current_track.get(),
            'state': self.core.playback.state.get(),
            'time_position': self.core.playback.time_position.get(),
        }
        self.send_webhook({'status_report': current_status})
        self.report_again(current_status)
