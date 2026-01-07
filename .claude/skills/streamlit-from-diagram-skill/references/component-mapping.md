# Visual Element to Streamlit Component Mapping

## ⚠️ CRITICAL RULE: Never Generate Placeholders

Every wireframe element represents REAL content. Transform every placeholder into specific, meaningful content.

**Example Transformation:**

| Wireframe Shows | ❌ WRONG Output | ✅ CORRECT Output |
|-----------------|-----------------|-------------------|
| "Predictive Item" box with lines | Generic "Predictive Item" card with gray lines | "Revenue Forecast" card with "Q4: $128K", "↑23%" |
| Bar chart frame | Unlabeled bars | "Monthly Revenue" chart with axis labels |
| Metric box | Empty or "Value" | "TODAY'S VISITORS: 1,247 ↑12%" |
| "Try This" button | Button saying "Try This" | Button saying "✦ Optimize ad spend" |

## Layout Elements

| Visual Element | Streamlit Component | REQUIRED Content |
|----------------|---------------------|------------------|
| Sidebar | `st.sidebar` | Filters, insight cards with real data |
| Header bar | `st.markdown()` + CSS | Logo, company name, search, profile |
| **Left icon nav (circles)** | `st.markdown()` + CSS | **4-5 circular icons, one active** |
| **Right tiles panel** | `st.markdown()` + CSS | **Collapsible with < arrow** |
| Multi-column | `st.columns([ratio, ratio])` | Content in BOTH columns |
| Tabs | `st.tabs(["Overview", "Details"])` | Named tabs with content |
| Expander | `st.expander("Filters")` | Working filter controls |
| Container | `st.container()` | Grouped related elements |
| Divider | `st.divider()` | Visual separation |
| **Dark/Light toggle** | `st.toggle()` | Theme switcher |

## MANDATORY Edge Navigation Elements

### Left Icon Navigation (ALWAYS INCLUDE)

When wireframe shows circles on the left edge:

```python
# At start of app, after page_config
st.markdown("""
<div class="icon-nav-header">
    <div class="nav-logo">Z</div>
</div>
<div class="icon-nav">
    <div class="icon-nav-item active" title="Dashboard">📊</div>
    <div class="icon-nav-item" title="Analytics">📈</div>
    <div class="icon-nav-item" title="Reports">📋</div>
    <div class="icon-nav-item" title="Users">👥</div>
    <div class="icon-nav-item" title="Settings">⚙️</div>
</div>
""", unsafe_allow_html=True)
```

### Right Tiles Panel (ALWAYS INCLUDE)

When wireframe shows "Tiles" or vertical bar on right:

```python
# At END of app, after all other content
st.markdown("""
<div class="tiles-panel">
    <div class="tiles-collapse" title="Collapse">‹</div>
    <div class="tiles-tab-label">Tiles</div>
    <div class="tiles-icons">
        <div class="tiles-icon" title="Chart View">📊</div>
        <div class="tiles-icon" title="Table View">📋</div>
        <div class="tiles-icon" title="Map View">🗺️</div>
        <div class="tiles-icon" title="Settings">⚙️</div>
    </div>
</div>
""", unsafe_allow_html=True)
```

### Complete CSS for Both Panels

```python
st.markdown("""
<style>
/* Icon Navigation Header (top-left corner) */
.icon-nav-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 48px;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
    border-right: 1px solid #e5e5e5;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
}

.icon-nav-header .nav-logo {
    width: 28px;
    height: 28px;
    border: 2px solid #1a1a1a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
}

/* Left Icon Navigation */
.icon-nav {
    position: fixed;
    left: 0;
    top: 56px;
    bottom: 0;
    width: 48px;
    background: #ffffff;
    border-right: 1px solid #e5e5e5;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 16px;
    gap: 8px;
    z-index: 999998;
}

.icon-nav-item {
    width: 32px;
    height: 32px;
    border: 2px solid #d0d0d0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: transparent;
    font-size: 14px;
    transition: all 0.2s ease;
}

.icon-nav-item.active {
    border-color: #2196f3;
    background: #e3f2fd;
}

.icon-nav-item:hover {
    border-color: #2196f3;
    transform: scale(1.05);
}

/* Right Tiles Panel */
.tiles-panel {
    position: fixed;
    right: 0;
    top: 56px;
    bottom: 0;
    width: 40px;
    background: #f5f5f5;
    border-left: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 8px;
    z-index: 100;
}

.tiles-collapse {
    cursor: pointer;
    font-size: 16px;
    color: #666;
    margin-bottom: 4px;
    padding: 4px;
}

.tiles-collapse:hover {
    color: #2196f3;
}

.tiles-tab-label {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 12px;
    color: #666;
    font-weight: 500;
    padding: 8px 0;
    cursor: pointer;
}

.tiles-icons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 20px;
}

.tiles-icon {
    width: 24px;
    height: 24px;
    background: #e0e0e0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.tiles-icon:hover {
    background: #2196f3;
    color: white;
}

/* Adjust sidebar position for icon-nav */
[data-testid="stSidebar"] {
    top: 56px !important;
    left: 48px !important;
    height: calc(100vh - 56px) !important;
}

/* Adjust main content for panels */
.block-container {
    padding-right: 50px !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
```

## Charts and Visualizations

| Visual Element | Recommended Component | AVOID |
|----------------|----------------------|-------|
| Bar chart | `alt.Chart().mark_bar()` | ❌ `st.bar_chart()` |
| Line chart | `alt.Chart().mark_line()` | ❌ `st.line_chart()` |
| Area chart | `alt.Chart().mark_area()` | ❌ `st.area_chart()` |
| Scatter plot | `alt.Chart().mark_circle()` | ❌ `st.scatter_chart()` |
| Pie/Donut | `alt.Chart().mark_arc()` | N/A |
| Heatmap | `alt.Chart().mark_rect()` | N/A |
| Map | `st.map()` or `pydeck` | Basic maps only in SiS |

### Altair Chart Pattern (Always Use)

```python
import altair as alt

# Define explicit colors for consistency
CHART_COLORS = {
    "primary": "#4A90D9",
    "secondary": "#E57373", 
    "success": "#81C784",
    "warning": "#FFB74D",
    "accent": "#9575CD"
}

chart = alt.Chart(df).mark_bar(
    color=CHART_COLORS["primary"],  # ALWAYS explicit color
    cursor="pointer"  # For interactivity
).encode(
    x=alt.X("category:N", sort=None, title=None),
    y=alt.Y("value:Q", title="Value"),
    tooltip=["category", "value"]  # Add tooltips
).properties(
    height=200
).interactive()  # Enable zoom/pan

st.altair_chart(chart, use_container_width=True)
```

## Data Display

| Visual Element | Recommended Component | AVOID |
|----------------|----------------------|-------|
| Data table | `st.dataframe()` | ❌ `column_config` parameter |
| Sortable table | `st.dataframe()` | Built-in sorting |
| Metric card | `st.metric()` | Works everywhere |
| JSON viewer | `st.json()` | Works everywhere |
| Code block | `st.code()` | Works everywhere |

### Table Formatting Pattern

```python
# ✅ CORRECT - Format with pandas, not column_config
display_df = df.copy()
display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,.0f}")
display_df["Percentage"] = display_df["Percentage"].apply(lambda x: f"{x:.1%}")
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(display_df, use_container_width=True, height=300)

# ❌ WRONG - column_config breaks in SiS Container
# st.dataframe(df, column_config={
#     "Revenue": st.column_config.NumberColumn(format="$%d")
# })
```

## Input Widgets

| Visual Element | Streamlit Component | Notes |
|----------------|---------------------|-------|
| Text input | `st.text_input()` | Single line |
| Text area | `st.text_area()` | Multi-line |
| Number input | `st.number_input()` | With step/range |
| Date picker | `st.date_input()` | ✅ Works in all |
| Date range | `st.date_input()` with tuple | Pass 2 dates |
| Dropdown | `st.selectbox()` | Single select |
| Multi-select | `st.multiselect()` | Multiple select |
| Slider | `st.slider()` | Range support |
| Checkbox | `st.checkbox()` | Boolean toggle |
| Radio | `st.radio()` | Single choice |
| Button | `st.button()` | Action trigger |
| Toggle | `st.toggle()` | Boolean switch |
| File upload | `st.file_uploader()` | Limited in SiS |
| Color picker | `st.color_picker()` | Works everywhere |

## Interactive Elements

| Visual Element | Streamlit Component | Notes |
|----------------|---------------------|-------|
| Clickable card | Custom HTML + `st.button()` | See pattern below |
| Download button | `st.download_button()` | Works in all |
| Link button | `st.link_button()` | External links |
| Progress bar | `st.progress()` | Animated |
| Spinner | `st.spinner()` | Loading state |
| Status messages | `st.success/warning/error/info()` | Alerts |
| Toast | `st.toast()` | Pop-up notification |
| Balloons | `st.balloons()` | Celebration |

### Clickable Card Pattern

```python
# Custom styled card with button
st.markdown("""
<div class="custom-card">
    <h4>Card Title</h4>
    <p>Card description text</p>
    <p class="metric">$12,345</p>
</div>
""", unsafe_allow_html=True)

if st.button("View Details", key="card_1"):
    st.session_state.selected_card = "card_1"
```

## Sidebar Insight Cards (FULL PATTERN)

When wireframe shows "Predictive Item" or similar card placeholders, generate FULLY POPULATED cards:

### Card Template (Generate 4 Unique Cards)

```python
# Card 1: Revenue Forecast
st.markdown("""
<div class="insight-card">
    <div class="card-icon" style="background: #2196F3;">📈</div>
    <div class="card-content">
        <div class="card-title">Revenue Forecast</div>
        <div class="card-detail">Q4 projection: $128K</div>
        <div class="card-action positive">↑ 23% vs last quarter</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.button("View Details", key="revenue", use_container_width=True)

# Card 2: Churn Risk Alert
st.markdown("""
<div class="insight-card">
    <div class="card-icon" style="background: #FF9800;">⚠️</div>
    <div class="card-content">
        <div class="card-title">Churn Risk Alert</div>
        <div class="card-detail">47 users at high risk</div>
        <div class="card-action warning">Action needed this week</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.button("Review Users", key="churn", use_container_width=True)

# Card 3: Growth Opportunity
st.markdown("""
<div class="insight-card">
    <div class="card-icon" style="background: #4CAF50;">🎯</div>
    <div class="card-content">
        <div class="card-title">Growth Opportunity</div>
        <div class="card-detail">Enterprise segment: +18%</div>
        <div class="card-action positive">12 leads ready to convert</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.button("View Leads", key="growth", use_container_width=True)

# Card 4: Anomaly Detected
st.markdown("""
<div class="insight-card">
    <div class="card-icon" style="background: #E91E63;">🔍</div>
    <div class="card-content">
        <div class="card-title">Anomaly Detected</div>
        <div class="card-detail">Traffic spike: +340%</div>
        <div class="card-action">Source: Social campaign</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.button("Investigate", key="anomaly", use_container_width=True)
```

## Right Panel Pattern (OFTEN MISSED!)

When wireframe shows a right panel with boxes, ALWAYS generate complete content:

```python
# Create right column
left_main, right_panel = st.columns([4, 1])

with right_panel:
    # Metric Card 1
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">TODAY'S VISITORS</div>
        <div class="stat-value">1,247</div>
        <div class="stat-delta positive">↑ 12% vs yesterday</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metric Card 2
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">PENDING TASKS</div>
        <div class="stat-value">23</div>
        <div class="stat-delta warning">5 due today</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Suggestions Section
    st.markdown("**AI SUGGESTIONS**")
    if st.button("✦ Optimize ad spend", use_container_width=True):
        st.toast("Analyzing ad spend patterns...")
    if st.button("✦ Review churn users", use_container_width=True):
        st.toast("Loading churn analysis...")
    if st.button("✦ Export Q4 report", use_container_width=True):
        st.toast("Generating report...")
    
    st.markdown("---")
    
    # Prompt Section
    st.markdown("**Enter Prompt**")
    user_prompt = st.text_area(
        "", 
        placeholder="Ask about your data...",
        height=80,
        label_visibility="collapsed"
    )
    if st.button("▷ Run", type="primary", use_container_width=True):
        if user_prompt:
            st.toast(f"Processing: {user_prompt[:30]}...")
    
    st.markdown("---")
    
    # Recent Activity
    with st.expander("Recent Activity", expanded=False):
        st.markdown("""
        📊 **Report generated** • 2m ago  
        👤 **New user signup** • 15m ago  
        💰 **Payment received** • 1h ago  
        🔔 **Alert resolved** • 2h ago
        """)
```

## Chart with Title Pattern (MANDATORY)

Every chart MUST have a title, axis labels, and tooltips:

```python
# ✅ CORRECT: Full chart with all required elements
st.markdown("**Monthly Revenue**")  # TITLE (required)

chart_data = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [42000, 48000, 51000, 47000, 55000, 62000]
})

chart = alt.Chart(chart_data).mark_bar(
    color="#4A90D9",  # EXPLICIT COLOR (required)
    cornerRadiusTopLeft=4,
    cornerRadiusTopRight=4
).encode(
    x=alt.X("month:N", title="Month", sort=None),  # AXIS LABEL (required)
    y=alt.Y("revenue:Q", title="Revenue ($)"),     # AXIS LABEL (required)
    tooltip=[
        alt.Tooltip("month:N", title="Month"),
        alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f")  # TOOLTIP (required)
    ]
).properties(height=250)

st.altair_chart(chart, use_container_width=True)
```

## Layout Examples

### Dashboard Header

```python
st.markdown("""
<div class="dashboard-header">
    <div class="logo">COMPANY</div>
    <div class="title">Dashboard Title</div>
    <div class="user-info">User Name</div>
</div>
""", unsafe_allow_html=True)
```

### KPI Row

```python
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Revenue", "$125,000", "+12%")
with col2:
    st.metric("Users", "1,234", "+5%")
with col3:
    st.metric("Conversion", "3.2%", "-0.5%")
with col4:
    st.metric("Sessions", "45,678", "+8%")
```

### Sidebar with Filters

```python
with st.sidebar:
    st.header("Filters")
    
    with st.expander("Date Range", expanded=True):
        date_range = st.date_input(
            "Select dates",
            value=(datetime.today() - timedelta(days=30), datetime.today())
        )
    
    with st.expander("Categories", expanded=True):
        categories = st.multiselect(
            "Select categories",
            ["A", "B", "C", "D"],
            default=["A", "B", "C", "D"]
        )
```

### Tabbed Content

```python
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Settings"])

with tab1:
    # Overview content
    st.write("Overview charts and metrics")

with tab2:
    # Detailed tables
    st.write("Detailed data tables")

with tab3:
    # Settings
    st.write("Configuration options")
```

## CSS Styling

### Custom Theme Variables

```python
st.markdown("""
<style>
:root {
    --primary: #4A90D9;
    --secondary: #E57373;
    --success: #81C784;
    --warning: #FFB74D;
    --text: #1a1a1a;
    --background: #f8f9fa;
    --border: #e5e5e5;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom card styling */
.custom-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}

.custom-card:hover {
    border-color: var(--primary);
    box-shadow: 0 2px 8px rgba(74, 144, 217, 0.15);
}
</style>
""", unsafe_allow_html=True)
```
