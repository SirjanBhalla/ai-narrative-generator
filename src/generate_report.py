import os

def get_traffic_light(delta_str):
    try:
        delta = float(delta_str.replace("%", ""))
        if delta >= 1.0:
            return "green", "Improving"
        elif delta >= -1.5:
            return "amber", "Needs Attention"
        else:
            return "red", "Critical"
    except:
        return "amber", "Needs Attention"

def format_narrative(narrative):
    lines = narrative.strip().split("\n")
    html = ""
    in_list = False
    current_section = []
    sections = []
    current_heading = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("##") or (line.startswith("**") and line.endswith("**")):
            if current_heading is not None:
                sections.append((current_heading, current_section))
            current_heading = line.replace("##", "").replace("**", "").strip()
            current_section = []
        else:
            current_section.append(line)

    if current_heading is not None:
        sections.append((current_heading, current_section))

    if not sections:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("*") or line.startswith("-"):
                html += f'<li>{line.lstrip("*- ").strip()}</li>'
            else:
                html += f'<p>{line}</p>'
        return html

    for heading, items in sections:
        html += f'<div class="narrative-card">'
        html += f'<div class="narrative-card-heading">{heading}</div>'
        html += '<ul>'
        for item in items:
            if item.startswith("*") or item.startswith("-"):
                html += f'<li>{item.lstrip("*- ").strip()}</li>'
            else:
                html += f'<li>{item}</li>'
        html += '</ul>'
        html += '</div>'

    return html

def format_brief(narrative):
    lines = narrative.strip().split("\n")
    sections = []
    current_heading = None
    current_items = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("**") and line.endswith("**"):
            if current_heading is not None:
                sections.append((current_heading, current_items))
            current_heading = line.strip("*").strip()
            current_items = []
        elif line.startswith("*") or line.startswith("-"):
            current_items.append(line.lstrip("*- ").strip())
        else:
            current_items.append(line)

    if current_heading is not None:
        sections.append((current_heading, current_items))

    html = ""
    for heading, items in sections:
        html += f'<div class="brief-card">'
        html += f'<div class="brief-card-heading">{heading}</div>'
        if items:
            html += '<div class="brief-card-body">'
            for item in items:
                html += f'<div class="brief-card-item">{item}</div>'
            html += '</div>'
        html += '</div>'

    return html

def build_metric_table(df, columns, format_map=None):
    headers = "".join([f"<th>{col.replace('_', ' ')}</th>" for col in columns])
    rows = ""
    for _, row in df.iterrows():
        cells = ""
        for col in columns:
            val = row[col]
            if format_map and col in format_map:
                val = format_map[col](val)
            if col == "Margin_Delta":
                try:
                    delta = float(str(val).replace("%", ""))
                    color = "#1a6b3c" if delta >= 0 else "#c0392b"
                    cells += f'<td style="color:{color};font-weight:600;">{val}</td>'
                except:
                    cells += f"<td>{val}</td>"
            else:
                cells += f"<td>{val}</td>"
        rows += f"<tr>{cells}</tr>"
    return f"""
    <table>
        <thead><tr>{headers}</tr></thead>
        <tbody>{rows}</tbody>
    </table>"""

def build_scorecard_group(label, items):
    color_map = {"green": "#1a6b3c", "amber": "#b5611a", "red": "#c0392b"}
    bg_map = {"green": "#f0faf4", "amber": "#fdf6ec", "red": "#fdf0ef"}
    border_map = {"green": "#a8d5b5", "amber": "#f0c490", "red": "#f0a090"}

    cards = ""
    for item in items:
        c = item["color"]
        cards += f"""
        <div class="score-card" style="background:{bg_map[c]};border:1px solid {border_map[c]};">
            <div class="score-label">{item["label"]}</div>
            <div class="score-value" style="color:{color_map[c]};">{item["value"]}</div>
            <div class="score-metric-type">{item.get("metric_type", "Profit Margin")}</div>
            <div class="score-delta">{item["delta"]}</div>
            <div class="score-status" style="color:{color_map[c]};">{item["status"]}</div>
        </div>"""

    return f"""
    <div class="scorecard-group">
        <div class="scorecard-group-label">{label}</div>
        <div class="scorecard-grid">{cards}</div>
    </div>"""

def generate_report(
    overall_context,
    category_yoy,
    region_yoy,
    segment_yoy,
    top_5,
    bottom_5,
    category_narrative,
    region_narrative,
    segment_narrative,
    subcategory_narrative,
    executive_brief
):
    # Category scorecard
    category_items = []
    for _, row in category_yoy.iterrows():
        color, label = get_traffic_light(row["Margin_Delta"])
        category_items.append({
            "label": row["Category"],
            "value": row["Margin_2026"],
            "delta": f'vs hist: {row["Margin_Delta"]}',
            "color": color,
            "status": label,
            "metric_type": "Profit Margin"
        })

    # Region scorecard
    region_items = []
    for _, row in region_yoy.iterrows():
        color, label = get_traffic_light(row["Margin_Delta"])
        region_items.append({
            "label": row["Region"],
            "value": row["Margin_2026"],
            "delta": f'vs hist: {row["Margin_Delta"]}',
            "color": color,
            "status": label,
            "metric_type": "Profit Margin"
        })

    # Segment scorecard
    segment_items = []
    for _, row in segment_yoy.iterrows():
        color, label = get_traffic_light(row["Margin_Delta"])
        segment_items.append({
            "label": row["Segment"],
            "value": row["Margin_2026"],
            "delta": f'vs hist: {row["Margin_Delta"]}',
            "color": color,
            "status": label,
            "metric_type": "Profit Margin"
        })

    # Sub-category value destroyers
    loss_items = []
    loss_df = bottom_5[bottom_5["Profit"] < 0]
    for _, row in loss_df.iterrows():
        loss_items.append({
            "label": row["Sub-Category"],
            "value": f'${row["Profit"]:,.0f}',
            "delta": f'Margin: {row["Margin"]:.1f}%',
            "color": "red",
            "status": "Value Destroyer",
            "metric_type": "Annual Profit"
        })

    scorecard_html = (
        build_scorecard_group("Category Performance", category_items) +
        build_scorecard_group("Regional Performance", region_items) +
        build_scorecard_group("Segment Performance", segment_items) +
        build_scorecard_group("Sub-Category Alerts", loss_items)
    )

    # Tables
    category_table = build_metric_table(category_yoy,
        ["Category", "Margin_2026", "Margin_hist", "Margin_Delta", "Avg_Discount"])
    region_table = build_metric_table(region_yoy,
        ["Region", "Margin_2026", "Margin_hist", "Margin_Delta", "Avg_Discount"])
    segment_table = build_metric_table(segment_yoy,
        ["Segment", "Margin_2026", "Margin_hist", "Margin_Delta", "Avg_Discount"])

    def fmt_currency(v):
        try:
            val = float(v)
            if val < 0:
                return f"-${abs(val):,.0f}"
            return f"${val:,.0f}"
        except:
            return v

    def fmt_pct(v):
        try:
            return f"{float(v):.1f}%"
        except:
            return v

    top5_table = build_metric_table(top_5,
        ["Sub-Category", "Sales", "Profit", "Margin"],
        format_map={"Sales": fmt_currency, "Profit": fmt_currency, "Margin": fmt_pct})
    bottom5_table = build_metric_table(bottom_5,
        ["Sub-Category", "Sales", "Profit", "Margin"],
        format_map={"Sales": fmt_currency, "Profit": fmt_currency, "Margin": fmt_pct})

    executive_brief_html = format_brief(executive_brief)
    category_narrative_html = format_narrative(category_narrative)
    region_narrative_html = format_narrative(region_narrative)
    segment_narrative_html = format_narrative(segment_narrative)
    subcategory_narrative_html = format_narrative(subcategory_narrative)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Business Report 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f7f6f3;
            --surface: #ffffff;
            --text-primary: #1c1c1c;
            --text-secondary: #4a4a4a;
            --text-muted: #888888;
            --border: #e4e0d8;
            --accent: #1a1a2e;
            --green: #1a6b3c;
            --amber: #b5611a;
            --red: #c0392b;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'DM Sans', sans-serif;
            background: var(--bg);
            color: var(--text-primary);
            line-height: 1.7;
            font-size: 15px;
        }}

        .page-wrapper {{
            max-width: 1080px;
            margin: 0 auto;
            padding: 52px 32px 80px;
        }}

        /* HEADER */
        .report-header {{
            margin-bottom: 40px;
            padding-bottom: 28px;
            border-bottom: 2px solid var(--accent);
        }}

        .report-header h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.4rem;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: -0.5px;
            margin-bottom: 10px;
        }}

        .report-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px 20px;
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 300;
        }}

        /* SECTION BLOCKS */
        .section-block {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 32px 36px;
            margin-bottom: 24px;
        }}

        .section-eyebrow {{
            font-size: 10px;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .section-block h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}

        /* EXECUTIVE BRIEF CARDS */
        .brief-card {{
            margin-bottom: 16px;
            border: 1px solid var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}

        .brief-card:last-child {{
            margin-bottom: 0;
        }}

        .brief-card-heading {{
            font-family: 'Playfair Display', serif;
            font-size: 1rem;
            font-weight: 700;
            color: var(--surface);
            background: var(--accent);
            padding: 12px 20px;
            letter-spacing: 0.3px;
        }}

        .brief-card-body {{
            padding: 4px 0;
        }}

        .brief-card-item {{
            padding: 12px 20px;
            font-size: 15.5px;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border);
            line-height: 1.7;
        }}

        .brief-card-item:last-child {{
            border-bottom: none;
        }}

        /* SCORECARD */
        .scorecard-group {{
            margin-bottom: 24px;
        }}

        .scorecard-group:last-child {{
            margin-bottom: 0;
        }}

        .scorecard-group-label {{
            font-size: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }}

        .scorecard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
        }}

        .score-card {{
            padding: 16px 18px;
            border-radius: 4px;
        }}

        .score-label {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .score-value {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 6px;
        }}

        .score-delta {{
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}

        .score-status {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .score-metric-type {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 400;
            margin-bottom: 4px;
            font-style: italic;
        }}

        /* COLLAPSIBLE */
        .collapsible-block {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            margin-bottom: 16px;
            overflow: hidden;
        }}

        .collapsible-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 22px 32px;
            cursor: pointer;
            user-select: none;
            transition: background 0.15s;
        }}

        .collapsible-header:hover {{
            background: #fafaf7;
        }}

        .collapsible-header-left {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .collapsible-header h3 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--accent);
        }}

        .collapsible-toggle {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}

        .collapsible-toggle .arrow {{
            display: inline-block;
            transition: transform 0.2s;
            font-size: 10px;
        }}

        .collapsible-toggle.open .arrow {{
            transform: rotate(180deg);
        }}

        .collapsible-content {{
            display: none;
            padding: 0 32px 32px;
            border-top: 1px solid var(--border);
        }}

        .collapsible-content.open {{
            display: block;
        }}

        /* TABLES */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0 0;
            font-size: 14px;
        }}

        th {{
            text-align: left;
            padding: 10px 14px;
            font-size: 10px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--text-muted);
            border-bottom: 2px solid var(--border);
            font-weight: 600;
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            color: var(--text-primary);
        }}

        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #fafaf8; }}

        /* NARRATIVE CARDS */
        .narrative-block {{
            margin-top: 28px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
        }}

        .narrative-label {{
            font-size: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 16px;
        }}

        .narrative-card {{
            border: 1px solid var(--border);
            border-radius: 4px;
            margin-bottom: 12px;
            overflow: hidden;
        }}

        .narrative-card:last-child {{
            margin-bottom: 0;
        }}

        .narrative-card-heading {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--surface);
            background: #2c3e6b;
            padding: 10px 18px;
        }}

        .narrative-card ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .narrative-card li {{
            font-size: 15.5px;
            color: var(--text-secondary);
            padding: 11px 18px;
            border-bottom: 1px solid var(--border);
            line-height: 1.7;
        }}

        .narrative-card li:last-child {{
            border-bottom: none;
        }}

        .narrative-card p {{
            font-size: 15.5px;
            color: var(--text-secondary);
            padding: 11px 18px;
            line-height: 1.7;
        }}

        .table-label {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 28px;
            margin-bottom: 4px;
        }}

        /* FOOTER */
        .report-footer {{
            margin-top: 52px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            color: var(--text-muted);
            font-size: 12px;
        }}
    </style>
</head>
<body>
<div class="page-wrapper">

    <header class="report-header">
        <h1>Executive Business Report</h1>
        <div class="report-meta">
            <span>Full Year 2026</span>
            <span>·</span>
            <span>Benchmark: 3-Year Historical Average (2023–2025)</span>
            <span>·</span>
            <span>AI-Generated Narrative</span>
        </div>
    </header>

    <section class="section-block">
        <div class="section-eyebrow">Executive Brief</div>
        <h2>Summary for Leadership</h2>
        {executive_brief_html}
    </section>

    <section class="section-block">
        <div class="section-eyebrow">Performance Scorecard</div>
        <h2>Metric Health at a Glance</h2>
        {scorecard_html}
    </section>

    <div class="collapsible-block">
        <div class="collapsible-header" onclick="toggleSection('category')">
            <div class="collapsible-header-left">
                <div class="section-eyebrow">Category Analysis</div>
                <h3>Performance by Product Category</h3>
            </div>
            <div class="collapsible-toggle" id="category-toggle">
                View Analysis <span class="arrow">▼</span>
            </div>
        </div>
        <div class="collapsible-content" id="category-content">
            {category_table}
            <div class="narrative-block">
                <div class="narrative-label">Detailed Analysis</div>
                {category_narrative_html}
            </div>
        </div>
    </div>

    <div class="collapsible-block">
        <div class="collapsible-header" onclick="toggleSection('region')">
            <div class="collapsible-header-left">
                <div class="section-eyebrow">Regional Analysis</div>
                <h3>Performance by Region</h3>
            </div>
            <div class="collapsible-toggle" id="region-toggle">
                View Analysis <span class="arrow">▼</span>
            </div>
        </div>
        <div class="collapsible-content" id="region-content">
            {region_table}
            <div class="narrative-block">
                <div class="narrative-label">Detailed Analysis</div>
                {region_narrative_html}
            </div>
        </div>
    </div>

    <div class="collapsible-block">
        <div class="collapsible-header" onclick="toggleSection('segment')">
            <div class="collapsible-header-left">
                <div class="section-eyebrow">Segment Analysis</div>
                <h3>Performance by Customer Segment</h3>
            </div>
            <div class="collapsible-toggle" id="segment-toggle">
                View Analysis <span class="arrow">▼</span>
            </div>
        </div>
        <div class="collapsible-content" id="segment-content">
            {segment_table}
            <div class="narrative-block">
                <div class="narrative-label">Detailed Analysis</div>
                {segment_narrative_html}
            </div>
        </div>
    </div>

    <div class="collapsible-block">
        <div class="collapsible-header" onclick="toggleSection('subcategory')">
            <div class="collapsible-header-left">
                <div class="section-eyebrow">Sub-Category Analysis</div>
                <h3>Top and Bottom Performers</h3>
            </div>
            <div class="collapsible-toggle" id="subcategory-toggle">
                View Analysis <span class="arrow">▼</span>
            </div>
        </div>
        <div class="collapsible-content" id="subcategory-content">
            <div class="table-label">Top 5 by Profit</div>
            {top5_table}
            <div class="table-label" style="margin-top:28px;">Bottom 5 by Profit</div>
            {bottom5_table}
            <div class="narrative-block">
                <div class="narrative-label">Detailed Analysis</div>
                {subcategory_narrative_html}
            </div>
        </div>
    </div>

    <footer class="report-footer">
        <span>Superstore Business Intelligence — Confidential</span>
        <span>Powered by AI Narrative Engine</span>
    </footer>

</div>

<script>
    function toggleSection(id) {{
        const content = document.getElementById(id + '-content');
        const toggle = document.getElementById(id + '-toggle');
        const isOpen = content.classList.contains('open');
        content.classList.toggle('open', !isOpen);
        toggle.classList.toggle('open', !isOpen);
        toggle.innerHTML = isOpen
            ? 'View Analysis <span class="arrow">▼</span>'
            : 'Hide Analysis <span class="arrow">▼</span>';
    }}
</script>

</body>
</html>"""

    return html


def save_report(html, path="outputs/report.html"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report saved to {path}")