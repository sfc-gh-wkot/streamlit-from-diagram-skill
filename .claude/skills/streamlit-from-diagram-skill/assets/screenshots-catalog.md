# Screenshot Catalog

This file catalogs the example dashboard screenshots demonstrating the wireframe-to-4-environment deployment workflow.

## How to Add Screenshots

Place screenshot images in this `assets/` folder with these names:
- `wireframe.png` — Original wireframe/sketch
- `localhost.png` — Streamlit running locally
- `sis-warehouse.png` — SiS Warehouse runtime
- `sis-container.png` — SiS Container runtime
- `spcs.png` — Raw SPCS service

---

## Screenshot 1: Wireframe (Starting Point)

**File:** `wireframe.png`

**Description:** Black and white wireframe sketch showing the dashboard layout structure.

**Key Elements:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ [Z] COMPANY | Property Name ▼    [Q Search]         (All) Profile Name ▼│
├────┬──────────────────────────────────────────────────────────────┬─────┤
│ ○  │ ┌─────────────────┐  Page Title                              │Tiles│
│ ○  │ │ Predictive Item │  sub paragraph                           │  ^  │
│ ○  │ │ ───────────────│                                          │     │
│ ○  │ │ ───────────────│  ┌─────────────────────────────────────┐ │[  ] │
│ ○  │ └─────────────────┘  │ ▌▌▐▌▐▐▌▌▐▌▐▐▌▐▐ (Bar Chart)        │ │[  ] │
│    │                      │                                     │ │     │
│    │ ┌─────────────────┐  └─────────────────────────────────────┘ │     │
│    │ │ Predictive Item │                                          │ ✦ Try│
│    │ │ ───────────────│  ┌─────────────────────────────────────┐ │ ✦ Try│
│    │ │ ───────────────│  │   ╱╲                                │ │     │
│    │ └─────────────────┘  │  ╱  ╲___╱╲___ (Line Chart)         │ │Enter│
│    │                      │                                     │ │Prompt│
│    │ ┌─────────────────┐  └─────────────────────────────────────┘ │[   ]│
│    │ │ Predictive Item │                                          │     │
│    │ │ ───────────────│  ┌──────────────┬──────────────┐         │[▷Run]│
│ ○  │ └─────────────────┘  │ (Pie Chart)  │ (Bar Chart)  │         │     │
└────┴──────────────────────┴──────────────┴──────────────┴─────────┴─────┘
```

**Design Intent:**
- 3-column layout: icon nav, content area, right panel
- Left sidebar with insight/predictive cards
- Main area with title, charts (bar, line, pie)
- Right panel with metrics, suggestions, prompt input
- Collapsible "Tiles" panel on far right

---

## Screenshot 2: Localhost (http://localhost:8501)

**File:** `localhost.png`

**URL:** `localhost:8501`

**Tab Shown:** Overview

**Visual Elements:**
- **Header:** "Z" logo, "COMPANY | Property Name", centered Search, "All" badge, "Profile Name"
- **Left Icons:** 5 circular icons, first one active (blue)
- **Sidebar:**
  - "🎛️ Filters" expander
  - Revenue Forecast card (📈 blue icon, Q4 projection: $128K, ↑23%)
  - [View Details] button
  - Churn Risk Alert card (⚠️ orange icon, 47 users, "Action needed")
  - [Review Users] button
  - Growth Opportunity card (🎯 green icon, +18%, "12 leads")
  - [View Leads] button
  - Anomaly Detected card (🔍 pink icon, +340%, "Social campaign")
  - [Investigate] button

- **Main Content:**
  - "📊 Dashboard" title
  - "Showing data for: Last 30 Days | Channels: Web, Mobile, API, Desktop, Other"
  - 4 icon buttons (💰 👥 📈 ⏱️)
  - KPI Row:
    - Total Revenue: $586,362 ↑13%
    - Active Users: 50,342 ↑8%
    - Conversion: 4.36% ↑0.3%
    - Avg. Session: 3m 28s ↑1.6%
  - Tabs: [📈 Overview] [📊 Breakdown] [📋 Data Table]
  - **Overview tab content:**
    - "Monthly Revenue" bar chart (blue + green bars for months Apr-Sep)
    - "Daily Trend" line chart (red line with points, dates 2024-Jan 21)
    - "Performance Comparison" multi-line chart (Series A blue, B light blue, C red)

- **Right Panel:**
  - TODAY'S VISITORS: 1,247 ↑12%
  - PENDING TASKS: 23, "5 due today"
  - AI SUGGESTIONS:
    - ✦ Optimize ad spend
    - ✦ Review churn users
    - ✦ Export Q4 report
  - "Enter Prompt" text area
  - [▷ Run] button (red)
  - "Recent Activity" expander

- **Far Right:** "Tiles" panel with 4 icons

---

## Screenshot 3: Raw SPCS (your-service-your-account.snowflakecomputing.app)

**File:** `spcs.png`

**URL:** `your-service-your-account.snowflakecomputing.app`

**Tab Shown:** Breakdown

**Notable Differences from Localhost:**
- URL shows `.snowflakecomputing.app` domain
- Dashboard link icon (🔗) next to title

**Breakdown Tab Content:**
- "Traffic by Device (click to filter)" — Stacked area chart
  - Desktop (blue), Mobile (red), Tablet (green)
  - X-axis: 2024, Fri 05, Tue 09, Sat 13
  - Y-axis: Traffic 0-120

- "Requests by Channel (click bars)" — Colored bar chart
  - Web (blue): ~320
  - Mobile (red): ~380
  - API (green): ~280
  - Desktop (orange): ~450
  - Other (purple): ~420
  - Y-axis: Requests 0-400

- "Channel Distribution" — Donut chart
  - Same 5 categories with matching colors
  - Legend on right side

**KPI Values (different from localhost - random data):**
- Total Revenue: $620,522 ↑5%
- Active Users: 64,526 ↑6%
- Conversion: 4.62% ↑0.8%
- Avg. Session: 4m 57s ↑0.9%

---

## Screenshot 4: SiS Warehouse (app.snowflake.com)

**File:** `sis-warehouse.png`

**URL:** `app.snowflake.com/YOUR_ORG/YOUR_ACCOUNT/#/streamlit-apps/YOUR_DB.YOUR_SCHEMA.YOUR_APP`

**Tab Shown:** Breakdown

**Snowflake UI Elements:**
- Snowflake sidebar (left) with navigation icons
- Breadcrumb: "Streamlit Apps > Zego Dashboard (Warehouse)"
- "Showing cache..." indicator
- [Share] [Edit] buttons in header

**App Content:** Identical to SPCS screenshot (Breakdown tab)

**KPI Values:**
- Total Revenue: $541,752 ↑12%
- Active Users: 61,323 ↑3%
- Conversion: 4.26% ↓1.0%
- Avg. Session: 3m 13s ↑1.1%

---

## Screenshot 5: SiS Container (app.snowflake.com)

**File:** `sis-container.png`

**URL:** `app.snowflake.com/YOUR_ORG/YOUR_ACCOUNT/#/streamlit-apps/YOUR_DB.YOUR_SCHEMA.YOUR_APP_CONTAINER`

**Tab Shown:** Overview

**Snowflake UI Elements:**
- Same Snowflake sidebar as Warehouse
- Breadcrumb: "SNOWFLAKE_LEARNING_DB.PUBLIC.ZEGO_DASHBOARD_CONTAINER"
- "Starting..." indicator (loading)
- Sidebar has "X" close button visible

**App Content:** Overview tab (same as localhost Screenshot 2)

**KPI Values:**
- Total Revenue: $531,400 ↑8%
- Active Users: 59,503 ↑7%
- Conversion: 3.91% ↓0.9%
- Avg. Session: 4m 36s ↑1.2%

**Important Note:** This environment uses older Streamlit (~1.35), so `st.column_config` is NOT available. Tables use pandas formatting instead.

---

## Visual Consistency Verification

All 4 environments show:

✅ Same layout structure (header, sidebar, main, right panel)
✅ Same color scheme (blue primary, red secondary, etc.)
✅ Same chart types (bar, line, area, pie)
✅ Same interactive elements (buttons, tabs, expanders)
✅ Matching chart colors via explicit Altair definitions

The only differences are:
- Random data values (different seeds)
- Snowflake UI frame in SiS environments
- Minor styling variations from Streamlit version differences
