---
name: generating-streamlit-dashboards
description: |
  This skill should be used when the user asks to "create dashboard from wireframe", "convert this design to Streamlit", "build app from screenshot", "make this into a Streamlit app", or "turn this mockup into code". Transforms wireframes, screenshots, and UI designs into production-ready Streamlit dashboards with rich content, interactive charts, and professional styling.
  
  This skill should NOT be used when the user asks to "debug my Streamlit app", "how do I use st.columns", "modify the existing dashboard", "fix this Streamlit error", or "explain Streamlit". These requests require general Streamlit knowledge, not wireframe-to-code transformation.
---

# Streamlit Dashboard from Image

Transform wireframes and screenshots into production-ready Streamlit dashboards.

## Quick Reference

| Resource | Location |
|----------|----------|
| Workflow details | `references/workflow-details.md` |
| Chart patterns | `references/chart-patterns.md` |
| Component mapping | `references/component-mapping.md` |
| Layout patterns | `references/layout-patterns.md` |
| CSS patterns | `references/css-patterns.md` |
| Interactivity patterns | `references/interactivity-patterns.md` |
| Content requirements | `references/content-requirements.md` |
| Testability guidelines | `references/testability.md` |
| Version compatibility | `references/version-matrix.md` |
| Snowflake deployment | `references/snowflake-deployment.md` |
| Security rules | `references/security-rules.md` |
| Troubleshooting | `references/troubleshooting.md` |
| Model-specific guidance | `references/model-guidance.md` |
| CSS templates | `assets/templates/css/` |
| HTML templates | `assets/templates/html/` |
| Config templates | `assets/templates/` |
| Evaluations | `evaluations/` |

---

## Quick Start Example

**Input:** User provides `wireframe.png` showing:
- Left icon navigation (4 circles)
- Sidebar with 3 "Predictive Item" cards
- Main area with "Page Title", 2 charts (bar + line)
- Top navbar with "COMPANY | Property Name", Search, Profile
- Right panel with tiles, "Try This" buttons, "Enter Prompt" input

**Output:**

```
project/
├── .gitignore           ← Created FIRST (credential protection)
├── streamlit_app.py     ← Full implementation with rich content
└── pyproject.toml       ← uv dependencies
```

**Key Transformations:**

| Wireframe Element | Transformed Output |
|-------------------|-------------------|
| "Predictive Item" boxes | **Revenue Forecast** ($128K, +23%), **Churn Risk Alert** (47 users), **Growth Opportunity** (+18%) |
| Bar chart placeholder | **Monthly Revenue** — Altair bar chart with axis labels, tooltips |
| Line chart placeholder | **Daily Trend** — Altair line chart with `.interactive()` |
| "Try This" buttons | **AI SUGGESTIONS** — ✦ Optimize ad spend, ✦ Review churn users |
| "Enter Prompt" + Run | Text input + "▷ Run" button with mock response |

**Verification:** `curl -sf http://localhost:8501/_stcore/health` returns 200

**Result:** App running at http://localhost:8501, git committed, STOP and wait for user.

See `references/content-requirements.md` for detailed transformation tables and sample data guidelines.

---

## Security (MANDATORY)

⚠️ **NEVER** read, echo, or commit credentials (passwords, tokens, .env files)

⚠️ **ALWAYS** create `.gitignore` FIRST before any other file operations

⚠️ **DO NO HARM** to user databases — CREATE only, never DROP/DELETE/UPDATE

See `references/security-rules.md` for complete guidelines including safe token extraction.

---

## Execution Phases

This skill operates in three phases. See `references/workflow-details.md` for detailed procedures.

### Phase 1: Localhost (Default) [LOW FREEDOM]

**Trigger:** User provides wireframe/screenshot

**Duration:** ~2 minutes

**Output:** Running app at http://localhost:8501

Create files in EXACT order: `.gitignore` → `streamlit_app.py` → `pyproject.toml`

### Phase 2: Visual Validation (Optional) [MEDIUM FREEDOM]

**Trigger:** User says "validate visually"

**Duration:** ~2-3 minutes

**Output:** Score and improvements list

Runs up to 3 iterations with early exit at 90%. Implement improvements as needed.

### Phase 3: Snowflake Deployment (Optional) [LOW FREEDOM]

**Trigger:** User explicitly says "deploy to snowflake/sis/spcs"

**Duration:** ~5 minutes

**Output:** URLs for deployed environments

NOT triggered by: "can be deployed to X, Y, Z" (capability description)

---

## Tool Usage by Phase

| Phase | Primary Tools | Purpose |
|-------|---------------|---------|
| Localhost | Write, Bash | Generate files, run app |
| Validation | Read, Bash | Analyze code, run scripts |
| Deployment | Bash, Grep | Find tokens, deploy |

---

## Wireframe Analysis Protocol [HIGH FREEDOM]

**Edge Scan Protocol (Often Missed):**

1. **Left edge** — Circles/icons? → Icon navigation
2. **Right edge** — "Tiles" or vertical bar? → Tiles panel
3. **Top edge** — Logo/search/profile? → Navbar
4. **Bottom edge** — Footer? → Footer section

**Element Inventory:**
- Count sidebar cards → Generate THAT many unique cards
- Count charts → Generate THAT many with titles
- Count metrics → Generate THAT many with values

**CRITICAL:** Never use placeholder text. Every "Predictive Item" becomes "Revenue Forecast", every box with lines becomes a real card with metrics.

Select appropriate content based on wireframe context (finance → revenue/costs, analytics → traffic/conversions).

See `references/content-requirements.md` for complete transformation guidelines.

---

## Code Quality Standards (IMPORTANT)

Generated Streamlit code MUST be:

| Standard | Description |
|----------|-------------|
| **Modern Python** | Use Python 3.11+ features, type hints, f-strings, dataclasses where appropriate |
| **Modular** | Separate concerns: data generation, chart creation, rendering logic |
| **Testable** | Pure functions for data/charts (no `st.` imports), components for rendering |
| **Easy to Navigate** | Logical file structure, clear section comments, consistent naming |
| **Easy to Comprehend** | Descriptive variable names, docstrings on functions, no magic numbers |

For dashboards >300 lines, use modular project structure. See `references/testability.md` for patterns.

**Quick Example:**

```python
# ✅ Good: Modern, modular, testable
def create_revenue_chart(df: pd.DataFrame, color: str = "#4A90D9") -> alt.Chart:
    """Create revenue bar chart with tooltips."""
    return alt.Chart(df).mark_bar(color=color).encode(
        x=alt.X("month:N", title="Month"),
        y=alt.Y("revenue:Q", title="Revenue ($)", axis=alt.Axis(format="$,.0f")),
        tooltip=[alt.Tooltip("revenue:Q", format="$,.0f")]
    ).interactive()

# ❌ Bad: Monolithic, untestable, hard to follow
def render():
    st.markdown("**Revenue**")
    st.altair_chart(alt.Chart(pd.DataFrame({"m":["Jan"],"r":[100]})).mark_bar()...)
```

---

## Code Generation Rules

### Toolchain

| Tool | Purpose | Command |
|------|---------|---------|
| **uv** | Package management | `uv sync`, `uv run` |
| **ruff** | Lint + format | `ruff check --fix && ruff format` |

### Must Use

```python
# Cache data generation at app entry point
@st.cache_data
def load_data():
    return generate_all_data(seed=42)

data = load_data()

# Altair with explicit colors, titles, tooltips
alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:N", title="Month"),
    y=alt.Y("value:Q", title="Revenue ($)"),
    tooltip=["month", alt.Tooltip("value:Q", format="$,.0f")]
).interactive()

# st.checkbox for dark mode (SiS Container compatible)
st.checkbox("Dark Mode", key="dark_mode")
```

### Must Avoid

```python
# ❌ st.column_config - breaks SiS Container
# ❌ st.toggle() - may not be available
# ❌ st.dataframe(hide_index=True) - not in older versions
# ❌ st.bar_chart() - colors vary across environments
# ❌ External fonts - blocked by CSP
# ❌ Altair xOffset - requires Altair 5.0+
```

See `references/version-matrix.md` for full compatibility table.

---

## Model Loading Strategy

| Model | Load on Trigger | Load as Needed |
|-------|-----------------|----------------|
| **Haiku** | SKILL.md + workflow-details.md + chart-patterns.md | Other references |
| **Sonnet** | SKILL.md | Navigate with grep patterns |
| **Opus** | SKILL.md | Load references on-demand |

For model-specific guidance, see `references/model-guidance.md`.

---

## Finding Specific Patterns

Navigate large reference files with grep:

```bash
# Chart patterns
grep -n "mark_bar\|mark_line\|mark_area" references/chart-patterns.md

# Deployment troubleshooting
grep -n "Error\|Fix\|WRONG" references/snowflake-deployment.md

# CSS patterns
grep -n "icon-nav\|tiles-panel" assets/templates/css/*.css
```

---

## Visual Validation JSON Output

The `scripts/visual-validate.py` script outputs JSON for parsing:

```json
{
  "iteration": 1,
  "score_percent": 75,
  "improvements": ["Add left icon navigation", "Add chart titles"],
  "continue_to_next": true,
  "early_exit": false
}
```

| Field | Description |
|-------|-------------|
| `score_percent` | 0-100 quality score |
| `improvements` | List of specific fixes needed |
| `continue_to_next` | Whether to run next iteration |
| `early_exit` | True if score >= 90% after iteration 2 |

---

## Script Reference

| Script | Usage | Notes |
|--------|-------|-------|
| `visual-validate.py` | `python scripts/visual-validate.py . 1 --auto` | Captures screenshot, scores layout |
| `visual-validate.py` | `python scripts/visual-validate.py . 2 --auto --early-exit 90` | Early exit if score ≥90% |
| `visual-validate.py` | `python scripts/visual-validate.py . 1 --fast` | Code analysis only, no screenshot |
| `self-assess.py` | `python scripts/self-assess.py` | Quick code quality check |
| `validate-compat.py` | `python scripts/validate-compat.py streamlit_app.py` | SiS compatibility check |

**Playwright install (required for visual-validate.py):**

```bash
uv pip install playwright && uv run playwright install chromium
```

---

## File Structure

### Localhost Only (Default)

```
project/
├── .gitignore           # Credentials protection
├── streamlit_app.py     # Main application
└── pyproject.toml       # uv dependencies
```

### After Deployment Request

```
project/
├── .gitignore
├── streamlit_app.py
├── pyproject.toml
├── environment.yml      # SiS Warehouse (Conda)
├── requirements.txt     # SiS Container (pip)
├── snowflake.yml        # Snowflake CLI config
└── spcs/
    ├── Dockerfile
    ├── spec.yaml
    └── requirements-spcs.txt
```

Templates available in `assets/templates/`.

---

## Common Issues Quick Fix

| Issue | Fix |
|-------|-----|
| Version specifiers in environment.yml | Remove `>=`, `==` — plain names only |
| `snow connection add` fails | Edit `~/.snowflake/config.toml` directly |
| st.toggle() not available | Use `st.checkbox()` |
| Altair xOffset not supported | Use `column` faceting |
| Empty stacked bar chart | Ensure long-format data |

See `references/troubleshooting.md` for detailed solutions.

---

## Testing This Skill

Verify the skill works correctly:

1. **Basic Test:** Provide `assets/example-wireframe.png` as input
   - Expected: Working localhost app at http://localhost:8501
   - Verify: `curl -sf http://localhost:8501/_stcore/health`

2. **Code Quality Check:**
   ```bash
   python scripts/self-assess.py
   ```

3. **Validation Test:**
   ```bash
   python scripts/visual-validate.py . 1 --fast
   ```

4. **Compatibility Check:**
   ```bash
   python scripts/validate-compat.py streamlit_app.py
   ```

---

## Output Templates

### Localhost Ready

```
Streamlit app is running at http://localhost:8501

Options:
  - "validate visually" - run visual validation
  - "deploy to snowflake" - generate deployment files
```

### After Snowflake Deployment

```
Snowflake deployment complete.

Deployed to:
  - Localhost: http://localhost:8501
  - SiS Warehouse: [URL]
  - SiS Container: [URL]
  - SPCS: [URL]
```
