"""Tests for data storage functions."""

import json

import pandas as pd
import pytest

from api_pipeline.storage import (
    save_dataframe,
    save_json,
)


def test_save_json(tmp_path):
    """JSON data should be saved correctly."""

    data = [
        {
            "id": 101,
            "name": "Arun",
        },
        {
            "id": 102,
            "name": "Priya",
        },
    ]

    file_path = tmp_path / "users.json"

    save_json(
        data,
        file_path,
    )

    assert file_path.exists()

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        result = json.load(file)

    assert result == data


def test_save_dataframe_to_csv(tmp_path):
    """DataFrame should be saved and read back from CSV."""

    dataframe = pd.DataFrame(
        {
            "customer_id": [101, 102],
            "name": ["Arun", "Priya"],
            "country": ["India", "India"],
        }
    )

    file_path = tmp_path / "customers.csv"

    save_dataframe(
        dataframe,
        file_path,
    )

    assert file_path.exists()

    result = pd.read_csv(file_path)

    pd.testing.assert_frame_equal(
        result,
        dataframe,
    )


def test_save_dataframe_to_parquet(tmp_path):
    """DataFrame should be saved and read back from Parquet."""

    dataframe = pd.DataFrame(
        {
            "customer_id": [101, 102],
            "name": ["Arun", "Priya"],
            "country": ["India", "India"],
        }
    )

    file_path = tmp_path / "customers.parquet"

    save_dataframe(
        dataframe,
        file_path,
    )

    assert file_path.exists()

    result = pd.read_parquet(file_path)

    pd.testing.assert_frame_equal(
        result,
        dataframe,
    )


def test_save_dataframe_unsupported_format(tmp_path):
    """Unsupported file formats should raise ValueError."""

    dataframe = pd.DataFrame(
        {
            "customer_id": [101],
            "name": ["Arun"],
        }
    )

    file_path = tmp_path / "customers.txt"

    with pytest.raises(
        ValueError,
        match="Unsupported file format",
    ):
        save_dataframe(
            dataframe,
            file_path,
        )