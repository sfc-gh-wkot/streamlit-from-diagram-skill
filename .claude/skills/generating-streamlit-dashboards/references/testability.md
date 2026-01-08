# Testability Guidelines

Patterns for writing testable Streamlit dashboard code by separating pure functions from rendering logic.

## Contents

- [When to Use Modular Structure](#when-to-use-modular-structure)
- [Key Principles](#key-principles)
- [Pure Function Patterns](#pure-function-patterns)
- [Component Patterns](#component-patterns)
- [Test File Templates](#test-file-templates)
- [Project Structure](#project-structure)

---

## When to Use Modular Structure

| Criteria | Single File | Modular Structure |
|----------|-------------|-------------------|
| Lines of code | <300 | >300 |
| Number of charts | 1-3 | 4+ |
| Team size | Solo | Multiple developers |
| Need unit tests | No | Yes |
| Reusable components | No | Yes |

For simple dashboards (<300 lines), a single `streamlit_app.py` file is appropriate. For complex dashboards, use the modular structure below.

---

## Key Principles

1. **Data/chart functions are pure (no Streamlit imports)** — Testable with pytest
2. **Components contain Streamlit rendering logic** — Isolated side effects
3. **Config centralizes constants** — Easy modification of colors, labels, mock data
4. **Main file only orchestrates** — Imports and layout, minimal logic

---

## Pure Function Patterns

### Testable Chart Function

```python
# src/charts/analytics.py
import altair as alt
import pandas as pd

CHART_COLORS = {"primary": "#4A90D9", "secondary": "#50C878"}

def create_revenue_chart(df: pd.DataFrame) -> alt.Chart:
    """Create revenue bar chart. Pure function, no Streamlit imports."""
    return alt.Chart(df).mark_bar(color=CHART_COLORS["primary"]).encode(
        x=alt.X("month:N", title="Month"),
        y=alt.Y("revenue:Q", title="Revenue ($)", axis=alt.Axis(format="$,.0f")),
        tooltip=[
            alt.Tooltip("month:N", title="Month"),
            alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f")
        ]
    ).properties(height=300)
```

### Testable Data Generator

```python
# src/data/generators.py
import pandas as pd
import numpy as np

def generate_revenue_data(seed: int = 42, months: int = 12) -> pd.DataFrame:
    """Generate sample revenue data. Pure function, no Streamlit imports."""
    np.random.seed(seed)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][:months]
    return pd.DataFrame({
        "month": month_names,
        "revenue": np.random.randint(40000, 100000, months)
    })

def generate_kpi_metrics(seed: int = 42) -> list[dict]:
    """Generate KPI metrics. Pure function."""
    np.random.seed(seed)
    return [
        {"label": "Total Revenue", "value": f"${np.random.randint(40, 60):,}K", "delta": 12.5},
        {"label": "Active Users", "value": f"{np.random.randint(2000, 3000):,}", "delta": 8.2},
        {"label": "Conversion", "value": f"{np.random.uniform(2, 5):.2f}%", "delta": -0.4},
        {"label": "Avg. Session", "value": f"{np.random.randint(3, 6)}m {np.random.randint(0, 59)}s", "delta": 1.2},
    ]
```

---

## Component Patterns

### Rendering Component (with Streamlit)

```python
# src/components/kpi_cards.py
import streamlit as st
from src.config import COLORS

def render_kpi_row(metrics: list[dict]):
    """Render a row of KPI cards. Contains Streamlit logic."""
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            delta_class = "positive" if metric["delta"] > 0 else "negative"
            delta_sign = "+" if metric["delta"] > 0 else ""
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {COLORS['primary']}">
                <div class="kpi-label">{metric['label']}</div>
                <div class="kpi-value">{metric['value']}</div>
                <div class="kpi-delta {delta_class}">
                    {delta_sign}{metric['delta']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
```

---

## Test File Templates

### Testing Pure Chart Functions

```python
# tests/test_charts.py
import pytest
import pandas as pd
import altair as alt
from src.charts.analytics import create_revenue_chart

@pytest.fixture
def sample_revenue_data():
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar"],
        "revenue": [100000, 120000, 115000]
    })

def test_create_revenue_chart_returns_chart(sample_revenue_data):
    result = create_revenue_chart(sample_revenue_data)
    assert isinstance(result, alt.Chart)

def test_create_revenue_chart_has_correct_encoding(sample_revenue_data):
    result = create_revenue_chart(sample_revenue_data)
    # Altair charts store encoding info in the spec
    spec = result.to_dict()
    assert "x" in spec["encoding"]
    assert "y" in spec["encoding"]
```

### Testing Data Generators

```python
# tests/test_data_generators.py
import pytest
import pandas as pd
from src.data.generators import generate_revenue_data, generate_kpi_metrics

def test_generate_revenue_data_returns_dataframe():
    result = generate_revenue_data()
    assert isinstance(result, pd.DataFrame)

def test_generate_revenue_data_has_correct_columns():
    result = generate_revenue_data()
    assert "month" in result.columns
    assert "revenue" in result.columns

def test_generate_revenue_data_deterministic():
    result1 = generate_revenue_data(seed=42)
    result2 = generate_revenue_data(seed=42)
    pd.testing.assert_frame_equal(result1, result2)

def test_generate_kpi_metrics_returns_list():
    result = generate_kpi_metrics()
    assert isinstance(result, list)
    assert len(result) == 4

def test_generate_kpi_metrics_has_required_keys():
    result = generate_kpi_metrics()
    for metric in result:
        assert "label" in metric
        assert "value" in metric
        assert "delta" in metric
```

---

## Project Structure

### Recommended Directory Layout

```
project/
├── streamlit_app.py      # Thin orchestration (~150 lines max)
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py         # Constants, mock data, colors
│   ├── styles.py         # CSS strings
│   ├── data/
│   │   ├── __init__.py
│   │   └── generators.py # Pure data generation (no st imports)
│   ├── charts/
│   │   ├── __init__.py
│   │   └── analytics.py  # Pure Altair chart functions
│   └── components/
│       ├── __init__.py
│       ├── navigation.py
│       ├── sidebar.py
│       ├── kpi_cards.py
│       └── ai_assistant.py
└── tests/
    ├── __init__.py
    ├── test_data_generators.py
    └── test_charts.py
```

### Main Orchestration File

```python
# streamlit_app.py
import streamlit as st
from src.config import APP_TITLE, MOCK_DATA
from src.styles import get_css
from src.data.generators import generate_dashboard_data
from src.charts.analytics import create_revenue_chart, create_trend_chart
from src.components.navigation import render_sidebar
from src.components.kpi_cards import render_kpi_row

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

# Load data (cached)
@st.cache_data
def load_data():
    return generate_dashboard_data(seed=42)

data = load_data()

# Layout
render_sidebar(data["navigation"])
render_kpi_row(data["metrics"])

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Monthly Revenue**")
    st.altair_chart(create_revenue_chart(data["revenue"]), use_container_width=True)
with col2:
    st.markdown("**Growth Trend**")
    st.altair_chart(create_trend_chart(data["trends"]), use_container_width=True)
```

### pyproject.toml for Testing

```toml
[project]
name = "my-dashboard"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.35",
    "pandas>=2.0",
    "altair>=5.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.4"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

---

## Running Tests

```bash
# Install dev dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_charts.py -v
```
