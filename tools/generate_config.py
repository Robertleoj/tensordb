from pathlib import Path

import toml
from jinja2 import Environment


def _is_ref(value: str | int | float | list) -> str:
    """Returns True if the value is a reference type.

    Args:
        value: The value.
    """
    return isinstance(value, list)


def make_python_config(config_path: Path, template_path: Path, destination_path: Path):
    """Make a python config file from a template and a toml file.

    Args:
        config_path: Path to the toml config file.
        template_path: Path to the jinja2 template file.
        destination_path: Path to the destination python file.
    """
    config_data = toml.load(config_path)
    env = Environment()

    with template_path.open("r") as f:
        template = env.from_string(f.read())

    with destination_path.open("w") as f:
        f.write(template.render(config_path=str(config_path), dictionary=config_data, is_ref=_is_ref))


def _to_cpp(value: str | int | float | list) -> str:
    """Convert a value to a C++ string representation.

    Args:
        value: The value.

    Returns:
        The C++ string representation.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return "{" + ", ".join([str(_to_cpp(v)) for v in value]) + "}"
    else:
        raise ValueError(f"Unsupported type: {type(value)}")


def _cpp_type(value: str | int | float | list) -> str:
    """Get the C++ type of a value.

    Args:
        value: The value.
    """
    if isinstance(value, str):
        return "std::string"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, list):
        return f"std::vector<{_cpp_type(value[0])}>"
    else:
        raise ValueError(f"Unsupported type: {type(value)}")


def make_cpp_config(
    config_path: Path,
    hpp_template_path: Path,
    hpp_destination_path: Path,
):
    """Make a C++ config file from a template and a toml file.

    Args:
        config_path: Path to the toml config file.
        hpp_template_path: Path to the jinja2 template file for the hpp file.
        hpp_destination_path: Path to the destination of the hpp file.
    """
    config_data = toml.load(config_path)
    env = Environment()
    env.filters["to_cpp"] = _to_cpp
    env.filters["cpp_type"] = _cpp_type

    with hpp_template_path.open("r") as f:
        hpp_template = env.from_string(f.read())

    rendered = hpp_template.render(config_path=str(config_path), config=config_data)

    # avoid recompilation by only writing the file if it has changed

    if hpp_destination_path.exists():
        with hpp_destination_path.open("r") as f:
            current_version = f.read()
    else:
        current_version = ""

    if rendered != current_version:
        with hpp_destination_path.open("w") as f:
            f.write(rendered)


def build_config() -> None:
    """Build the python config file from toml file and jinja2 template."""
    config_path = Path("config.toml")
    make_python_config(
        config_path=config_path,
        template_path=Path("jinja_templates/config/config.py.j2"),
        destination_path=Path("src/tensordb/_config/global_config.py"),
    )

    make_cpp_config(
        config_path=config_path,
        hpp_template_path=Path("jinja_templates/config/config.hpp.j2"),
        hpp_destination_path=Path("include/_tensordb_cpp/config.hpp"),
    )


if __name__ == "__main__":
    build_config()
