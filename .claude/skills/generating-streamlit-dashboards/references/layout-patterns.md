# Layout Patterns

Complete patterns for edge navigation, panels, and sidebar elements.

## Contents

- [Left Icon Navigation](#left-icon-navigation)
- [Right Tiles Panel](#right-tiles-panel)
- [Sidebar Insight Cards](#sidebar-insight-cards)
- [Right Panel Pattern](#right-panel-pattern)
- [Dashboard Header](#dashboard-header)
- [KPI Row](#kpi-row)
- [Tabbed Content](#tabbed-content)

---

## Left Icon Navigation

When wireframe shows circles on the left edge, generate this pattern:

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

---

## Right Tiles Panel

When wireframe shows "Tiles" or vertical bar on right edge:

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

---

## Sidebar Insight Cards

When wireframe shows "Predictive Item" or similar card placeholders, generate FULLY POPULATED cards.

### Card Template (Generate 4 Unique Cards)

```python
with st.sidebar:
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

---

## Right Panel Pattern

When wireframe shows a right panel with boxes:

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

---

## Dashboard Header

```python
st.markdown("""
<div class="dashboard-header">
    <div class="logo">COMPANY</div>
    <div class="title">Dashboard Title</div>
    <div class="user-info">User Name</div>
</div>
""", unsafe_allow_html=True)
```

---

## KPI Row

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

---

## Tabbed Content

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

---

## Sidebar with Filters

```python
from datetime import datetime, timedelta

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
