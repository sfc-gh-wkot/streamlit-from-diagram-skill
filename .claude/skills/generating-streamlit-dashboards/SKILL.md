---
name: generating-streamlit-dashboards
description: |
  Generates production-ready Streamlit dashboards from wireframes, screenshots, mockups, or UI designs.
  TRIGGERS: "create dashboard", "build app from wireframe", "convert design to Streamlit", "make this into a Streamlit app"
  DOES NOT TRIGGER: general Streamlit questions, debugging existing apps, API help, modifying existing dashboards
  Deploys to localhost by default; Snowflake deployment ONLY on explicit "deploy to snowflake/sis/spcs" request.
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
| Version compatibility | `references/version-matrix.md` |
| Snowflake deployment | `references/snowflake-deployment.md` |
| Security rules | `references/security-rules.md` |
| Troubleshooting | `references/troubleshooting.md` |
| CSS templates | `assets/templates/css/` |
| HTML templates | `assets/templates/html/` |
| Config templates | `assets/templates/` |
| Example app | `references/examples/` |
| Evaluations | `evaluations/` |

---

## Quick Start Example

**Input:** User provides `wireframe.png` showing sidebar with 3 cards, main area with 2 charts, left icon nav

**Output:**
```
project/
├── .gitignore           ← Created FIRST (credential protection)
├── streamlit_app.py     ← 3 insight cards, 2 Altair charts, icon nav
└── pyproject.toml       ← uv dependencies
```

**Result:** App running at http://localhost:8501, git committed, STOP and wait for user.

**What happens next:**
- User says "validate visually" → Run visual validation loop (up to 3 iterations)
- User says "deploy to snowflake" → Generate deployment files
- User says nothing → Skill is complete

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

⚠️ Create files in EXACT order: `.gitignore` → `streamlit_app.py` → `pyproject.toml`

### Phase 2: Visual Validation (Optional) [MEDIUM FREEDOM]

**Trigger:** User says "validate visually"
**Duration:** ~2-3 minutes
**Output:** Score and improvements list

Runs up to 3 iterations with early exit at 90%. Implement improvements as needed.

### Phase 3: Snowflake Deployment (Optional) [LOW FREEDOM]

**Trigger:** User explicitly says "deploy to snowflake/sis/spcs"
**Duration:** ~5 minutes
**Output:** URLs for deployed environments

⚠️ NOT triggered by: "can be deployed to X, Y, Z" (capability description)

---

## Tool Usage by Phase

| Phase | Primary Tools | Purpose |
|-------|---------------|---------|
| Localhost | Write, Bash | Generate files, run app |
| Validation | Read, Bash | Analyze code, run scripts |
| Deployment | Bash, Grep | Find tokens, deploy |

---

## Wireframe Analysis Protocol [HIGH FREEDOM]

See `references/workflow-details.md#phase-1-localhost-generation` for complete procedures.

**Quick checklist:**
1. **Edge Scan** — Check all 4 edges for navigation elements (icons left, tiles right, navbar top)
2. **Element Inventory** — Count exact number of cards, charts, metrics
3. **Content Generation** — Transform ALL placeholders into specific, meaningful content

**NEVER use placeholder text.** Every "Predictive Item" becomes "Revenue Forecast", every box with lines becomes a real card with metrics.

Use judgment to select appropriate content based on wireframe context (e.g., finance dashboard → revenue/costs, analytics → traffic/conversions).

---

## Code Generation Rules

### Toolchain

| Tool | Purpose | Command |
|------|---------|---------|
| **uv** | Package management | `uv sync`, `uv run` |
| **ruff** | Lint + format | `ruff check --fix && ruff format` |
| **ty** | Type check (optional) | `ty check` |

### Must Use

```python
# Altair with explicit colors
alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:N", title="Month"),
    y=alt.Y("value:Q", title="Revenue ($)"),
    tooltip=["month", alt.Tooltip("value:Q", format="$,.0f")]
)

# Charts always have titles
st.markdown("**Monthly Revenue**")
st.altair_chart(chart, use_container_width=True)

# Pandas formatting for tables
df["Revenue"] = df["Revenue"].apply(lambda x: f"${x:,}")

# st.checkbox for dark mode (SiS Container compatible)
st.checkbox("Dark Mode", key="dark_mode")
```

### Must Avoid

```python
# st.column_config - breaks SiS Container
# st.toggle() - may not be available
# st.dataframe(hide_index=True) - not in older versions
# st.bar_chart() - colors vary across environments
# External fonts - blocked by CSP
# Altair xOffset - requires Altair 5.0+
```

See `references/version-matrix.md` for full compatibility table.

---

## Finding Specific Patterns

For large reference files, use grep:

```bash
# Chart patterns
grep -n "mark_bar\|mark_line\|mark_area" references/chart-patterns.md
grep -n "Stacked\|Grouped\|Pie" references/chart-patterns.md

# Deployment troubleshooting
grep -n "Error\|Fix\|WRONG" references/snowflake-deployment.md
grep -n "SiS Container" references/version-matrix.md

# CSS patterns
grep -n "icon-nav\|tiles-panel" assets/templates/css/*.css
```

---

## Visual Validation JSON Output

The `scripts/visual-validate.py` script outputs JSON for parsing:

```json
{
  "iteration": 1,
  "score": 75,
  "score_percent": 75,
  "improvements": [
    "Add left icon navigation",
    "Add chart titles",
    "Add chart tooltips"
  ],
  "screenshot": "/path/to/.screenshot_iter_1.png",
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
| Version specifiers in environment.yml | Remove `>=`, `==` - plain names only |
| `snow connection add` fails | Edit `~/.snowflake/config.toml` directly |
| st.toggle() not available | Use `st.checkbox()` |
| Altair xOffset not supported | Use `column` faceting |
| Empty stacked bar chart | Ensure long-format data |

See `references/troubleshooting.md` for detailed solutions.

---

## Testing This Skill

To verify the skill is working correctly:

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
   - Expected: JSON output with score and improvements

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

---

## Model Compatibility Notes

| Model | Guidance | File Loading Strategy |
|-------|----------|----------------------|
| **Claude Haiku** | May need chart patterns copied into context | Load `chart-patterns.md` and `component-mapping.md` proactively; grep patterns may not be followed reliably |
| **Claude Sonnet** | Works well with reference file navigation | Use grep patterns to find specific sections; load files on-demand |
| **Claude Opus** | Can infer patterns from minimal examples | Rely on SKILL.md alone when possible; avoid loading verbose references unless needed |

**Loading priority by phase:**
- Phase 1: `workflow-details.md`, `component-mapping.md`
- Phase 2: `chart-patterns.md` (for improvements)
- Phase 3: `snowflake-deployment.md`, `security-rules.md`

For all models: Keep context focused by loading only relevant reference files.
