import logging
from typing import Any

import toml

from tensordb._utils.paths import get_package_root

logger = logging.getLogger(__name__)


class classproperty(property):
    """Decorator class to create class properties.

    Obtained from https://stackoverflow.com/a/64738850
    """

    def __get__(self, cls, owner):
        """Get class property.

        Args:
            cls: Class.
            owner: Owner.
        """
        return classmethod(self.fget).__get__(None, owner)()


class ConfigDict:
    """Dictionary class used for configuration.

    Instead of string key access, this dict allows access using attributes.
    So instead of `config['param']`, this class allows the use of `config.param` syntax.
    """

    def __init__(self, data: dict) -> None:
        """Convert a dictionary into a ConfigDict.

        Args:
            data: The dictionary to convert
        """
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigDict(value)
            self.__dict__[key] = value

    def __getattr__(self, key: str) -> Any:
        """Return the value of the value corresponding to the key.

        Args:
            key: The key to get the value for
        """
        return self.__dict__.get(key)

    def __repr__(self) -> str:
        """Forwards the rperesentation of the underlying dictionary."""
        return repr(self.__dict__)


class Config:
    """Singleton class for global configuration.

    After calling GlobalConfig.initialize(config_path), the config can be accessed
    via GlobalConfig.config.
    """

    _instance: ConfigDict | None = None
    _config_path = get_package_root() / "config.toml"

    @classproperty
    def config(cls) -> ConfigDict:
        """Global config."""
        if cls._instance is None:
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls) -> None:
        """Initialize global config from toml file."""
        if cls._instance is not None:
            logger.warn("Config already initialized. Ignoring call to GlobalConfig.initialize.")
            return

        logger.info(f"Initializing config from {cls._config_path}")
        cls._load()

    @classmethod
    def _load(cls) -> None:
        with cls._config_path.open("r") as config_file:
            cls._instance = ConfigDict(toml.load(config_file))

    @classmethod
    def _reload(cls) -> None:
        """Reload global config from json file.

        Intended to be used only in testing / debugging.
        """
        logger.info(f"Reloading config from {cls._config_path}")
        cls._load()
