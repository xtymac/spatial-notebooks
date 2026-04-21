"""Summary statistics for tabular data. Phase 1 practice target."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class Summary:
    rows: int
    columns: int
    numeric_columns: list[str]
    missing_by_column: dict[str, int]


def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path)


def summarize(df: pd.DataFrame) -> Summary:
    numeric = df.select_dtypes(include="number").columns.tolist()
    missing = {col: int(df[col].isna().sum()) for col in df.columns}
    return Summary(
        rows=len(df),
        columns=len(df.columns),
        numeric_columns=numeric,
        missing_by_column=missing,
    )


def add_density(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with a `density` column (population per km²)."""
    required = {"population", "area_km2"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"df must have columns {sorted(required)}; missing: {sorted(missing)}"
        )
    return df.assign(density=df["population"] / df["area_km2"])
