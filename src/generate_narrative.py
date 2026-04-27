import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load and prepare data
df = pd.read_excel("data/sample_superstore.xls", sheet_name="Orders")
df["Order Date"] = pd.to_datetime(df["Order Date"])

historical = df[df["Order Date"].dt.year < 2026]
current = df[df["Order Date"].dt.year == 2026]

# Calculate category metrics
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

category_yoy = curr_category.merge(
    hist_category, on="Category", suffixes=("_2026", "_hist")
)
category_yoy["Margin_Delta"] = (
    category_yoy["Margin_2026"] - category_yoy["Margin_hist"]
)

# Add average discount by category
discount_category = df.groupby("Category").agg(
    Avg_Discount=("Discount", "mean")
).reset_index()
discount_category["Avg_Discount"] = (discount_category["Avg_Discount"] * 100).round(1).astype(str) + "%"

category_yoy = category_yoy.merge(discount_category, on="Category")

# Build prompt
category_yoy["Margin_2026"] = category_yoy["Margin_2026"].round(1).astype(str) + "%"
category_yoy["Margin_hist"] = category_yoy["Margin_hist"].round(1).astype(str) + "%"
category_yoy["Margin_Delta"] = category_yoy["Margin_Delta"].round(1).astype(str) + "%"

category_data = category_yoy[
    ["Category", "Margin_2026", "Margin_hist", "Margin_Delta", "Avg_Discount"]
].to_string(index=False)

prompt = f"""
You are a senior business analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing 
2026 performance against a 3-year historical average (2023-2025). 
Avg_Discount is the average discount rate applied to orders in that category.

{category_data}

Write an executive narrative structured around exactly these three questions:

1. What is happening?
   - Lead with the most critical finding first
   - Name specific categories, exact margins, and direction of change
   - Reference both current and historical numbers when describing a change

2. What is driving it?
   - Use the Avg_Discount data to explain margin performance
   - Only reference causes that are supported by the data provided
   - Do not invent causes that are not in the data

3. What should be done?
   - Recommend a specific directional decision
   - Reference the contrast between the weakest and strongest category
   - Do not invent budget figures, percentages, or allocation numbers

Format rules:
   - Use these three questions as headers
   - Use bullet points under each header
   - Name specific numbers in every bullet point
   - Do not use vague language like "historical levels" or "significant decline"
   - Do not recommend a review or investigation, recommend a decision
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)

print("=== CATEGORY NARRATIVE ===")
print(response.choices[0].message.content)