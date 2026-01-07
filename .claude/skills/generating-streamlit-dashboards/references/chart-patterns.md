# Altair Chart Patterns

Explicit, SiS-compatible chart patterns for Streamlit dashboards.

## Contents

- [Color Palette](#color-palette)
- [Basic Bar Chart](#basic-bar-chart)
- [Stacked Bar Chart](#stacked-bar-chart)
- [Grouped Bar Chart (Altair 4.x Compatible)](#grouped-bar-chart-altair-4x-compatible)
- [Line Chart](#line-chart)
- [Multi-Line Chart](#multi-line-chart)
- [Area Chart](#area-chart)
- [Stacked Area Chart](#stacked-area-chart)
- [Pie/Donut Chart](#piedonut-chart)
- [Scatter Plot](#scatter-plot)
- [Dark Mode Altair Theme](#dark-mode-altair-theme)
- [Chart Requirements Checklist](#chart-requirements-checklist)

---

## Color Palette

Define at top of `streamlit_app.py`:

```python
CHART_COLORS = {
    "primary": "#4A90D9",    # Main brand blue
    "secondary": "#E57373",  # Accent red
    "success": "#81C784",    # Green
    "warning": "#FFB74D",    # Orange
    "accent": "#9575CD",     # Purple
    "teal": "#26A69A",       # Teal
}
```

---

## Basic Bar Chart

```python
st.markdown("**Monthly Revenue**")  # TITLE REQUIRED

data = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [42000, 48000, 51000, 47000, 55000, 62000]
})

chart = alt.Chart(data).mark_bar(
    color=CHART_COLORS["primary"],  # EXPLICIT COLOR
    cornerRadiusTopLeft=4,
    cornerRadiusTopRight=4
).encode(
    x=alt.X("month:N", title="Month", sort=None),      # AXIS LABEL
    y=alt.Y("revenue:Q", title="Revenue ($)"),         # AXIS LABEL
    tooltip=[
        alt.Tooltip("month:N", title="Month"),
        alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f")  # TOOLTIP
    ]
).properties(height=250)

st.altair_chart(chart, use_container_width=True)
```

---

## Stacked Bar Chart

**⚠️ CRITICAL: Data MUST be in long format (one row per category+group).**

```python
st.markdown("**Quarterly by Department**")

# ✅ CORRECT: Long format data
stacked_data = pd.DataFrame({
    "Quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4"],
    "Department": ["Sales", "Marketing", "Operations"] * 4,
    "Amount": [120, 80, 60, 150, 90, 70, 180, 100, 85, 200, 110, 95]
})

stacked_bar = alt.Chart(stacked_data).mark_bar().encode(
    x=alt.X("Quarter:N", title="Quarter", sort=["Q1", "Q2", "Q3", "Q4"]),
    y=alt.Y("Amount:Q", title="Amount ($K)", stack="zero"),  # stack="zero" for stacking!
    color=alt.Color(
        "Department:N",
        scale=alt.Scale(
            domain=["Sales", "Marketing", "Operations"],
            range=["#4A90D9", "#E57373", "#81C784"]
        ),
        legend=alt.Legend(title="Department", orient="bottom")
    ),
    tooltip=[
        alt.Tooltip("Quarter:N"),
        alt.Tooltip("Department:N"),
        alt.Tooltip("Amount:Q", title="Amount", format="$,.0f")
    ]
).properties(height=300)

st.altair_chart(stacked_bar, use_container_width=True)
```

**❌ WRONG: Wide format causes empty chart:**
```python
# This won't stack!
wrong_data = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Sales": [120, 150, 180, 200],
    "Marketing": [80, 90, 100, 110],
})
```

---

## Grouped Bar Chart (Altair 4.x Compatible)

**⚠️ Don't use `xOffset` - not available in SiS Container (Altair 4.x).**

```python
st.markdown("**Revenue by Region and Product**")

grouped_data = pd.DataFrame({
    "Region": ["North", "North", "South", "South", "East", "East", "West", "West"],
    "Product": ["A", "B"] * 4,
    "Revenue": [120, 90, 150, 110, 80, 140, 100, 130]
})

# ✅ Use column faceting instead of xOffset
grouped_bar = alt.Chart(grouped_data).mark_bar().encode(
    x=alt.X("Product:N", title="", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Revenue:Q", title="Revenue ($K)"),
    color=alt.Color(
        "Product:N",
        scale=alt.Scale(domain=["A", "B"], range=["#4A90D9", "#E57373"]),
        legend=None  # Hide legend, labels on x-axis
    ),
    column=alt.Column(
        "Region:N",
        title="",
        header=alt.Header(labelOrient="bottom")
    ),
    tooltip=["Region", "Product", "Revenue"]
).properties(height=280, width=100)  # Set width per facet

st.altair_chart(grouped_bar, use_container_width=True)
```

---

## Line Chart

```python
st.markdown("**Monthly Trend**")

trend_data = pd.DataFrame({
    "month": pd.date_range("2024-01", periods=12, freq="ME"),
    "value": [45, 52, 48, 61, 55, 67, 72, 68, 75, 82, 78, 91]
})

line_chart = alt.Chart(trend_data).mark_line(
    point=True,
    color=CHART_COLORS["primary"]
).encode(
    x=alt.X("month:T", title="Month"),
    y=alt.Y("value:Q", title="Value"),
    tooltip=[
        alt.Tooltip("month:T", title="Month", format="%b %Y"),
        alt.Tooltip("value:Q", title="Value", format=",")
    ]
).properties(height=250).interactive()  # Enable zoom/pan

st.altair_chart(line_chart, use_container_width=True)
```

---

## Multi-Line Chart

```python
st.markdown("**Revenue by Channel**")

multi_data = pd.DataFrame({
    "month": list(pd.date_range("2024-01", periods=6, freq="ME")) * 3,
    "channel": ["Direct"] * 6 + ["Organic"] * 6 + ["Paid"] * 6,
    "revenue": [45, 52, 48, 61, 55, 67, 30, 35, 42, 38, 45, 52, 20, 25, 30, 28, 35, 40]
})

multi_line = alt.Chart(multi_data).mark_line(point=True).encode(
    x=alt.X("month:T", title="Month"),
    y=alt.Y("revenue:Q", title="Revenue ($K)"),
    color=alt.Color(
        "channel:N",
        scale=alt.Scale(
            domain=["Direct", "Organic", "Paid"],
            range=["#4A90D9", "#81C784", "#FFB74D"]
        ),
        legend=alt.Legend(title="Channel", orient="bottom")
    ),
    tooltip=["month:T", "channel:N", "revenue:Q"]
).properties(height=300).interactive()

st.altair_chart(multi_line, use_container_width=True)
```

---

## Area Chart

```python
st.markdown("**Cumulative Growth**")

area_data = pd.DataFrame({
    "month": pd.date_range("2024-01", periods=12, freq="ME"),
    "users": [1000, 1200, 1500, 1800, 2200, 2800, 3500, 4200, 5000, 5800, 6700, 7800]
})

area_chart = alt.Chart(area_data).mark_area(
    color=CHART_COLORS["primary"],
    opacity=0.7,
    line=True
).encode(
    x=alt.X("month:T", title="Month"),
    y=alt.Y("users:Q", title="Total Users"),
    tooltip=[
        alt.Tooltip("month:T", format="%b %Y"),
        alt.Tooltip("users:Q", title="Users", format=",")
    ]
).properties(height=250)

st.altair_chart(area_chart, use_container_width=True)
```

---

## Stacked Area Chart

```python
st.markdown("**Traffic Sources**")

stacked_area_data = pd.DataFrame({
    "month": list(pd.date_range("2024-01", periods=6, freq="ME")) * 3,
    "source": ["Organic"] * 6 + ["Paid"] * 6 + ["Referral"] * 6,
    "visits": [5000, 5500, 6000, 5800, 6200, 7000,
               3000, 3500, 4000, 4200, 4500, 5000,
               2000, 2200, 2500, 2400, 2800, 3000]
})

stacked_area = alt.Chart(stacked_area_data).mark_area(opacity=0.7).encode(
    x=alt.X("month:T", title="Month"),
    y=alt.Y("visits:Q", title="Visits", stack="zero"),
    color=alt.Color(
        "source:N",
        scale=alt.Scale(
            domain=["Organic", "Paid", "Referral"],
            range=["#81C784", "#FFB74D", "#9575CD"]
        )
    ),
    tooltip=["month:T", "source:N", "visits:Q"]
).properties(height=300)

st.altair_chart(stacked_area, use_container_width=True)
```

---

## Pie/Donut Chart

```python
st.markdown("**Revenue Distribution**")

pie_data = pd.DataFrame({
    "category": ["Product A", "Product B", "Product C", "Services"],
    "value": [35, 28, 22, 15]
})

pie_chart = alt.Chart(pie_data).mark_arc(
    innerRadius=50  # Set > 0 for donut
).encode(
    theta=alt.Theta("value:Q"),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(
            domain=["Product A", "Product B", "Product C", "Services"],
            range=["#4A90D9", "#E57373", "#81C784", "#FFB74D"]
        ),
        legend=alt.Legend(orient="right")
    ),
    tooltip=["category:N", alt.Tooltip("value:Q", format=".1f")]
).properties(height=300)

st.altair_chart(pie_chart, use_container_width=True)
```

---

## Scatter Plot

```python
st.markdown("**Price vs Volume**")

scatter_data = pd.DataFrame({
    "price": np.random.uniform(10, 100, 50),
    "volume": np.random.uniform(100, 1000, 50),
    "category": np.random.choice(["A", "B", "C"], 50)
})

scatter = alt.Chart(scatter_data).mark_circle(size=60).encode(
    x=alt.X("price:Q", title="Price ($)"),
    y=alt.Y("volume:Q", title="Volume"),
    color=alt.Color("category:N"),
    tooltip=["price:Q", "volume:Q", "category:N"]
).properties(height=300).interactive()

st.altair_chart(scatter, use_container_width=True)
```

---

## Dark Mode Altair Theme

Register a custom theme for true dark mode charts:

```python
def custom_dark_theme():
    """Custom Altair theme for true dark mode."""
    return {
        "config": {
            "background": "#1a1a2e",
            "view": {"fill": "#1a1a2e", "stroke": "transparent"},
            "title": {"color": "#ffffff", "fontSize": 14, "fontWeight": 600},
            "axis": {
                "domainColor": "#3a3a5a",
                "gridColor": "#2a2a4a",
                "tickColor": "#3a3a5a",
                "labelColor": "#a0a0a0",
                "titleColor": "#ffffff",
            },
            "legend": {
                "labelColor": "#a0a0a0",
                "titleColor": "#ffffff",
            },
            "text": {"color": "#ffffff"},
        }
    }

# Register and enable
alt.themes.register("custom_dark", custom_dark_theme)

if st.session_state.get("dark_mode"):
    alt.themes.enable("custom_dark")
else:
    alt.themes.enable("default")
```

---

## Chart Requirements Checklist

Every chart MUST have:

- [ ] **Title** - `st.markdown("**Chart Title**")` before chart
- [ ] **Explicit colors** - Never rely on defaults
- [ ] **Axis labels** - `title=` in `alt.X()` and `alt.Y()`
- [ ] **Tooltips** - `tooltip=[...]` in encode
- [ ] **Container width** - `use_container_width=True`
- [ ] **Legend** (for multi-series) - `legend=alt.Legend(...)`
