from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from spatial_notebooks.stats import Summary, add_density, load_csv, summarize


def test_summarize_counts_rows_and_columns() -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = summarize(df)

    assert result.rows == 3
    assert result.columns == 2
    assert result.numeric_columns == ["a"]
    assert result.missing_by_column == {"a": 0, "b": 0}


def test_summarize_counts_missing_values() -> None:
    df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, "z"]})

    result = summarize(df)

    assert result.missing_by_column == {"a": 1, "b": 2}


def test_summarize_handles_empty_dataframe() -> None:
    result = summarize(pd.DataFrame())

    assert result == Summary(rows=0, columns=0, numeric_columns=[], missing_by_column={})


def test_load_csv_reads_file(tmp_path: Path) -> None:
    csv = tmp_path / "t.csv"
    csv.write_text("a,b\n1,x\n2,y\n", encoding="utf-8")

    df = load_csv(csv)

    assert list(df.columns) == ["a", "b"]
    assert len(df) == 2


def test_load_csv_raises_when_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "does-not-exist.csv")


def test_add_density_computes_people_per_km2() -> None:
    df = pd.DataFrame({"population": [100, 200], "area_km2": [10.0, 50.0]})

    result = add_density(df)

    assert list(result["density"]) == [10.0, 4.0]


def test_add_density_returns_new_dataframe() -> None:
    df = pd.DataFrame({"population": [100], "area_km2": [10.0]})

    result = add_density(df)

    assert "density" not in df.columns
    assert "density" in result.columns


def test_add_density_rejects_missing_columns() -> None:
    df = pd.DataFrame({"population": [1, 2]})

    with pytest.raises(ValueError, match="area_km2"):
        add_density(df)
