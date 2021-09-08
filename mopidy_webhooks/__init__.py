from __future__ import annotations

import pathlib

import pkg_resources
from mopidy import config, ext


__version__ = pkg_resources.get_distribution("Mopidy-Webhooks").version


class Extension(ext.Extension):
    dist_name = "Mopidy-Webhooks"
    ext_name = "webhooks"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()

        schema["webhook_url"] = config.String()
        schema["api_key"] = config.String(optional=True)
        schema["api_key_header_name"] = config.String(optional=True)

        schema["status_update_interval"] = config.Integer()

        return schema

    def setup(self, registry):
        from .frontend import WebhookFrontend

        registry.add("frontend", WebhookFrontend)
