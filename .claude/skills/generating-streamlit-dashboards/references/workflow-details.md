# Detailed Workflow Guide

Complete step-by-step procedures for generating Streamlit dashboards from wireframes.

## Contents

- [Execution Flow Overview](#execution-flow-overview)
- [Phase 1: Localhost Generation](#phase-1-localhost-generation)
- [Phase 2: Visual Validation (Optional)](#phase-2-visual-validation-optional)
- [Phase 3: Snowflake Deployment (Only on Request)](#phase-3-snowflake-deployment-only-on-request)
- [TODO List Rules](#todo-list-rules)

---

## Execution Flow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1: LOCALHOST (Default, ~2 minutes)                          │
├─────────────────────────────────────────────────────────────────────┤
│  1. git init + .gitignore (credentials protection)                 │
│  2. Analyze wireframe thoroughly                                    │
│  3. Generate streamlit_app.py + pyproject.toml ONLY                │
│  4. Lint: ruff check --fix && ruff format                          │
│  5. Validate spacing/alignment (code review)                        │
│  6. Start: uv sync && uv run streamlit run streamlit_app.py &      │
│  7. Health check: curl -sf localhost:8501/_stcore/health           │
│  8. git commit -m "Initial localhost Streamlit dashboard"          │
│  9. ✅ OUTPUT: "App running at http://localhost:8501"              │
│  10. 🛑 STOP - Wait for user                                       │
└─────────────────────────────────────────────────────────────────────┘

── user says "validate visually" ──

┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 2: VISUAL VALIDATION (Optional, ~2-3 minutes)               │
├─────────────────────────────────────────────────────────────────────┤
│  Prerequisites:                                                     │
│    uv pip install playwright && uv run playwright install chromium  │
│                                                                     │
│  FOR iteration = 1, 2, 3:                                          │
│    1. python scripts/visual-validate.py . $iteration --auto        │
│    2. Implement improvements from JSON output                       │
│    3. ruff check --fix && ruff format                              │
│    4. App auto-reloads on save                                      │
│    5. If score >= 90% after iter 2, early exit allowed             │
│                                                                     │
│  ✅ OUTPUT: "Validation complete, score: XX/100"                   │
│  🛑 STOP - Wait for user                                           │
└─────────────────────────────────────────────────────────────────────┘

── user says "deploy to snowflake" ──

┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 3: SNOWFLAKE DEPLOYMENT (Only on explicit request)          │
├─────────────────────────────────────────────────────────────────────┤
│  1. Validate localhost works first                                  │
│  2. 🔐 Search for PAT token (NOW, not earlier!)                    │
│  3. Configure snow CLI connection                                   │
│  4. Test: snow connection test -c <conn>                           │
│  5. Generate deployment files:                                      │
│     - environment.yml (SiS Warehouse)                               │
│     - requirements.txt (SiS Container)                              │
│     - snowflake.yml                                                 │
│     - spcs/ folder                                                  │
│  6. Deploy to requested environments                                │
│  7. git commit -m "Add Snowflake deployment files"                 │
│  ✅ OUTPUT: URLs for all deployed environments                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Localhost Generation

### Step 1: Initialize Project

```bash
# Initialize git (if not already a repo)
git init

# 🔐 CRITICAL: Create .gitignore first
# Use assets/templates/gitignore.template as base
# See references/security-rules.md for required patterns
```

### Step 2: Analyze Wireframe

**Edge Scan Protocol (Often Missed!):**

1. **Left edge:** Circles/icons? → Icon navigation (use `assets/templates/html/icon-nav.html`)
2. **Right edge:** "Tiles" or vertical bar? → Tiles panel (use `assets/templates/html/tiles-panel.html`)
3. **Top edge:** Logo/search/profile? → Navbar (use `assets/templates/html/top-navbar.html`)
4. **Bottom edge:** Footer? → Footer section

**Element Inventory:**
- Count sidebar cards → Generate THAT many unique cards
- Count charts → Generate THAT many with titles
- Count metrics → Generate THAT many with values

### Step 3: Generate Files

**Create ONLY:**
- `streamlit_app.py` - Main application
- `pyproject.toml` - uv dependencies (use `assets/templates/pyproject.toml.template`)

**DO NOT create:**
- environment.yml
- requirements.txt
- snowflake.yml
- spcs/ folder

### Step 4: Lint & Format

```bash
# Target only generated files - NEVER run on entire directory!
ruff check streamlit_app.py --fix
ruff format streamlit_app.py

# Optional type checking
ty check streamlit_app.py
```

### Step 5: Spacing/Alignment Validation

Before starting the app, review code for common issues:

| Issue | Fix |
|-------|-----|
| Sidebar text truncation | Use shorter text or CSS word-wrap |
| Column width imbalance | Use weighted columns: `st.columns([1.2, 1, 1, 1.2])` |
| Metric cards overflow | Use abbreviated formats: "$1.24M" |
| Charts without container width | Add `use_container_width=True` |
| Buttons in sidebar | Add `use_container_width=True` |

### Step 6: Start App

```bash
# Install dependencies
uv sync

# Start in background
uv run streamlit run streamlit_app.py --server.port 8501 &

# Health check loop
for i in {1..30}; do
    curl -sf http://localhost:8501/_stcore/health && break
    sleep 0.3
done
```

### Step 7: Initial Commit

```bash
git add -A
git commit -m "Initial localhost Streamlit dashboard"
```

### Step 8: Output Message

```
✅ STREAMLIT APP IS RUNNING!

🌐 http://localhost:8501

Options:
  • "validate visually" - run visual validation loop
  • "deploy to snowflake" - generate deployment files
```

**STOP and wait for user.**

---

## Phase 2: Visual Validation (Optional)

**Trigger:** User says "validate visually" or "use visual validation"

### Prerequisites

```bash
# Install Playwright (one-time)
uv pip install playwright
uv run playwright install chromium
```

### Validation Loop

Run up to 3 iterations with early exit at 90%:

```bash
# Iteration 1
python scripts/visual-validate.py . 1 --auto

# Iteration 2 (with early exit check)
python scripts/visual-validate.py . 2 --auto --early-exit 90

# Iteration 3 (if needed)
python scripts/visual-validate.py . 3 --auto
```

### After Each Iteration

1. Parse JSON output for improvements
2. Implement fixes in `streamlit_app.py`
3. Run: `ruff check streamlit_app.py --fix && ruff format streamlit_app.py`
4. App auto-reloads on save

### Scoring Criteria

| Category | Points | Checks |
|----------|--------|--------|
| Layout Elements | 40 | Icon nav, tiles panel, navbar, sidebar cards |
| Charts & Content | 30 | Titles, tooltips, metrics |
| Alignment | 20 | Column widths, spacing |
| Polish | 10 | Dark mode, chart variety |

**Score Interpretation:**
- 90-100: Excellent - Ready for deployment
- 70-89: Good - Minor polish needed
- 50-69: Fair - Several issues
- <50: Poor - Major rework needed

---

## Phase 3: Snowflake Deployment (Only on Request)

**Trigger:** User explicitly says "deploy to snowflake/sis/spcs"

**NOT a trigger:** "can be deployed to X, Y, Z" (describes CAPABILITY)

### Pre-Conditions

Before ANY deployment:
- ✅ `streamlit_app.py` exists and works
- ✅ App is running at http://localhost:8501
- ✅ User has reviewed the local app
- ✅ User EXPLICITLY said "deploy to snowflake/sis/spcs"

### Step 1: Validate PAT Token

```bash
# Search common locations (ONLY run when deployment requested!)
for path in ".env" "../.env" "../../.env" "$HOME/.env"; do
    if [ -f "$path" ] && grep -qE "^SNOWFLAKE_PAT=" "$path" 2>/dev/null; then
        echo "✅ Found PAT at: $path"
        ENV_PATH="$path"
        break
    fi
done

# If not found, ask user
if [ -z "$ENV_PATH" ]; then
    echo "❌ No .env with SNOWFLAKE_PAT found. Please create one."
fi
```

### Step 2: Extract Token

```bash
# SAFE - Extract without displaying content
grep -E "^SNOWFLAKE_PAT=" "${ENV_PATH:-.env}" \
    | head -1 | cut -d'=' -f2- > .snowflake-token
chmod 600 .snowflake-token
```

### Step 3: Configure Connection

**Option 1: Reuse existing**
```bash
snow connection list
snow streamlit deploy --connection EXISTING_CONN
```

**Option 2: Create new via config.toml**
```bash
cat >> ~/.snowflake/config.toml << EOF

[connections.myconn]
account = "xxx-yyy"
user = "myuser"
authenticator = "PROGRAMMATIC_ACCESS_TOKEN"
token_file_path = "$(pwd)/.snowflake-token"
EOF
```

### Step 4: Test Connection

```bash
snow connection test -c <connection_name>
# If fails → Ask user for help
```

### Step 5: Generate Deployment Files

Use templates from `assets/templates/`:
- `environment.yml` (SiS Warehouse)
- `requirements.txt` (SiS Container)
- `snowflake.yml`
- `spcs/Dockerfile`
- `spcs/spec.yaml`
- `spcs/requirements-spcs.txt`

**Naming Convention (use underscores, not hyphens!):**
```bash
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)
APP_NAME="MY_DASHBOARD_${TIMESTAMP}"
```

### Step 6: Deploy

**SiS Warehouse:**
```bash
snow streamlit deploy app_warehouse --connection <conn> --replace
```

**SiS Container (must use SQL):**
```bash
snow stage copy streamlit_app.py @STAGE/app/ -c <conn> --overwrite
snow stage copy requirements.txt @STAGE/app/ -c <conn> --overwrite
snow sql -c <conn> -q "
    CREATE OR REPLACE STREAMLIT DB.SCHEMA.${APP_NAME}
        FROM '@STAGE/app/'
        MAIN_FILE = 'streamlit_app.py'
        TITLE = '${TIMESTAMP} My Dashboard (Container)'
        QUERY_WAREHOUSE = SYSTEM\$STREAMLIT_NOTEBOOK_WH
        COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU;
"
```

**SPCS:**
```bash
cd spcs && cp ../streamlit_app.py .
docker build --platform linux/amd64 -t app:latest .
snow spcs image-registry login --connection <conn>
docker push <registry>/app:latest
snow sql -c <conn> -q "CREATE SERVICE..."
```

### Step 7: Commit Deployment Files

```bash
git add -A
git commit -m "Add Snowflake deployment files (Warehouse, Container, SPCS)"
```

---

## Workflow Checklists

Copy these checklists and track progress in your response.

### Phase 1: Localhost (Default)

```
Localhost Progress:
- [ ] Initialize git repo with .gitignore
- [ ] Analyze wireframe thoroughly
- [ ] Generate streamlit_app.py
- [ ] Generate pyproject.toml
- [ ] Lint: ruff check --fix && ruff format
- [ ] Validate spacing/alignment
- [ ] Start localhost and verify health
- [ ] Initial git commit
- [ ] STOP - Output localhost URL and wait
```

### Phase 2: Visual Validation (On Request)

```
Validation Progress:
- [ ] Install playwright if needed
- [ ] Run iteration 1: visual-validate.py . 1 --auto
- [ ] Implement improvements from JSON output
- [ ] Lint and format changes
- [ ] Run iteration 2 (early exit if score >= 90%)
- [ ] Run iteration 3 if needed
- [ ] Output final score and STOP
```

### Phase 3: Snowflake Deployment (On Request)

```
Deployment Progress:
- [ ] Verify localhost works first
- [ ] Search for PAT token (NOW, not earlier)
- [ ] Configure snow CLI connection
- [ ] Test connection: snow connection test
- [ ] Generate deployment files (environment.yml, requirements.txt, etc.)
- [ ] Deploy to requested environments
- [ ] Git commit deployment files
- [ ] Output URLs for all deployed environments
```

**NEVER add deployment tasks automatically.** Only add when user explicitly says:
- "deploy to snowflake" → All environments
- "deploy to warehouse" → SiS Warehouse only
- "deploy to container" → SiS Container only
- "deploy to spcs" → SPCS only

---

## Modular Project Structure (for Complex Dashboards)

For dashboards exceeding ~300 lines, use a modular structure for maintainability and testability.

### When to Use Modular Structure

| Criteria | Single File | Modular Structure |
|----------|-------------|-------------------|
| Lines of code | <300 | >300 |
| Number of charts | 1-3 | 4+ |
| Team size | Solo | Multiple developers |
| Need unit tests | No | Yes |
| Reusable components | No | Yes |

### Recommended Structure

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

### Key Principles

1. **Data/chart functions are pure (no Streamlit imports)** — Testable with pytest
2. **Components contain Streamlit rendering logic** — Isolated side effects
3. **Config centralizes constants** — Easy modification of colors, labels, mock data
4. **Main file only orchestrates** — Imports and layout, minimal logic

### Example: Pure Chart Function (Testable)

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

### Example: Component with Streamlit (Rendering)

```python
# src/components/kpi_cards.py
import streamlit as st
from src.config import COLORS

def render_kpi_row(metrics: list[dict]):
    """Render a row of KPI cards. Contains Streamlit logic."""
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {COLORS['primary']}">
                <div class="kpi-label">{metric['label']}</div>
                <div class="kpi-value">{metric['value']}</div>
                <div class="kpi-delta {'positive' if metric['delta'] > 0 else 'negative'}">
                    {'+' if metric['delta'] > 0 else ''}{metric['delta']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
```

### Example: Main Orchestration File

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

### Testing Pure Functions

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

def test_create_revenue_chart_has_correct_mark(sample_revenue_data):
    result = create_revenue_chart(sample_revenue_data)
    assert result.mark == "bar" or hasattr(result.mark, "type")
```

### pyproject.toml for Modular Projects

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
