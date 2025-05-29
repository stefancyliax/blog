import pytest
from helper import starts_with_number_dot, debug_print, set_log_level_from_string
import helper as helper_module  # To access and modify CURRENT_LOG_LEVEL

# Import log levels directly for use in tests
from helper import LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR


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


# Tests for debug_print
def test_debug_print_debug_when_current_is_debug(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_DEBUG
    try:
        debug_print("Test message", LOG_LEVEL_DEBUG)
        captured = capsys.readouterr()
        assert "Test message" in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_info_when_current_is_debug(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_DEBUG
    try:
        debug_print("Test message", LOG_LEVEL_INFO)
        captured = capsys.readouterr()
        assert "Test message" in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level


# Tests for set_log_level_from_string
def test_set_log_level_debug():
    original_level = helper_module.CURRENT_LOG_LEVEL
    try:
        set_log_level_from_string("DEBUG")
        assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_DEBUG
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_set_log_level_info_lowercase():
    original_level = helper_module.CURRENT_LOG_LEVEL
    try:
        set_log_level_from_string("info")
        assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_INFO
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_set_log_level_warning():
    original_level = helper_module.CURRENT_LOG_LEVEL
    try:
        set_log_level_from_string("WARNING")
        assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_WARNING
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_set_log_level_error():
    original_level = helper_module.CURRENT_LOG_LEVEL
    try:
        set_log_level_from_string("ERROR")
        assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_ERROR
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_set_log_level_invalid_string(capsys): # capsys or capfd for stderr
    original_level = helper_module.CURRENT_LOG_LEVEL
    # Set a different starting level to ensure it changes to INFO on invalid input
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_DEBUG
    try:
        set_log_level_from_string("INVALID_LEVEL")
        assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_INFO
        captured = capsys.readouterr() # Use capsys for stderr
        assert "Warning: Invalid log level string 'INVALID_LEVEL'. Defaulting to INFO." in captured.err
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_info_when_current_is_info(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_INFO
    try:
        debug_print("Test message", LOG_LEVEL_INFO)
        captured = capsys.readouterr()
        assert "Test message" in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_debug_not_printed_when_current_is_info(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_INFO
    try:
        debug_print("Test message", LOG_LEVEL_DEBUG)
        captured = capsys.readouterr()
        assert "Test message" not in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_warning_when_current_is_info(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_INFO
    try:
        debug_print("Test message", LOG_LEVEL_WARNING)
        captured = capsys.readouterr()
        assert "Test message" in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_error_when_current_is_error(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_ERROR
    try:
        debug_print("Test message", LOG_LEVEL_ERROR)
        captured = capsys.readouterr()
        assert "Test message" in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level

def test_debug_print_warning_not_printed_when_current_is_error(capsys):
    original_level = helper_module.CURRENT_LOG_LEVEL
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_ERROR
    try:
        debug_print("Test message", LOG_LEVEL_WARNING)
        captured = capsys.readouterr()
        assert "Test message" not in captured.out
    finally:
        helper_module.CURRENT_LOG_LEVEL = original_level


