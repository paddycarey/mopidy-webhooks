from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.3.0'
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Webhooks'
    ext_name = 'webhooks'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['api_key'] = config.String()
        schema['api_key_header_name'] = config.String()
        schema['status_update_interval'] = config.Integer()
        schema['webhook_url'] = config.String()
        return schema

    def setup(self, registry):
        from .frontend import WebhookFrontend
        registry.add('frontend', WebhookFrontend)
