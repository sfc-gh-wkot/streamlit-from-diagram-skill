# Example Dashboard: Wireframe to 4-Environment Deployment

This reference documents a complete example of transforming a wireframe into a production Streamlit dashboard deployed across all 4 environments.

## Starting Point: Wireframe

The initial wireframe defines the layout structure:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Z] COMPANY | Property Name ▼    [    Search    ]    (All) Profile Name │
├────┬──────────────────┬─────────────────────────────────────┬───────────┤
│    │                  │                                     │           │
│ ○  │ Predictive Item  │  Page Title                        │ [metric]  │
│ ○  │ ───────────────  │  sub paragraph                     │ [metric]  │
│ ○  │ ───────────────  │                                    │           │
│ ○  │ ───────────────  │  ┌─────────────────────────────┐   │ ───────── │
│    │                  │  │   ▌▌▐▌▐▐▌▌▐▌▐▐▌▐▐           │   │ ───────── │
│    ├──────────────────┤  │   Bar Chart                  │   ├───────────┤
│    │ Predictive Item  │  │                              │   │ ✦ Try This│
│    │ ───────────────  │  └─────────────────────────────┘   │ ✦ Try This│
│    │ ───────────────  │                                    │           │
│    │                  │  ┌─────────────────────────────┐   │ Enter     │
│    ├──────────────────┤  │   ╱╲                        │   │ Prompt    │
│    │ Predictive Item  │  │  ╱  ╲___╱╲___              │   │ [       ] │
│    │ ───────────────  │  │ Line Chart                  │   │ [▷ Run]   │
│    │ ───────────────  │  └─────────────────────────────┘   │           │
│    │                  │                                    │           │
│ ○  │                  │  ┌─────────────┬─────────────┐     │           │
└────┴──────────────────┴──│ Pie Chart   │ Other Chart │─────┴───────────┘
                           └─────────────┴─────────────┘
```

### Wireframe Analysis

**Layout Structure:**
- Fixed top navigation bar with logo, company/property selector, search, profile
- Left icon sidebar (5 circular icons for navigation)
- Left sidebar panel with "Predictive Item" insight cards
- Main content area with page title, charts
- Right sidebar with metrics, suggestions, prompt input
- Right edge "Tiles" panel

**UI Components Identified:**
1. Header: Company branding, search bar, user profile
2. Navigation: Icon-based sidebar with 5 items
3. Insight Cards: 3 cards with title + description text
4. Main Charts: Bar chart, line chart, pie/donut chart
5. Right Panel: Metric cards, action buttons, text input, run button

## ⚠️ Wireframe → Real Content Transformation

**The key insight:** Every wireframe placeholder line represents REAL content.

### Sidebar Card Transformation

```
WIREFRAME:                          GENERATED:
┌────────────────────┐              ┌────────────────────┐
│ Predictive Item    │  ────────►   │ 📈 Revenue Forecast │
│ ────────────────── │  ────────►   │ Q4 projection: $128K│
│ ────────────────── │  ────────►   │ ↑ 23% vs last qtr   │
│ ────────────────── │  ────────►   │ [View Details]      │
└────────────────────┘              └────────────────────┘
```

**Each line → specific content:**
- Line 1: Title → "Revenue Forecast" 
- Line 2: Detail → "Q4 projection: $128K"
- Line 3: Action text → "↑ 23% vs last quarter"
- Implicit: Button → "View Details"

### Chart Transformation

```
WIREFRAME:                          GENERATED:
┌─────────────────────┐             ┌─────────────────────┐
│                     │             │ **Monthly Revenue** │ ← Title added
│   ▌▌▐▌▐▐▌▌▐▌▐▐    │  ────────►  │                     │
│   Bar Chart         │             │   ▌▌▐▌▐▐▌▌▐▌▐▐    │
│                     │             │  Jan Feb Mar Apr... │ ← Axis labels
└─────────────────────┘             │     Revenue ($)     │ ← Y-axis
                                    └─────────────────────┘
```

### Right Panel Transformation

```
WIREFRAME:                          GENERATED:
┌────────────────┐                  ┌────────────────┐
│ [metric box]   │                  │ TODAY'S VISITORS│
│ ────────────── │     ────────►    │     1,247       │
│                │                  │ ↑ 12% vs yesterday│
├────────────────┤                  ├────────────────┤
│ [metric box]   │                  │ PENDING TASKS  │
│ ────────────── │     ────────►    │      23        │
│                │                  │  5 due today   │
├────────────────┤                  ├────────────────┤
│ ✦ Try This     │     ────────►    │ ✦ Optimize ad  │
│ ✦ Try This     │     ────────►    │ ✦ Review churn │
├────────────────┤                  ├────────────────┤
│ Enter Prompt   │                  │ Enter Prompt   │
│ [          ]   │     ────────►    │ [Ask about...] │
│ [▷ Run]        │                  │ [▷ Run]        │
└────────────────┘                  └────────────────┘
```

### Complete Card Content Template

For EACH "Predictive Item" card in wireframe, generate unique content:

| Card # | Icon | Title | Metric Line | Action Line | Button |
|--------|------|-------|-------------|-------------|--------|
| 1 | 📈 | Revenue Forecast | Q4 projection: $128K | ↑ 23% vs last quarter | View Details |
| 2 | ⚠️ | Churn Risk Alert | 47 users at high risk | Action needed this week | Review Users |
| 3 | 🎯 | Growth Opportunity | Enterprise segment: +18% | 12 leads ready to convert | View Leads |
| 4 | 🔍 | Anomaly Detected | Traffic spike: +340% | Source: Social campaign | Investigate |

## Implemented Dashboard

### Final Layout (All 4 Environments)

The wireframe was transformed into a fully functional interactive dashboard:

### ⚠️ MANDATORY ELEMENTS (Always Include)

| Element | Purpose | Implementation |
|---------|---------|----------------|
| **Left Icon Nav** | Quick access to main sections | Fixed position, 48px wide, circular icons |
| **Top Navbar** | Branding, search, profile | Fixed, 56px height |
| **Right Tiles Panel** | Quick actions, collapsible | Fixed, 40px wide, vertical label |
| **Theme Toggle** | Dark/light mode | `st.toggle("🌙 Dark Mode")` in sidebar |

**Header Section:**
- Logo "Z" with company branding
- "COMPANY | Property Name" text
- Centered search input
- "All" badge + "Profile Name"

**Left Icon Navigation (MANDATORY):**
- 5 circular icons (Dashboard, Analytics, Reports, Users, Settings)
- First icon highlighted as active
- Fixed position on left edge
- Hover effects for interactivity

**Right Tiles Panel (MANDATORY):**
- Collapse arrow "<" at top
- "Tiles" vertical text label
- 4 icon buttons (Chart, Table, Map, Settings)
- Fixed position on right edge

**Left Sidebar (Collapsible):**
```
🎛️ Filters (collapsible)
├── Date Range dropdown
├── Channels multi-select
└── Primary Metric radio

📈 Revenue Forecast
├── Q4 projection: $128K
├── ↑ 23% vs last quarter
└── [View Details] button

⚠️ Churn Risk Alert
├── 47 users at high risk
├── Action needed this week
└── [Review Users] button

🎯 Growth Opportunity
├── Enterprise segment: +18%
├── 12 leads ready to convert
└── [View Leads] button

🔍 Anomaly Detected
├── Traffic spike: +340%
├── Source: Social campaign
└── [Investigate] button

📤 Export Data (collapsible)
├── Format dropdown
└── [Download Report] button
```

**Main Content Area:**

*KPI Metrics Row:*
| 💰 Total Revenue | 👥 Active Users | 📈 Conversion | ⏱️ Avg. Session |
|------------------|-----------------|---------------|-----------------|
| $586,362 ↑13%   | 50,342 ↑8%      | 4.36% ↑0.3%   | 3m 28s ↑1.6%   |

*Tabbed Content:*
- **Overview Tab:** Monthly Revenue (bar), Daily Trend (line), Performance Comparison (multi-line)
- **Breakdown Tab:** Traffic by Device (stacked area), Requests by Channel (colored bars), Channel Distribution (donut)
- **Data Table Tab:** Sortable table with Download CSV button

**Right Sidebar:**
```
TODAY'S VISITORS
1,247
↑ 12% vs yesterday

PENDING TASKS
23
5 due today

AI SUGGESTIONS
├── ✦ Optimize ad spend
├── ✦ Review churn users
└── ✦ Export Q4 report

Enter Prompt
[Ask about your data...]
[▷ Run]

📋 Recent Activity (expandable)
├── 📊 Report generated • 2m ago
├── 👤 New user signup • 15m ago
└── ...
```

**Right Edge Panel:**
- "Tiles" label (vertical text)
- 4 icon buttons (📊 📋 🗺️ ⚙️)

## Visual Comparison Across Environments

### Environment 1: Localhost (http://localhost:8501)

**Characteristics:**
- Streamlit 1.51.0 (full features)
- Blue/green bar chart colors via explicit Altair
- All interactive features work
- Fast hot-reload during development
- No network restrictions

**Screenshot shows:** Overview tab with Monthly Revenue (blue/green bars), Daily Trend (red line with points), Performance Comparison (3-series line chart)

### Environment 2: Raw SPCS (your-service-your-account.snowflakecomputing.app)

**Characteristics:**
- Streamlit 1.51.0 (custom Docker)
- Full control via uv package management
- Same visual appearance as localhost
- Runs on Snowflake compute pool

**Screenshot shows:** Breakdown tab with Traffic by Device (stacked area with Desktop/Mobile/Tablet), Requests by Channel (5 colored bars), Channel Distribution (donut chart with legend)

### Environment 3: SiS Warehouse (app.snowflake.com/.../ZEGO_DASHBOARD)

**Characteristics:**
- Streamlit 1.51.0 via Snowflake Anaconda
- Snowflake UI frame around app
- "Showing cache..." indicator
- Share/Edit buttons in header

**Screenshot shows:** Breakdown tab - identical to SPCS version, confirming visual consistency

### Environment 4: SiS Container (app.snowflake.com/.../ZEGO_DASHBOARD_CONTAINER)

**Characteristics:**
- Older Streamlit (~1.35)
- More limited features
- `st.column_config` NOT available
- "Starting..." indicator visible

**Screenshot shows:** Overview tab - same layout, pandas-formatted table columns (not column_config)

## Key Implementation Details

### Altair Charts (Explicit Colors)

All charts use hardcoded colors for cross-environment consistency:

```python
CHART_COLORS = {
    "primary": "#4A90D9",    # Blue (Web)
    "secondary": "#E57373",  # Red (Mobile)
    "success": "#81C784",    # Green (API)
    "warning": "#FFB74D",    # Orange (Desktop)
    "accent": "#9575CD",     # Purple (Other)
}

# Bar chart with explicit color
bar_chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(...)

# Multi-category with color scale
channel_chart = alt.Chart(df).mark_bar().encode(
    color=alt.Color("category:N", scale=alt.Scale(
        domain=["Web", "Mobile", "API", "Desktop", "Other"],
        range=["#4A90D9", "#E57373", "#81C784", "#FFB74D", "#9575CD"]
    ))
)
```

### Table Formatting (No column_config)

```python
# Works in ALL environments
display_df = table_data.copy()
display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,}")
display_df["Bounce Rate"] = display_df["Bounce Rate"].apply(lambda x: f"{x:.0%}")
display_df["Conversion"] = display_df["Conversion"].apply(lambda x: f"{x:.2%}")
st.dataframe(display_df, use_container_width=True, height=300)
```

### Custom CSS Styling

```python
st.markdown("""
<style>
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Fixed navigation */
.top-navbar {
    position: fixed;
    top: 0;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
}

/* Sidebar cards */
.sidebar-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 12px;
    cursor: pointer;
}
.sidebar-card:hover {
    border-color: #2196f3;
}
</style>
""", unsafe_allow_html=True)
```

## Files Structure

```
project/
├── streamlit_app.py          # 845 lines, all UI logic
├── pyproject.toml            # uv deps (Streamlit 1.51.0)
├── environment.yml           # Conda deps (snowflake channel)
├── requirements.txt          # pip deps (SiS Container)
├── snowflake.yml             # snow CLI project definition
└── spcs/
    ├── Dockerfile            # python:3.11-slim + uv
    ├── spec.yaml             # SPCS service spec
    └── requirements-spcs.txt # SPCS deps
```

## Deployment Results

| Environment | URL | Streamlit | Status |
|-------------|-----|-----------|--------|
| Localhost | http://localhost:8501 | 1.51.0 | ✅ Running |
| SiS Warehouse | app.snowflake.com/.../ZEGO_DASHBOARD | 1.51.0 | ✅ Deployed |
| SiS Container | app.snowflake.com/.../ZEGO_DASHBOARD_CONTAINER | ~1.35 | ✅ Deployed |
| Raw SPCS | your-service-your-account.snowflakecomputing.app | 1.51.0 | ✅ Running |

## Lessons Learned

1. **Chart Colors:** Default `st.bar_chart()` produced different colors across environments. Solution: Use explicit Altair charts with hardcoded colors.

2. **Table Formatting:** `st.column_config` broke in SiS Container. Solution: Format data with pandas before passing to `st.dataframe()`.

3. **SPCS Architecture:** Must build Docker images with `--platform linux/amd64` for Snowflake.

4. **Compute Pools:** Cannot use `SYSTEM_COMPUTE_POOL_CPU` for raw SPCS services - must create custom pool.

5. **Docker Auth:** Use `snow spcs image-registry login` instead of direct `docker login` for Snowflake registries.
