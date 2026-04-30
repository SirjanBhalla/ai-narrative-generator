# AI Executive Narrative Generator

An AI-powered Python pipeline that automates business performance analysis by transforming raw sales data into a boardroom-ready executive narrative using LLM prompt engineering and structured data grounding.

---

## What It Does

Most business reporting stops at the numbers. This project goes further. It takes a structured sales dataset, calculates key performance metrics across four dimensions (category, region, customer segment, and sub-category), and feeds those metrics into a prompt-engineered LLM pipeline that produces an insight-driven executive narrative.

The output is an interactive HTML report containing:

- A traffic light performance scorecard showing margin health across every dimension
- An executive brief answering three questions: what is happening, what is driving it, and what should be done
- Collapsible detailed analysis sections for each dimension
- Color-coded tables highlighting positive and negative margin trends

The entire pipeline runs in under 60 seconds from a single command.

---

## Architecture

See [architecture.md](architecture.md) for the full pipeline diagram.

The pipeline has four stages:

1. **Data preparation** - Load the Superstore dataset, split into current year (2026) vs historical baseline (2023-2025), and calculate margin, year-over-year delta, and average discount rate for each dimension
2. **Data grounding** - Pre-calculate direction labels and format all numbers before passing to the LLM, so the model reasons on verified facts rather than raw data
3. **Prompt layer** - Five modular prompt files, one per dimension plus a synthesis prompt that produces the executive brief
4. **Report generation** - Assemble all narratives and metrics into a single interactive HTML file

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data processing | pandas |
| LLM API | Groq (llama-3.3-70b-versatile) |
| Report output | HTML, CSS, JavaScript |
| Dataset | Tableau Superstore (.xls) |
| Environment | python-dotenv |
| Version control | Git, GitHub |

---

## How to Run It Locally

**1. Clone the repo**

```bash
git clone https://github.com/SirjanBhalla/ai-narrative-generator.git
cd ai-narrative-generator
```

**2. Install dependencies**

```bash
pip install pandas openpyxl xlrd groq python-dotenv
```

**3. Add your API key**

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at console.groq.com.

**4. Add the dataset**

Place the Superstore `.xls` file in the `data/` folder and name it `sample_superstore.xls`.

**5. Run the pipeline**

```bash
python -m src.main
```

**6. Open the report**

Open `outputs/report.html` in any browser

---

## Key Technical Decisions

**Why grounding matters**

The LLM never sees raw data. Every number passed to the model is pre-calculated and verified in Python first. Direction labels (IMPROVING, DECLINING) are computed in code, not inferred by the model. This eliminates a whole class of hallucination errors where the model misinterprets numerical direction.

**Why modular prompts**

Each dimension has its own prompt file rather than one large prompt handling everything. This makes iteration faster, failures easier to isolate, and each prompt easier to tune independently. Nine versions of the category prompt were tested before reaching production quality.

**Why a synthesis prompt**

The executive brief is generated separately from the detail sections. It receives all four narratives as input and is constrained to produce a single, cross-dimensional summary. This separates the "what happened in each dimension" from the "so what for leadership" and prevents the two from becoming redundant.

**Why HTML over PDF**

The report is designed to be opened in a browser, not printed. Collapsible sections mean an executive sees only the brief and scorecard by default and can drill into any dimension on demand. This mirrors how executives actually consume information.

---

## Known Limitations

- The dataset is static. In a production environment this pipeline would connect to a live data warehouse rather than a flat file.
- Dollar impact modeling is not automated. The report surfaces margin and discount patterns but does not calculate estimated profit recovery figures. That analysis is intentionally left for a human analyst to validate and present separately.
- The Groq API is non-deterministic. Each run produces slightly different narrative wording. The structure and findings remain consistent but exact phrasing will vary.
- South region margin decline does not have a clear discount-rate explanation in the data. The pipeline correctly flags this as unexplained rather than inventing a cause.

---

## Future Enhancements

- Connect to a live Snowflake or Databricks data source instead of a flat file
- Add scheduled runs so the report generates automatically on a monthly cadence and is emailed to a distribution list
- Add return rate analysis using the Returns tab in the Superstore dataset
- Add a dollar impact estimate layer with clearly stated assumptions for each recovery figure

---

## Project Context

This project was built as a portfolio piece to demonstrate practical AI skills relevant to a BI and Data Analyst role. The goal was not to build a product but to answer a real question: how does an analyst use LLMs to accelerate the reporting workflow without sacrificing accuracy or introducing hallucinated insights?

The answer this project demonstrates is structured data grounding combined with constrained prompt engineering. The LLM handles natural language generation. The analyst handles data validation, prompt design, and output quality control.
