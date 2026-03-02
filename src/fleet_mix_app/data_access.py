from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_cc_data() -> pd.DataFrame:
    """Load annual car population by CC band."""
    path = DATA_DIR / "annual_car_population_by_cc_clean.csv"
    df = pd.read_csv(path)
    return df


def load_make_data() -> pd.DataFrame:
    """Load annual car population by make and fuel type."""
    path = DATA_DIR / "annual_car_population_by_make_clean.csv"
    df = pd.read_csv(path)
    return df
