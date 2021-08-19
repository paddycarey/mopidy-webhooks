from __future__ import annotations

import json
import logging

import requests
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def send_webhook(config, payload):
    """Sends a HTTP request to the configured server.

    All exceptions are suppressed but emit a warning message in the log.
    """
    try:
        headers = {
            "Content-Type": "application/json",
        }
        if config["api_key"] and config["api_key_header_name"]:
            headers[config["api_key_header_name"]] = config["api_key"]

        # TODO: Allow multiple webhook URLs
        response = requests.post(
            config["webhook_url"],
            data=json.dumps(payload, cls=ModelJSONEncoder),
            headers=headers,
        )
    except Exception as e:
        logger.exception(
            "Unable to send webhook: ({0}) {1}".format(
                e.__class__.__name__,
                str(e),
            )
        )
    else:
        logger.debug(
            "Webhook response: ({0}) {1}".format(
                response.status_code,
                response.text,
            )
        )
