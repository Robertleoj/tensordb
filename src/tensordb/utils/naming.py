import re


def check_name_valid(name: str) -> bool:
    """Check if a name is a valid name.

    We define a valid name as a string that only contains alphanumeric characters and underscores.

    Args:
        name: The name to check.

    Returns:
        valid: True if the name is valid, False otherwise.
    """
    return bool(re.match("^[A-Za-z0-9_]*$", name))
