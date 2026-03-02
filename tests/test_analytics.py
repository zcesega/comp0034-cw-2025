import pandas as pd

from fleet_mix_app.analytics import compare_cc_by_year


def test_compare_cc_by_year_basic_properties():
    """GIVEN cc data WHEN two years are compared THEN score is valid."""
    data = [
        {"year": 2005, "cc_rating": "A", "number": 50},
        {"year": 2005, "cc_rating": "B", "number": 50},
        {"year": 2006, "cc_rating": "A", "number": 25},
        {"year": 2006, "cc_rating": "B", "number": 75},
    ]
    df = pd.DataFrame(data)

    result = compare_cc_by_year(df, 2005, 2006)

    total_p1 = sum(r["pct_year1"] for r in result["rows"])
    total_p2 = sum(r["pct_year2"] for r in result["rows"])

    assert round(total_p1, 2) == 100.0
    assert round(total_p2, 2) == 100.0
    assert result["mix_shift_score"] >= 0.0
