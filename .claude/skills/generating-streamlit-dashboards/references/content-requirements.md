# Rich Content Requirements

Minimum content requirements for transforming wireframe elements into production-ready dashboard components.

## Contents

- [Overview](#overview)
- [Element Minimum Requirements](#element-minimum-requirements)
- [Content Transformation Examples](#content-transformation-examples)
- [Sidebar Card Transformations](#sidebar-card-transformations)
- [KPI Card Transformations](#kpi-card-transformations)
- [Chart Requirements](#chart-requirements)
- [Right Panel Elements](#right-panel-elements)
- [Sample Data Guidelines](#sample-data-guidelines)

---

## Overview

Every wireframe element represents REAL content. Transform every placeholder into specific, meaningful content with these 5 qualities:

| Quality | Description | Example |
|---------|-------------|---------|
| **Sample Data** | Realistic numbers, not placeholders | `$45,231` not `$XXX`, `2,345 users` not `N users` |
| **Visible Labels** | Axis labels, titles, legends on all charts | `title="Monthly Revenue"`, axis with "Apr, May, Jun..." |
| **Lightweight Interactivity** | Hover states, `.interactive()` on charts | `chart.interactive()`, CSS `:hover` effects |
| **Sample Content** | Domain-specific text that tells a story | "47 users at high risk" not "Some users need attention" |
| **Mock Clickability** | Buttons/links that appear actionable | "✦ Optimize ad spend", "▷ Run", action links with arrows |

---

## Element Minimum Requirements

| Element | Minimum Content Requirements |
|---------|------------------------------|
| Insight Cards | Icon + title + 2-3 metrics + action link |
| KPI Cards | Label + formatted value (`$1.24M`) + delta indicator (`+12%`) |
| Charts | Title above + axis labels + tooltips with formatting |
| Sidebar items | Icon + descriptive title + secondary text |
| Action buttons | Verb-noun format ("View Report", "Export Data") |

---

## Content Transformation Examples

### Generic Placeholder → Rich Content

**Wireframe shows:** Box with lines labeled "Predictive Item"

❌ **Bad output:**
```python
st.markdown("### Predictive Item")
st.markdown("Some text here")
```

✅ **Good output:**
```python
st.markdown("""
<div class="insight-card">
    <div class="icon">📈</div>
    <h4>Revenue Forecast</h4>
    <p class="metric">Q4 projection: $128K</p>
    <p class="delta positive">↑ 23% vs last quarter</p>
    <a href="#" class="action-link">View Details →</a>
</div>
""", unsafe_allow_html=True)
```

---

## Sidebar Card Transformations

| Wireframe | Bad Output | Good Output |
|-----------|------------|-------------|
| "Predictive Item" + lines | Generic card with placeholder text | **Revenue Forecast** — Q4 projection: $128K, ↑23% vs last quarter |
| "Predictive Item" + lines | Another generic card | **Churn Risk Alert** — 47 users at high risk, "Action needed this week" |
| "Predictive Item" + lines | Yet another generic | **Growth Opportunity** — Enterprise segment: +18%, "12 leads ready to convert" |
| "Predictive Item" + lines | Empty card | **Anomaly Detected** — Traffic spike: +340%, Source: Social campaign |

---

## KPI Card Transformations

| Wireframe | Bad Output | Good Output |
|-----------|------------|-------------|
| Box with lines | "Metric: Value" | **Total Revenue** $45,231 ↑+12.5% |
| Box with lines | "Users: Count" | **Active Users** 2,345 ↑+8.2% |
| Box with lines | "Rate: %" | **Conversion** 3.24% ↓-0.4% |
| Box with lines | "Time: Duration" | **Avg. Session** 4m 32s ↑+1.2% |

---

## Chart Requirements

Every chart MUST have title, axis labels, and tooltips:

```python
# ✅ Good chart - all labels visible
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:N", title="Month", axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("revenue:Q", title="Revenue ($K)", axis=alt.Axis(format="$,.0f")),
    tooltip=[
        alt.Tooltip("month:N", title="Month"),
        alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f")
    ]
).properties(
    title="Monthly Revenue"  # Chart title
).interactive()  # Enable zoom/pan
```

### Chart Checklist

- [ ] Title displayed above chart (via `st.markdown("**Title**")` or `.properties(title=)`)
- [ ] X-axis has descriptive title
- [ ] Y-axis has descriptive title with units
- [ ] Tooltips show formatted values
- [ ] `.interactive()` called for zoom/pan
- [ ] Explicit color set (not default)

---

## Right Panel Elements

| Wireframe | Good Output |
|-----------|-------------|
| Tiles/stat boxes | **TODAY'S VISITORS** 1,247 ↑12% vs yesterday |
| Tiles/stat boxes | **PENDING TASKS** 23, "5 due today" |
| "Try This" buttons | **AI SUGGESTIONS** — ✦ Optimize ad spend, ✦ Review churn users, ✦ Export Q4 report |
| "Enter Prompt" + Run | Text input with placeholder "Ask about your data..." + "▷ Run" button |
| Activity feed | **RECENT ACTIVITY** — 📊 Report generated 2m ago, 👤 New user signup 15m ago |

---

## Sample Data Guidelines

### KPI Values
- Use realistic, formatted numbers: `$45,231`, `2,345`, `3.24%`, `4m 32s`
- Include mix of positive and negative deltas
- Format consistently: `↑+12.5%` (positive), `↓-0.4%` (negative)

### Chart Data
- Generate 6-12 data points with realistic variation
- Use appropriate time ranges (months, days, hours)
- Include realistic value ranges for the domain

### Activity Feed
- Use relative timestamps: "2m ago", "15m ago", "1h ago", "Yesterday"
- Include varied activity types with appropriate icons
- Show realistic usernames or system actions

### Domain-Specific Content

Select content appropriate to the wireframe context:

| Context | Sample Content Areas |
|---------|---------------------|
| Finance Dashboard | Revenue, expenses, margins, forecasts |
| Analytics | Traffic, conversions, sessions, bounce rate |
| Sales | Pipeline, deals, quotas, win rates |
| Operations | Uptime, incidents, deployments, SLAs |
| HR | Headcount, turnover, satisfaction, hiring |

---

## Verification Checklist

After generating a dashboard, verify:

- [ ] No raw HTML visible on page (all `st.markdown` renders correctly)
- [ ] All charts have visible axis labels (not column names like "order")
- [ ] All cards have meaningful content (not "Predictive Item" or "Value")
- [ ] Navigation icons are clickable with visual feedback
- [ ] AI suggestion buttons show response on click
- [ ] Prompt input + Run button functional with mock response
- [ ] All numbers formatted ($45,231 not 45231)
- [ ] Delta indicators colored (green for positive, red for negative)
