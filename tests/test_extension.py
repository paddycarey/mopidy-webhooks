from mopidy_webhooks import Extension


def test_get_default_config():
    config = Extension().get_default_config()
    assert "[webhooks]" in config
    assert "enabled = true" in config


def test_get_config_schema():
    schema = Extension().get_config_schema()
    assert "webhook_url" in schema
    assert "api_key" in schema
    assert "api_key_header_name" in schema
    assert "status_update_interval" in schema
