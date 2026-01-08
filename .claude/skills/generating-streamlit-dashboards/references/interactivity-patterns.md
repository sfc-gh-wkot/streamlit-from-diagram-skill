# Interactivity Patterns

Common patterns for adding interactivity to Streamlit dashboards without external APIs.

## Contents

- [Session State Basics](#session-state-basics)
- [Expandable Cards](#expandable-cards)
- [Mock Response Patterns](#mock-response-patterns)
- [Prompt Input with Callbacks](#prompt-input-with-callbacks)
- [Chart Interactivity](#chart-interactivity)
- [Navigation State](#navigation-state)
- [Filter Controls](#filter-controls)

---

## Session State Basics

Streamlit reruns the entire script on every interaction. Use `st.session_state` to persist values.

```python
# Initialize state (runs only once per session)
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Modify state
if st.button("Increment"):
    st.session_state.counter += 1

# Read state
st.write(f"Count: {st.session_state.counter}")
```

**Key rules:**
- Always check `if "key" not in st.session_state` before initializing
- State persists across reruns but not across browser tabs
- Use unique keys for each stateful element

---

## Expandable Cards

Toggle card details with session state.

```python
# Initialize expanded state for multiple cards
def init_card_states(cards: list):
    for i, card in enumerate(cards):
        key = f"card_{i}_expanded"
        if key not in st.session_state:
            st.session_state[key] = False

# Render expandable card
def render_expandable_card(card: dict, index: int):
    key = f"card_{index}_expanded"
    is_expanded = st.session_state.get(key, False)
    
    # Card header (always visible)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{card['title']}**")
        st.caption(card['subtitle'])
    with col2:
        if st.button("▼" if not is_expanded else "▲", key=f"btn_{index}"):
            st.session_state[key] = not is_expanded
            st.rerun()
    
    # Card details (conditional)
    if is_expanded:
        st.markdown(card['details'])
        if card.get('metrics'):
            cols = st.columns(len(card['metrics']))
            for col, metric in zip(cols, card['metrics']):
                col.metric(metric['label'], metric['value'])

# Usage
cards = [
    {
        "title": "Revenue Forecast",
        "subtitle": "Q4 2024 projection",
        "details": "Based on current trends, revenue is expected to grow 15% YoY.",
        "metrics": [
            {"label": "Projected", "value": "$1.24M"},
            {"label": "Confidence", "value": "87%"}
        ]
    },
    # ... more cards
]

init_card_states(cards)
for i, card in enumerate(cards):
    render_expandable_card(card, i)
    st.divider()
```

---

## Mock Response Patterns

Simulate API responses for prototypes and demos.

```python
# Define mock responses
MOCK_RESPONSES = {
    "analyze_trends": {
        "message": "📊 **Trend Analysis Complete**\n\nKey findings:\n- Revenue up 23% vs last quarter\n- Customer acquisition cost down 12%\n- Churn rate stable at 2.3%",
        "data": {"trend": "positive", "confidence": 0.87}
    },
    "export_data": {
        "message": "✅ **Export Successful**\n\nData exported to `report_2024.csv`\n- 1,247 records\n- 15 columns\n- File size: 2.3 MB",
        "data": {"filename": "report_2024.csv", "rows": 1247}
    },
    "generate_forecast": {
        "message": "🔮 **Forecast Generated**\n\nNext 30 days:\n- Expected revenue: $142,500\n- Range: $128,000 - $157,000\n- Key driver: Seasonal uptick",
        "data": {"forecast": 142500, "lower": 128000, "upper": 157000}
    }
}

# Initialize response state
if "last_response" not in st.session_state:
    st.session_state.last_response = None

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Analyze Trends", use_container_width=True):
        st.session_state.last_response = MOCK_RESPONSES["analyze_trends"]
with col2:
    if st.button("📥 Export Data", use_container_width=True):
        st.session_state.last_response = MOCK_RESPONSES["export_data"]
with col3:
    if st.button("🔮 Generate Forecast", use_container_width=True):
        st.session_state.last_response = MOCK_RESPONSES["generate_forecast"]

# Display response
if st.session_state.last_response:
    st.markdown("---")
    st.markdown(st.session_state.last_response["message"])
```

---

## Prompt Input with Callbacks

Handle text input with simulated AI responses.

```python
# Mock AI responses based on keywords
def get_mock_ai_response(prompt: str) -> str:
    prompt_lower = prompt.lower()
    
    if "revenue" in prompt_lower or "sales" in prompt_lower:
        return """📈 **Revenue Analysis**

Based on the current data:
- Total revenue YTD: $4.2M
- Growth rate: 18% YoY
- Top performing segment: Enterprise (45% of revenue)
- Recommendation: Focus on mid-market expansion"""
    
    elif "forecast" in prompt_lower or "predict" in prompt_lower:
        return """🔮 **Forecast Summary**

30-day projection:
- Expected: $385,000
- Best case: $420,000
- Conservative: $350,000

Key factors: Seasonal trends, pipeline conversion rates"""
    
    else:
        return f"""💡 **Analysis Result**

I analyzed your request: "{prompt}"

Here are the key insights:
- Data quality: 94% complete
- Anomalies detected: 3
- Suggested actions: Review outliers in Q3 data"""

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input area
st.markdown("### 🤖 AI Assistant")
prompt = st.text_input(
    "Ask a question about your data",
    placeholder="e.g., What's the revenue trend?",
    key="ai_prompt"
)

if st.button("Send", type="primary") and prompt:
    response = get_mock_ai_response(prompt)
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": response
    })
    st.rerun()

# Display chat history
for msg in st.session_state.chat_history[-6:]:  # Last 3 exchanges
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(msg["content"])
    st.markdown("---")
```

---

## Chart Interactivity

Add interactive features to Altair charts.

### Basic Interactivity

```python
import altair as alt

# Enable tooltips and zoom/pan
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("category:N", title="Category"),
    y=alt.Y("value:Q", title="Value"),
    tooltip=[
        alt.Tooltip("category:N", title="Category"),
        alt.Tooltip("value:Q", title="Value", format="$,.0f")
    ]
).interactive()  # Enables zoom/pan

st.altair_chart(chart, use_container_width=True)
```

### Selection-Based Highlighting

```python
# Create selection
selection = alt.selection_point(fields=["category"])

# Apply selection to chart
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("category:N", title="Category"),
    y=alt.Y("value:Q", title="Value"),
    color=alt.condition(
        selection,
        alt.value("#4A90D9"),  # Selected color
        alt.value("#cccccc")   # Unselected color
    ),
    tooltip=["category", "value"]
).add_params(selection)

st.altair_chart(chart, use_container_width=True)
```

### Linked Charts

```python
# Shared selection across charts
brush = alt.selection_interval()

# First chart (selector)
chart1 = alt.Chart(df).mark_point().encode(
    x="date:T",
    y="value:Q",
    color=alt.condition(brush, "category:N", alt.value("lightgray"))
).add_params(brush).properties(height=200)

# Second chart (filtered by selection)
chart2 = alt.Chart(df).mark_bar().encode(
    x="category:N",
    y="sum(value):Q"
).transform_filter(brush).properties(height=200)

# Display stacked
st.altair_chart(chart1 & chart2, use_container_width=True)
```

---

## Navigation State

Track active page/section in multi-page layouts.

```python
# Initialize navigation state
if "active_page" not in st.session_state:
    st.session_state.active_page = "overview"

# Navigation items
NAV_ITEMS = [
    {"id": "overview", "icon": "📊", "label": "Overview"},
    {"id": "analytics", "icon": "📈", "label": "Analytics"},
    {"id": "reports", "icon": "📋", "label": "Reports"},
    {"id": "settings", "icon": "⚙️", "label": "Settings"},
]

# Render navigation in sidebar
with st.sidebar:
    st.markdown("### Navigation")
    for item in NAV_ITEMS:
        is_active = st.session_state.active_page == item["id"]
        btn_type = "primary" if is_active else "secondary"
        if st.button(
            f"{item['icon']} {item['label']}",
            key=f"nav_{item['id']}",
            type=btn_type,
            use_container_width=True
        ):
            st.session_state.active_page = item["id"]
            st.rerun()

# Render page content
page = st.session_state.active_page

if page == "overview":
    st.header("📊 Overview")
    # ... overview content
elif page == "analytics":
    st.header("📈 Analytics")
    # ... analytics content
elif page == "reports":
    st.header("📋 Reports")
    # ... reports content
elif page == "settings":
    st.header("⚙️ Settings")
    # ... settings content
```

---

## Filter Controls

Interactive data filtering with state persistence.

```python
# Initialize filter state
if "filters" not in st.session_state:
    st.session_state.filters = {
        "date_range": "Last 30 days",
        "category": "All",
        "min_value": 0
    }

# Filter controls
with st.expander("🔍 Filters", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.selectbox(
            "Date Range",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            index=["Last 7 days", "Last 30 days", "Last 90 days", "All time"].index(
                st.session_state.filters["date_range"]
            )
        )
        st.session_state.filters["date_range"] = date_range
    
    with col2:
        categories = ["All", "Category A", "Category B", "Category C"]
        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(st.session_state.filters["category"])
        )
        st.session_state.filters["category"] = category
    
    with col3:
        min_value = st.slider(
            "Minimum Value",
            0, 1000,
            st.session_state.filters["min_value"]
        )
        st.session_state.filters["min_value"] = min_value

# Apply filters to data
def apply_filters(df, filters):
    filtered = df.copy()
    
    # Date filter
    if filters["date_range"] != "All time":
        days = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days[filters["date_range"]])
        filtered = filtered[filtered["date"] >= cutoff]
    
    # Category filter
    if filters["category"] != "All":
        filtered = filtered[filtered["category"] == filters["category"]]
    
    # Value filter
    filtered = filtered[filtered["value"] >= filters["min_value"]]
    
    return filtered

# Display filtered data
filtered_df = apply_filters(df, st.session_state.filters)
st.dataframe(filtered_df)
```

---

## Reset State Pattern

Provide a way to reset all session state.

```python
def reset_all_state():
    """Clear all session state and trigger rerun."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Reset button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🔄 Reset All", use_container_width=True):
        reset_all_state()
```
