# Visual Element to Streamlit Component Mapping

Quick reference for mapping wireframe elements to Streamlit components.

**For detailed patterns, see:**
- Layout patterns (navigation, panels, cards): `layout-patterns.md`
- CSS patterns (styling, themes): `css-patterns.md`
- Chart patterns (Altair examples): `chart-patterns.md`

## Contents

- [Critical Rule: Never Generate Placeholders](#-critical-rule-never-generate-placeholders)
- [Layout Elements Quick Reference](#layout-elements)
- [Charts and Visualizations Quick Reference](#charts-and-visualizations)
- [Data Display](#data-display)
- [Input Widgets](#input-widgets)
- [Interactive Elements](#interactive-elements)
- [Chart with Title Pattern](#chart-with-title-pattern-mandatory)

---

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

## Edge Navigation (See `layout-patterns.md` for full code)

| Edge | Element | Pattern |
|------|---------|---------|
| Left circles | Icon navigation | See `layout-patterns.md#left-icon-navigation` |
| Right "Tiles" | Tiles panel | See `layout-patterns.md#right-tiles-panel` |
| Top bar | Navbar | See `layout-patterns.md#dashboard-header` |

**CSS for navigation:** See `css-patterns.md`

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

**Key chart rules:** Always use explicit colors (`color="#4A90D9"`), axis labels (`title=`), and tooltips (`tooltip=[...]`).

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

## Sidebar & Panel Patterns

For full patterns with CSS, see `layout-patterns.md`:
- Sidebar insight cards: `layout-patterns.md#sidebar-insight-cards`
- Right panel: `layout-patterns.md#right-panel-pattern`
- KPI row: `layout-patterns.md#kpi-row`

## Chart with Title Pattern (MANDATORY)

Every chart MUST have: title, explicit colors, axis labels, tooltips, container width.

```python
st.markdown("**Monthly Revenue**")  # Title BEFORE chart
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:N", title="Month"),
    y=alt.Y("value:Q", title="Revenue ($)"),
    tooltip=["month", alt.Tooltip("value:Q", format="$,.0f")]
)
st.altair_chart(chart, use_container_width=True)
```

## Layout Examples

See `layout-patterns.md` for complete patterns:
- Dashboard header
- KPI row
- Sidebar with filters
- Tabbed content

## CSS Styling

See `css-patterns.md` for complete styling:
- Custom theme variables
- Dark mode CSS
- Hide Streamlit branding
