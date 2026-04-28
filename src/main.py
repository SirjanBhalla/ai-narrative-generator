import pandas as pd
import os
from dotenv import load_dotenv
from src.prompts.category_prompt import get_category_narrative
from src.prompts.region_prompt import get_region_narrative
from src.prompts.segment_prompt import get_segment_narrative
from src.prompts.subcategory_prompt import get_subcategory_narrative
from src.prompts.synthesis_prompt import get_executive_synthesis

load_dotenv()

# Load data
df = pd.read_excel("data/sample_superstore.xls", sheet_name="Orders")
df["Order Date"] = pd.to_datetime(df["Order Date"])

historical = df[df["Order Date"].dt.year < 2026]
current = df[df["Order Date"].dt.year == 2026]

# Category metrics
hist_category = historical.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_category["Margin"] = (hist_category["Profit"] / hist_category["Sales"]) * 100

curr_category = current.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_category["Margin"] = (curr_category["Profit"] / curr_category["Sales"]) * 100

category_yoy = curr_category.merge(hist_category, on="Category", suffixes=("_2026", "_hist"))
category_yoy["Margin_Delta"] = category_yoy["Margin_2026"] - category_yoy["Margin_hist"]

discount_category = df.groupby("Category").agg(
    Avg_Discount=("Discount", "mean")
).reset_index()
discount_category["Avg_Discount"] = (discount_category["Avg_Discount"] * 100).round(1).astype(str) + "%"

category_yoy = category_yoy.merge(discount_category, on="Category")
category_yoy["Margin_2026"] = category_yoy["Margin_2026"].round(1).astype(str) + "%"
category_yoy["Margin_hist"] = category_yoy["Margin_hist"].round(1).astype(str) + "%"
category_yoy["Margin_Delta"] = category_yoy["Margin_Delta"].round(1).astype(str) + "%"


# Region metrics
hist_region = historical.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_region["Margin"] = (hist_region["Profit"] / hist_region["Sales"]) * 100

curr_region = current.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_region["Margin"] = (curr_region["Profit"] / curr_region["Sales"]) * 100

region_yoy = curr_region.merge(hist_region, on="Region", suffixes=("_2026", "_hist"))
region_yoy["Margin_Delta"] = region_yoy["Margin_2026"] - region_yoy["Margin_hist"]

discount_region = df.groupby("Region").agg(
    Avg_Discount=("Discount", "mean")
).reset_index()
discount_region["Avg_Discount"] = (discount_region["Avg_Discount"] * 100).round(1).astype(str) + "%"

region_yoy = region_yoy.merge(discount_region, on="Region")
region_yoy["Margin_2026"] = region_yoy["Margin_2026"].round(1).astype(str) + "%"
region_yoy["Margin_hist"] = region_yoy["Margin_hist"].round(1).astype(str) + "%"
region_yoy["Margin_Delta"] = region_yoy["Margin_Delta"].round(1).astype(str) + "%"


# Segment metrics
hist_segment = historical.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_segment["Margin"] = (hist_segment["Profit"] / hist_segment["Sales"]) * 100

curr_segment = current.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_segment["Margin"] = (curr_segment["Profit"] / curr_segment["Sales"]) * 100

segment_yoy = curr_segment.merge(hist_segment, on="Segment", suffixes=("_2026", "_hist"))
segment_yoy["Margin_Delta"] = segment_yoy["Margin_2026"] - segment_yoy["Margin_hist"]

discount_segment = df.groupby("Segment").agg(
    Avg_Discount=("Discount", "mean")
).reset_index()
discount_segment["Avg_Discount"] = (discount_segment["Avg_Discount"] * 100).round(1).astype(str) + "%"

segment_yoy = segment_yoy.merge(discount_segment, on="Segment")
segment_yoy["Margin_2026"] = segment_yoy["Margin_2026"].round(1).astype(str) + "%"
segment_yoy["Margin_hist"] = segment_yoy["Margin_hist"].round(1).astype(str) + "%"
segment_yoy["Margin_Delta"] = segment_yoy["Margin_Delta"].round(1).astype(str) + "%"


# Sub-category metrics
subcategory_metrics = df.groupby("Sub-Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
subcategory_metrics["Margin"] = (subcategory_metrics["Profit"] / subcategory_metrics["Sales"]) * 100
subcategory_metrics["Sales"] = subcategory_metrics["Sales"].round(0)
subcategory_metrics["Profit"] = subcategory_metrics["Profit"].round(0)
subcategory_metrics["Margin"] = subcategory_metrics["Margin"].round(1)
subcategory_metrics = subcategory_metrics.sort_values("Profit", ascending=False)

top_5 = subcategory_metrics.head(5)
bottom_5 = subcategory_metrics.tail(5)

# Overall business metrics for synthesis context
overall_2026_sales = current["Sales"].sum()
overall_2026_profit = current["Profit"].sum()
overall_2026_margin = (overall_2026_profit / overall_2026_sales * 100).round(1)

overall_hist_sales = historical["Sales"].sum()
overall_hist_profit = historical["Profit"].sum()
overall_hist_margin = (overall_hist_profit / overall_hist_sales * 100).round(1)

margin_direction = "IMPROVING" if overall_2026_margin > overall_hist_margin else "DECLINING"

overall_context = f"""
Overall business margin in 2026: {overall_2026_margin}%
Overall business margin historical average (2023-2025): {overall_hist_margin}%
Margin direction: {margin_direction}
Total profit in 2026: ${overall_2026_profit:,.0f}
All figures are full year 2026 unless otherwise stated.
Tables is a sub-category within Furniture.
Copiers is a sub-category within Technology.
"""

# Generate narrative

# print("=== CATEGORY NARRATIVE ===")
# print(get_category_narrative(category_yoy))

# print("\n=== REGION NARRATIVE ===")
# print(get_region_narrative(region_yoy))

# print("\n=== SEGMENT NARRATIVE ===")
# print(get_segment_narrative(segment_yoy))

# print("\n=== SUB-CATEGORY NARRATIVE ===")
# print(get_subcategory_narrative(top_5, bottom_5))


category_narrative = get_category_narrative(category_yoy)
region_narrative = get_region_narrative(region_yoy)
segment_narrative = get_segment_narrative(segment_yoy)
subcategory_narrative = get_subcategory_narrative(top_5, bottom_5)

print("\n" + "="*60)
print("EXECUTIVE BRIEF")
print("="*60)
print(get_executive_synthesis(
    category_narrative,
    region_narrative,
    segment_narrative,
    subcategory_narrative,
    overall_context
))

