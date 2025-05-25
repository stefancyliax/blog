import pytest
from helper import starts_with_number_dot  

@pytest.mark.parametrize("input_str,expected", [
    ("1. item", True),
    ("9. something", True),
    ("0. zero case", True),
    ("10. multi-digit", True),   # Only first 3 chars checked: "10."
    ("2 item", False),
    ("x. not a number", False),
    (".1 invalid", False),
    ("", False),
    ("1.", True),
    ("5.abc", True),
    ("5", False),
    ("542.", True),
    ("5143434.adfasd.", False),
    ("lorem ipsum. and some more", False),
    ("- lorem ipsum dolor ", False),
    ("sit amet", False),
    (", consectetur adipiscing elit.", False),
    ("- ", False),
    ("sed do eiusmod", False),
    (" tempor incididunt ut labore et dolore magna aliqua.", False),
    ("- ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", False),
])

def test_starts_with_number_dot(input_str, expected):
    assert starts_with_number_dot(input_str) == expected


