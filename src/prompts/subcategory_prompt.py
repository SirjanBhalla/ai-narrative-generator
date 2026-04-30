import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_subcategory_narrative(top_5, bottom_5):
    top_data = top_5[
        ["Sub-Category", "Sales", "Profit", "Margin"]
    ].to_string(index=False)

    bottom_data = bottom_5[
        ["Sub-Category", "Sales", "Profit", "Margin"]
    ].to_string(index=False)

    prompt = f"""
You are a senior business analyst writing an executive summary for the C-suite.

Below are the top 5 and bottom 5 sub-categories by profit for a retail business in 2026.
Margin is profit as a percentage of sales.

TOP 5 SUB-CATEGORIES BY PROFIT:
{top_data}

BOTTOM 5 SUB-CATEGORIES BY PROFIT:
{bottom_data}

Write an executive narrative structured around exactly these three questions:

1. What is happening?
   - Name the highest and lowest profit sub-categories with exact figures
   - Highlight any sub-category with negative profit explicitly
   - Reference both Sales and Profit where the contrast is meaningful

2. What is driving it?
   - Identify where high sales volume is not translating to profit
   - Only reference patterns visible in the data provided
   - Do not invent causes that are not supported by the numbers

3. What should be done?
   - Write as many recommendations as the data justifies, minimum 1, maximum 3
   - Do not repeat the same recommendation with different wording to fill space
   - Each bullet must be a distinct decision targeting a different part of the problem
   - Reference the contrast between the weakest and strongest performer
   - Do not invent budget figures, percentages, or allocation numbers
   - Do not calculate or estimate potential profit recovery figures. No invented dollar amounts in recommendations.

Format rules:
   - Use these three questions as headers
   - Use bullet points under each header
   - Name specific sub-categories and numbers in every bullet point
   - Do not use vague language
   - Do not recommend a review or investigation, recommend a decision
   - The first sentence must name a specific sub-category and a specific number
   - Negative profit sub-categories must be called out as value destroyers
   - The detailed analysis must go deeper than a headline summary and add specific numbers and sub-level insights, do not restate the obvious

"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content