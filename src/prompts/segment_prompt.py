import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_segment_narrative(segment_yoy):
    segment_data = segment_yoy[
        ["Segment", "Margin_2026", "Margin_hist", "Margin_Delta", "Avg_Discount"]
    ].to_string(index=False)

    prompt = f"""
You are a senior business analyst writing an executive summary for the C-suite.

Below is customer segment-level profitability data for a retail business comparing 
2026 performance against a 3-year historical average (2023-2025). 
Avg_Discount is the average discount rate applied to orders in that segment.

{segment_data}

Write an executive narrative structured around exactly these three questions:

1. What is happening?
   - Lead with the most critical finding first
   - Name specific segments, exact margins, and direction of change
   - Reference both current and historical numbers when describing a change

2. What is driving it?
   - Use the Avg_Discount data to explain margin performance
   - Only reference causes that are supported by the data provided
   - Do not invent causes that are not in the data

3. What should be done?
   - Write as many recommendations as the data justifies, minimum 1, maximum 3
   - Do not repeat the same recommendation with different wording to fill space
   - Each bullet must be a distinct decision targeting a different part of the problem
   - Reference the contrast between the weakest and strongest performer
   - Do not invent budget figures, percentages, or allocation numbers

Format rules:
   - Use these three questions as headers
   - Use bullet points under each header
   - Name specific numbers in every bullet point
   - Do not use vague language like "historical levels" or "significant decline"
   - Do not recommend a review or investigation, recommend a decision
   - The first sentence must name a specific segment and a specific number
   - Do not invent specific dollar figures or budget numbers
   - The detailed analysis must go deeper than a headline summary and add specific numbers and sub-level insights, do not restate the obvious

"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content