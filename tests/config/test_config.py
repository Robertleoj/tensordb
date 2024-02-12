from tensordb._config import Config, ConfigDict


def test_global_config() -> None:
    """Test that the global config is loaded correctly."""
    # this should trigger a load of the config
    Config.config

    assert isinstance(
        Config._instance, ConfigDict
    ), "GlobalConfig._instance should be a GlobalConfigData after initialization"
    assert isinstance(
        Config.config, ConfigDict
    ), "GlobalConfig.config should be a GlobalConfigData after initialization"
