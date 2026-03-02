from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def compare_cc_by_year(
    df_cc: pd.DataFrame, year1: int, year2: int
) -> Dict[str, Any]:
    """Compare CC-band distributions between two years.

    Returns a dict with table rows, totals, Mix Shift Score and top bands.
    """
    years = set(df_cc["year"].unique())
    if year1 not in years or year2 not in years:
        raise ValueError("Selected years are not available in the dataset.")
    if year1 == year2:
        raise ValueError("Please choose two different years.")

    subset = df_cc[df_cc["year"].isin([year1, year2])].copy()

    grouped = (
        subset.groupby("year", as_index=False)["number"]
        .sum()
        .rename(columns={"number": "total"})
    )
    totals = dict(zip(grouped["year"], grouped["total"]))

    if totals[year1] == 0 or totals[year2] == 0:
        raise ValueError("Total vehicle count is zero for one of the years.")

    subset["percentage"] = subset.apply(
        lambda row: (row["number"] / totals[row["year"]]) * 100.0,
        axis=1,
    )

    pivot = subset.pivot_table(
        index="cc_rating",
        columns="year",
        values=["number", "percentage"],
        fill_value=0.0,
    )

    rows: List[Dict[str, Any]] = []
    mix_shift_score = 0.0

    for cc_band, values in pivot.iterrows():
        n1 = float(values[("number", year1)])
        n2 = float(values[("number", year2)])
        p1 = float(values[("percentage", year1)])
        p2 = float(values[("percentage", year2)])
        pp_change = p2 - p1
        mix_shift_score += abs(pp_change)
        rows.append(
            {
                "cc_rating": cc_band,
                "number_year1": int(n1),
                "number_year2": int(n2),
                "pct_year1": p1,
                "pct_year2": p2,
                "pp_change": pp_change,
            }
        )

    rows.sort(key=lambda r: r["cc_rating"])
    top_bands = sorted(
        rows, key=lambda r: abs(r["pp_change"]), reverse=True
    )[:3]

    return {
        "year1": year1,
        "year2": year2,
        "total_year1": totals[year1],
        "total_year2": totals[year2],
        "rows": rows,
        "mix_shift_score": mix_shift_score,
        "top_bands": top_bands,
    }


def top_manufacturers_by_year(
    df_make: pd.DataFrame, year: int, limit: int = 10
) -> pd.DataFrame:
    """Return top manufacturers for a given year."""
    if year not in set(df_make["year"].unique()):
        raise ValueError("Selected year is not available in the dataset.")

    subset = df_make[df_make["year"] == year]
    grouped = (
        subset.groupby("make", as_index=False)["number"]
        .sum()
        .sort_values("number", ascending=False)
        .head(limit)
    )
    return grouped
