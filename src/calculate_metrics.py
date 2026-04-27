import pandas as pd

# Load the data
df = pd.read_excel("data/sample_superstore.xls", sheet_name="Orders")

# Split into historical baseline and current year
historical = df[df["Order Date"].dt.year < 2026]
current = df[df["Order Date"].dt.year == 2026]

# Convert Order Date to datetime so we can work with months and years
df["Order Date"] = pd.to_datetime(df["Order Date"])

# --- OVERALL METRICS ---
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = (total_profit / total_sales) * 100

print("=== OVERALL METRICS ===")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Overall Profit Margin: {overall_margin:.1f}%")

# --- PROFIT MARGIN BY CATEGORY ---
category_metrics = df.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

category_metrics["Margin"] = (category_metrics["Profit"] / category_metrics["Sales"]) * 100

print("\n=== PROFIT MARGIN BY CATEGORY ===")
print(category_metrics.to_string(index=False))

# --- SALES AND PROFIT BY REGION ---
region_metrics = df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

region_metrics["Margin"] = (region_metrics["Profit"] / region_metrics["Sales"]) * 100

print("\n=== SALES AND PROFIT BY REGION ===")
print(region_metrics.to_string(index=False))

# --- SALES AND PROFIT BY SEGMENT ---
segment_metrics = df.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

segment_metrics["Margin"] = (segment_metrics["Profit"] / segment_metrics["Sales"]) * 100

print("\n=== SALES AND PROFIT BY SEGMENT ===")
print(segment_metrics.to_string(index=False))

# --- MONTHLY SALES AND PROFIT TREND ---
df["Month"] = df["Order Date"].dt.to_period("M")

monthly_metrics = df.groupby("Month").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

monthly_metrics["MoM_Sales_Change"] = monthly_metrics["Sales"].pct_change() * 100

print("\n=== MONTHLY SALES AND PROFIT TREND ===")
print(monthly_metrics.to_string(index=False))


# --- TOP AND BOTTOM SUB-CATEGORIES BY PROFIT ---
subcategory_metrics = df.groupby("Sub-Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

subcategory_metrics["Margin"] = (subcategory_metrics["Profit"] / subcategory_metrics["Sales"]) * 100
subcategory_metrics = subcategory_metrics.sort_values("Profit", ascending=False)

print("\n=== TOP 5 SUB-CATEGORIES BY PROFIT ===")
print(subcategory_metrics.head(5).to_string(index=False))

print("\n=== BOTTOM 5 SUB-CATEGORIES BY PROFIT ===")
print(subcategory_metrics.tail(5).to_string(index=False))

# --- YEAR OVER YEAR COMPARISON BY CATEGORY ---
hist_category = historical.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_category["Margin"] = (hist_category["Profit"] / hist_category["Sales"]) * 100
hist_category = hist_category.rename(columns={"Sales": "Hist_Sales", "Profit": "Hist_Profit", "Margin": "Hist_Margin"})

curr_category = current.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_category["Margin"] = (curr_category["Profit"] / curr_category["Sales"]) * 100

category_yoy = curr_category.merge(hist_category, on="Category")
category_yoy["Margin_Delta"] = category_yoy["Margin"] - category_yoy["Hist_Margin"]

print("\n=== CATEGORY: CURRENT VS HISTORICAL ===")
print(category_yoy[["Category", "Margin", "Hist_Margin", "Margin_Delta"]].to_string(index=False))

# --- YEAR OVER YEAR COMPARISON BY REGION ---
hist_region = historical.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_region["Margin"] = (hist_region["Profit"] / hist_region["Sales"]) * 100
hist_region = hist_region.rename(columns={"Sales": "Hist_Sales", "Profit": "Hist_Profit", "Margin": "Hist_Margin"})

curr_region = current.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_region["Margin"] = (curr_region["Profit"] / curr_region["Sales"]) * 100

region_yoy = curr_region.merge(hist_region, on="Region")
region_yoy["Margin_Delta"] = region_yoy["Margin"] - region_yoy["Hist_Margin"]

print("\n=== REGION: CURRENT VS HISTORICAL ===")
print(region_yoy[["Region", "Margin", "Hist_Margin", "Margin_Delta"]].to_string(index=False))

# --- YEAR OVER YEAR COMPARISON BY SEGMENT ---
hist_segment = historical.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
hist_segment["Margin"] = (hist_segment["Profit"] / hist_segment["Sales"]) * 100
hist_segment = hist_segment.rename(columns={"Sales": "Hist_Sales", "Profit": "Hist_Profit", "Margin": "Hist_Margin"})

curr_segment = current.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
curr_segment["Margin"] = (curr_segment["Profit"] / curr_segment["Sales"]) * 100

segment_yoy = curr_segment.merge(hist_segment, on="Segment")
segment_yoy["Margin_Delta"] = segment_yoy["Margin"] - segment_yoy["Hist_Margin"]

print("\n=== SEGMENT: CURRENT VS HISTORICAL ===")
print(segment_yoy[["Segment", "Margin", "Hist_Margin", "Margin_Delta"]].to_string(index=False))