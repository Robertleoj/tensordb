from tensordb.utils.naming import check_name_valid


def test_check_name_valid() -> None:  # noqa: D103
    name = "valid_name"
    assert check_name_valid(name) is True, f"{name} should be valid"
    name = "valid_name_2"
    assert check_name_valid(name) is True, f"{name} should be valid"
    name = "ValidName"
    assert check_name_valid(name) is True, f"{name} should be valid"
    name = "invalid name"
    assert check_name_valid(name) is False, f"{name} should be invalid"
    name = "invalid-name"
    assert check_name_valid(name) is False, f"{name} should be invalid"
    name = "invalid_name!"
    assert check_name_valid(name) is False, f"{name} should be invalid"
    name = "invalid_name@"
    assert check_name_valid(name) is False, f"{name} should be invalid"
    name = "invalid_name#"
    assert check_name_valid(name) is False, f"{name} should be invalid"
    name = " invalid_name"
    assert check_name_valid(name) is False, f"{name} should be invalid"
