import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_executive_synthesis(category_narrative, region_narrative, 
                            segment_narrative, subcategory_narrative, 
                            overall_context):

    prompt = f"""
You are a senior business analyst writing a final executive brief for the C-suite.

Below are four analytical narratives covering different dimensions of business performance.
Your job is to synthesize these into one tight executive brief. Do not summarize each section separately.
Find the common threads, identify the most urgent issues, and state what leadership needs to decide.

CATEGORY ANALYSIS:
{category_narrative}

REGION ANALYSIS:
{region_narrative}

SEGMENT ANALYSIS:
{segment_narrative}

SUB-CATEGORY ANALYSIS:
{subcategory_narrative}

OVERALL CONTEXT:
{overall_context}

Write the executive brief in exactly this structure:

**BUSINESS HEADLINE**
One sentence. The single most important thing happening in this business right now.
Must reference a specific number.

**CRITICAL FINDINGS**
Exactly 3 bullet points. Each one must:
- Cross reference at least two dimensions (e.g. a category finding connected to a region finding)
- Name specific metrics and numbers
- Represent an urgent signal, not a general observation
- Not repeat the same point across bullets
- Do not connect two separate dimensions as cause and effect unless the data explicitly supports the relationship. Regional and category problems are separate unless the data shows otherwise.
- Each bullet must describe ONE dimension only. Do not connect Category to Region, Region to Segment, or any two dimensions as cause and effect in the same bullet. Cross-dimension connections are not supported by this data.

**DECISIONS REQUIRED**
Exactly 2 bullet points. Each one must:
- Name a specific part of the business
- State a clear directional action
- Reference the data that justifies it
- Not recommend a review, an investigation, or further analysis

**OPPORTUNITY**
One bullet point only. The single strongest positive signal in the data.
Must name a specific number.

Format rules:
- Total length must not exceed 200 words
- No vague language
- No invented figures
- Write for someone who has 60 seconds to read this
- The headline must reference the overall business margin, not just one category
- Critical Findings must only contain urgent negative signals. 
- Positive findings belong in a separate opportunities section, not here.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content