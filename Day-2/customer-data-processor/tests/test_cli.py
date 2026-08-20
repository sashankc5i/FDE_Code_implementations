"""Tests for command-line argument parsing."""

from unittest.mock import patch

from scripts.generate_data import parse_arguments


def test_parse_arguments_defaults():
    """Test default CLI values."""

    with patch(
        "sys.argv",
        ["generate_data.py"],
    ):
        arguments = parse_arguments()

    assert arguments.customers == 100
    assert arguments.duplicates == 0.05
    assert arguments.invalid == 0.05


def test_parse_arguments_custom_values():
    """Test custom CLI values."""

    with patch(
        "sys.argv",
        [
            "generate_data.py",
            "--customers",
            "500",
            "--duplicates",
            "0.10",
            "--invalid",
            "0.02",
        ],
    ):
        arguments = parse_arguments()

    assert arguments.customers == 500
    assert arguments.duplicates == 0.10
    assert arguments.invalid == 0.02