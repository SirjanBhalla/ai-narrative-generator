# Prompt Version Log — `generate_narrative.py`

> **Purpose:** Track every prompt version used to refine the AI narrative output.
> Each entry includes what changed and the full prompt text as it appeared in the script.

---

## Version 1.0

**NOTE:** Initial prompt. Broad, high-level rules with no structural constraints.

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- Lead with the most critical insight, not a general summary
- Name specific categories and margins, do not speak in generalities
- Identify what the numbers suggest is driving the pattern
- End with one specific recommendation
- Write like a senior analyst, not a report generator
- Use bullet points for readability
-->

---

## Version 2.0

**NOTE:** Removed system persona context. Added "no preamble" and "presenting to a board" tone constraints.

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- Open directly with the most urgent finding, no preamble
- Name specific categories and exact margin percentages
- Do not infer causes that are not present in the data
- End with one specific, actionable recommendation
- Write like a senior analyst presenting to a board, not a report generator
- Use bullet points for readability
-->

---

## Version 3.0

**NOTE:** Added explicit constraint that the recommendation must reference the contrast between weakest and strongest category, and must be a decision (not a review).

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- Open directly with the most urgent finding, no preamble
- Name specific categories and exact margin percentages
- Do not infer causes that are not present in the data
- End with one specific, actionable recommendation
- Write like a senior analyst presenting to a board, not a report generator
- Use bullet points for readability
- End with one specific, actionable recommendation that references the contrast
  between the weakest and strongest performing category.
  Do not recommend a review or an investigation. Recommend a decision.
-->

---

## Version 4.0

**NOTE:** Added constraint that the first sentence must name a specific category and number (no general business opener).

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- Open directly with the most urgent finding, no preamble
- The first sentence must name a specific category and a specific number.
  Do not start with a general statement about the business.
- Name specific categories and exact margin percentages
- Do not infer causes that are not present in the data
- End with one specific, actionable recommendation
- Write like a senior analyst presenting to a board, not a report generator
- Use bullet points for readability
- End with one specific, actionable recommendation that references the contrast
  between the weakest and strongest performing category.
  Do not recommend a review or an investigation. Recommend a decision.
-->

---

## Version 5.0

**NOTE:** Banned vague decline language ("experiencing a decline", "key highlights"). Added "go directly into bullet points" — no transition sentence.

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- The first sentence must name a specific category and a specific number.
  Do not start with a general statement about the business.
- Do not use phrases like "experiencing a decline" or "key highlights".
  Use precise language that reflects the magnitude of the change.
- Go directly into bullet points after the opening sentence.
  No transition phrase before them.
- Do not infer causes that are not present in the data.
- End with one specific, actionable recommendation
- Write like a senior analyst presenting to a board, not a report generator
- Use bullet points for readability
- End with one specific, actionable recommendation that references the contrast
  between the weakest and strongest performing category.
  Do not recommend a review or an investigation. Recommend a decision.
-->

---

## Version 6.0

**NOTE:** Added constraint that the recommendation must involve reducing investment/exposure in the worst category (not increasing it). Removed "Open directly" — replaced by stronger first-sentence rule.

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- The first sentence must name a specific category and a specific number.
  Do not start with a general statement about the business.
- Do not use phrases like "experiencing a decline" or "key highlights".
  Use precise language that reflects the magnitude of the change.
- Go directly into bullet points after the opening sentence.
  No transition phrase before them.
- Do not infer causes that are not present in the data.
- Do not invent specific dollar figures or budget numbers that are not
  present in the data.
- The recommendation must involve reducing investment or exposure in the
  worst performing category, not increasing it.
- End with one specific, actionable recommendation that references the
  contrast between the weakest and strongest performing category.
  Do not recommend a review or an investigation. Recommend a decision.
- Use bullet points for readability.
-->

---

## Version 7.0

**NOTE:** Added rule requiring both current and historical numbers to be named when describing a change. Added rule banning invented percentages or allocation figures in the recommendation.

<!--
You are a senior business intelligence analyst writing an executive summary for the C-suite.

Below is category-level profitability data for a retail business comparing
2026 performance against a 3-year historical average (2023-2025).

{category_data}

Write a 3-4 sentence executive narrative for this data. Follow these rules:
- The first sentence must name a specific category and a specific number.
  Do not start with a general statement about the business.
- Do not use phrases like "experiencing a decline" or "key highlights".
  Use precise language that reflects the magnitude of the change.
- Go directly into bullet points after the opening sentence.
  No transition phrase before them.
- Do not infer causes that are not present in the data.
- Do not invent specific dollar figures or budget numbers that are not
  present in the data.
- The recommendation must involve reducing investment or exposure in the
  worst performing category, not increasing it.
- End with one specific, actionable recommendation that references the
  contrast between the weakest and strongest performing category.
  Do not recommend a review or an investigation. Recommend a decision.
- Use bullet points for readability.
- Always reference both the current and historical number when describing
  a change. Never say "from historical levels" without naming the actual number.
- Do not invent percentages, budgets, or allocation figures of any kind.
  The recommendation must be directional only, no made up quantities.
-->

---

## Version 8.0

**NOTE:** Added `Avg_Discount` column to the data context. Restructured output format around three explicit executive questions: *What is happening? / What is driving it? / What should be done?*

<!--
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
-->