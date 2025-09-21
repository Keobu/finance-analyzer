"""Utility script to generate screenshot assets for the README gallery."""

from pathlib import Path
import importlib.util

import matplotlib

matplotlib.use("Agg")

import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str):
    module_path = ROOT / "src" / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


analysis = load_module("analysis")
categorize = load_module("categorize")
visualization = load_module("visualization")

net_balance = analysis.net_balance
category_totals = analysis.category_totals
categorize_transactions = categorize.categorize_transactions
plot_expenses_by_category = visualization.plot_expenses_by_category
plot_monthly_trend = visualization.plot_monthly_trend
DOCS_IMAGES = ROOT / "docs" / "images"
DOCS_IMAGES.mkdir(parents=True, exist_ok=True)


def build_sample_dataframe() -> pd.DataFrame:
    data = [
        ("2024-01-03", "Fresh Mart Supermarket", 82.45),
        ("2024-01-05", "City Transport - Metro", 24.80),
        ("2024-01-08", "Home Rent", 780.00),
        ("2024-01-12", "Netflix Subscription", 15.99),
        ("2024-01-14", "Downtown Fuel Station", 56.40),
        ("2024-01-18", "Green Market Groceries", 64.10),
        ("2024-01-20", "Spotify Premium", 9.99),
        ("2024-01-22", "Airport Taxi", 43.75),
        ("2024-02-02", "Fresh Mart Supermarket", 89.50),
        ("2024-02-06", "City Transport - Bus", 18.20),
        ("2024-02-09", "Cinema Night", 28.00),
        ("2024-02-15", "Home Utilities Bill", 120.00),
        ("2024-02-18", "Green Market Groceries", 58.30),
        ("2024-02-23", "Downtown Fuel Station", 52.10),
        ("2024-03-01", "Fresh Mart Supermarket", 94.60),
        ("2024-03-04", "Airport Taxi", 38.20),
        ("2024-03-09", "Netflix Subscription", 15.99),
        ("2024-03-12", "Home Rent", 780.00),
        ("2024-03-16", "Green Market Groceries", 61.85),
        ("2024-03-19", "City Transport - Metro", 22.40),
        ("2024-03-23", "Spotify Premium", 9.99),
        ("2024-03-27", "Cinema Night", 26.50),
    ]
    df = pd.DataFrame(data, columns=["date", "description", "amount"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def format_currency(value: float) -> str:
    return f"€{value:,.2f}"


def create_dashboard_preview(df: pd.DataFrame, pie_path: Path, bar_path: Path, output_path: Path) -> None:
    plt.style.use("dark_background")

    fig = plt.figure(figsize=(14, 8), facecolor="#0e1117")
    gs = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[0.55, 1.45], width_ratios=[1.2, 1, 1], hspace=0.32, wspace=0.28)

    metrics_ax = fig.add_subplot(gs[0, :])
    metrics_ax.axis("off")

    metrics = [
        ("Net Balance", format_currency(net_balance(df))),
        ("Active Categories", str(df["category"].nunique())),
        ("Transactions", str(len(df))),
    ]

    for idx, (label, value) in enumerate(metrics):
        x_pos = 0.07 + idx * 0.32
        metrics_ax.text(
            x_pos,
            0.70,
            value,
            fontsize=28,
            fontweight="bold",
            color="#F2F5FA",
            transform=metrics_ax.transAxes,
        )
        metrics_ax.text(
            x_pos,
            0.35,
            label,
            fontsize=14,
            color="#9BA4B5",
            transform=metrics_ax.transAxes,
        )

    metrics_ax.text(
        0.07,
        0.10,
        "Snapshot generated from sample data to mirror the Streamlit summary tab.",
        fontsize=11,
        color="#6C7686",
        transform=metrics_ax.transAxes,
    )

    table_ax = fig.add_subplot(gs[1, 0])
    table_ax.axis("off")

    category_df = category_totals(df).sort_values("total_amount", ascending=False)
    table_data = [[row.category, format_currency(row.total_amount)] for row in category_df.itertuples()]

    table = table_ax.table(
        cellText=table_data,
        colLabels=["Category", "Total (€)"],
        colColours=["#1f2933", "#1f2933"],
        loc="center",
        cellLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.1, 1.3)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#2d3748")
        if row == 0:
            cell.set_facecolor("#111827")
            cell.set_text_props(color="#E5E9F0", weight="bold")
        else:
            cell.set_facecolor("#1f2933")
            cell.set_text_props(color="#F2F5FA")

    table_ax.set_title("Category Totals", loc="left", fontsize=14, color="#F2F5FA", pad=12)

    pie_ax = fig.add_subplot(gs[1, 1])
    pie_ax.axis("off")
    pie_ax.imshow(mpimg.imread(pie_path))
    pie_ax.set_title("Expenses by Category", fontsize=14, color="#F2F5FA", pad=12)

    bar_ax = fig.add_subplot(gs[1, 2])
    bar_ax.axis("off")
    bar_ax.imshow(mpimg.imread(bar_path))
    bar_ax.set_title("Monthly Trend", fontsize=14, color="#F2F5FA", pad=12)

    fig.suptitle("Finance Expense Analyzer — Dashboard Preview", fontsize=18, color="#F9FAFB", fontweight="bold", y=0.95)

    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    df = build_sample_dataframe()
    df = categorize_transactions(df)

    # Charts expect positive spend values.
    df_for_charts = df.copy()
    df_for_charts["amount"] = df_for_charts["amount"].abs()

    pie_path = plot_expenses_by_category(df_for_charts, filename="category-pie.png", to_file=True)
    bar_path = plot_monthly_trend(df_for_charts, filename="monthly-bar.png", to_file=True)

    # Move generated charts into docs/images
    pie_dest = DOCS_IMAGES / "category-pie.png"
    bar_dest = DOCS_IMAGES / "monthly-bar.png"
    pie_dest.write_bytes(pie_path.read_bytes())
    bar_dest.write_bytes(bar_path.read_bytes())
    if pie_path.exists():
        pie_path.unlink()
    if bar_path.exists():
        bar_path.unlink()

    dashboard_path = DOCS_IMAGES / "dashboard-preview.png"
    create_dashboard_preview(df_for_charts, pie_dest, bar_dest, dashboard_path)

    print(f"Generated assets:\n- {pie_dest}\n- {bar_dest}\n- {dashboard_path}")


if __name__ == "__main__":
    main()
