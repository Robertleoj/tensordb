from dataclasses import asdict

import toml
from tensordb._config import CONFIG
from tensordb._utils.paths import get_package_root


def test_global_config() -> None:
    """Test that GLOBAL_CONFIG matches the global_config.toml file."""
    toml_dict = toml.load(get_package_root() / "config.toml")
    dataclass_dict = asdict(CONFIG)

    assert dataclass_dict == toml_dict
