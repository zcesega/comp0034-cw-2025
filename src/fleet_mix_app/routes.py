from flask import Blueprint, render_template, request
from plotly import express as px

from .analytics import compare_cc_by_year, top_manufacturers_by_year
from .data_access import load_cc_data, load_make_data

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@bp.route("/comparison", methods=["GET", "POST"])
def comparison():
    """Fleet mix comparison view."""
    df_cc = load_cc_data()
    years = sorted(df_cc["year"].unique())
    result = None
    error = None

    if request.method == "POST":
        year1 = request.form.get("year1", type=int)
        year2 = request.form.get("year2", type=int)
        try:
            if year1 is None or year2 is None:
                raise ValueError("Please select both years.")
            result = compare_cc_by_year(df_cc, year1, year2)
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "comparison.html",
        years=years,
        result=result,
        error=error,
    )


@bp.route("/manufacturers", methods=["GET", "POST"])
def manufacturers():
    """Manufacturer analysis view."""
    df_make = load_make_data()
    years = sorted(df_make["year"].unique())
    table = None
    chart_html = None
    selected_year = None
    error = None

    if request.method == "POST":
        selected_year = request.form.get("year", type=int)
        try:
            if selected_year is None:
                raise ValueError("Please select a year.")
            table_df = top_manufacturers_by_year(df_make, selected_year)
            table = table_df.to_dict(orient="records")
            fig = px.bar(
                table_df,
                x="make",
                y="number",
                title=f"Top manufacturers in {selected_year}",
            )
            chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "manufacturers.html",
        years=years,
        selected_year=selected_year,
        table=table,
        chart_html=chart_html,
        error=error,
    )
