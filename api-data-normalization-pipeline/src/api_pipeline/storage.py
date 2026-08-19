"""Functions for storing raw and processed data."""

import json
from pathlib import Path

import pandas as pd


def save_json(
    data: list[dict],
    file_path: Path,
) -> None:
    """Save raw API data as JSON."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
        )


def save_dataframe(
    dataframe: pd.DataFrame,
    file_path: Path,
) -> None:
    """
    Save a DataFrame based on the requested file format.

    Supported formats:
        CSV
        Parquet
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if file_path.suffix == ".csv":
        dataframe.to_csv(
            file_path,
            index=False,
        )

    elif file_path.suffix == ".parquet":
        dataframe.to_parquet(
            file_path,
            index=False,
        )

    else:
        raise ValueError(
            f"Unsupported file format: {file_path.suffix}"
        )