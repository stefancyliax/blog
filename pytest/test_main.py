import pytest
import sys
from main import main as main_function  # Use main_function to avoid conflict with pytest's main
import helper as helper_module
from helper import LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR

# Store the original CURRENT_LOG_LEVEL to restore after tests
original_global_log_level = helper_module.CURRENT_LOG_LEVEL

def setup_function():
    """Reset log level before each test to a known state."""
    helper_module.CURRENT_LOG_LEVEL = LOG_LEVEL_INFO # Default or any known state

def teardown_function():
    """Restore original log level after each test."""
    helper_module.CURRENT_LOG_LEVEL = original_global_log_level

def call_main_with_args(monkeypatch, args_list):
    """Helper function to call main_function with specified arguments."""
    monkeypatch.setattr(sys, "argv", ["main.py"] + args_list)
    try:
        main_function()
    except SystemExit as e:
        # Argparse calls sys.exit on --help or errors, catch it
        print(f"SystemExit caught with code: {e.code}")


def test_main_no_log_level_arg_defaults_to_info(monkeypatch):
    call_main_with_args(monkeypatch, [])
    assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_INFO

def test_main_log_level_debug(monkeypatch):
    call_main_with_args(monkeypatch, ["--log-level", "DEBUG"])
    assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_DEBUG

def test_main_log_level_warning_short_alias(monkeypatch):
    call_main_with_args(monkeypatch, ["-l", "WARNING"])
    assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_WARNING

def test_main_log_level_error(monkeypatch):
    call_main_with_args(monkeypatch, ["--log-level", "ERROR"])
    assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_ERROR

def test_main_basepath_and_log_level(monkeypatch):
    # Test with basepath to ensure it's still handled correctly
    call_main_with_args(monkeypatch, ["/custompath/", "--log-level", "DEBUG"])
    assert helper_module.CURRENT_LOG_LEVEL == LOG_LEVEL_DEBUG
    # We don't assert basepath here, just that log level setting isn't broken by it.

# It might also be useful to test what happens with invalid log level choices,
# but argparse handles this by exiting, which is harder to test without
# expecting SystemExit and checking stderr. The subtask focuses on successful setting.
