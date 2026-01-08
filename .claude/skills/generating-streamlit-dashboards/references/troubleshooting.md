# Troubleshooting Guide

## Contents

- [Lessons from Common Failures](#lessons-from-common-failures)
- [Skill Failure Modes](#skill-failure-modes)
- [HTML Rendering Issues](#html-rendering-issues)
- [CSS Rendering Issues](#css-rendering-issues)
- [All Environments](#all-environments)
- [Localhost Issues](#localhost-issues)
- [SiS Warehouse Issues](#sis-warehouse-issues)
- [SiS Container Issues](#sis-container-issues)
- [Raw SPCS Issues](#raw-spcs-issues)
- [Debugging Commands](#debugging-commands)

---

## Lessons from Common Failures

Patterns that have caused issues in real usage — learn from these to avoid repeating them.

| Failure Pattern | How It Manifests | Prevention |
|-----------------|------------------|------------|
| HTML form elements | Raw `<input>` shows as text | Use Streamlit native widgets or `<div>` mocks |
| Placeholder content | Charts say "Value", cards say "Item" | Transform ALL placeholders to domain-specific content |
| Missing chart labels | Axis shows column names like "order" | Always specify `title=` in Altair encoding |
| Single monolithic file | 600+ line file, untestable | Use modular structure for dashboards >300 lines |
| Unicode in HTML | Special characters break rendering | Use plain ASCII or HTML entities |

---

## Skill Failure Modes

Common ways the skill can fail and how to fix them.

### Deployment Without Explicit Request

| Symptom | Cause | Fix |
|---------|-------|-----|
| Creates deployment files during Phase 1 | Misinterpreted "can deploy to X" as deployment request | Only trigger Phase 3 on explicit "deploy to snowflake/sis/spcs" |
| Auto-deploys after localhost | Didn't STOP after Phase 1 | Ensure skill outputs localhost URL and STOPS |

### Missing Visual Elements

| Symptom | Cause | Fix |
|---------|-------|-----|
| No left icon navigation | Didn't scan left edge of wireframe | Run Edge Scan Protocol - check for circles on left |
| No right tiles panel | Didn't scan right edge | Check for "Tiles" label or vertical bar on right |
| Missing navbar | Didn't scan top edge | Check for logo/search/profile at top |

### Placeholder Content

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cards say "Predictive Item" | Skipped content generation | Transform EVERY placeholder to specific content |
| Charts have no titles | Missed chart title requirement | Add `st.markdown("**Title**")` before each chart |
| Generic button text | Used wireframe labels literally | Generate contextual action text |

### Wrong File Order

| Symptom | Cause | Fix |
|---------|-------|-----|
| Credentials committed | Created files before .gitignore | ALWAYS create .gitignore FIRST |
| Deployment files in Phase 1 | Created environment.yml/requirements.txt too early | Only `streamlit_app.py` + `pyproject.toml` in Phase 1 |

### Validation Loop Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Runs forever | Didn't check iteration count | Maximum 3 iterations, early exit at 90% |
| Doesn't parse improvements | Not reading JSON output | Parse `improvements` array from script output |
| Playwright errors | Missing installation | Run `uv pip install playwright && uv run playwright install chromium` |

### Color Inconsistency

| Symptom | Cause | Fix |
|---------|-------|-----|
| Charts have different colors | Used `st.bar_chart()` | Use Altair with explicit `color="#4A90D9"` |
| Theme looks wrong in SiS | Used external fonts | Use system fonts only (CSP blocks external) |

---

## HTML Rendering Issues

Streamlit's `st.markdown(unsafe_allow_html=True)` has a sanitizer that strips or breaks certain HTML patterns.

| Issue | Cause | Fix |
|-------|-------|-----|
| Raw HTML displayed as text | `st.markdown` with `<input>`, `<textarea>`, `<button>` | Replace with `<div>` elements or use native Streamlit widgets |
| HTML breaks after emoji | Unicode characters (▾, ◆, ▷) break sanitizer | Remove special Unicode, use HTML entities or plain text |
| Multi-line HTML renders as text | Newlines in HTML string | Use single-line HTML or split into multiple `st.markdown()` calls |
| HTML comments visible | `<!-- comments -->` not stripped cleanly | Remove all HTML comments from `st.markdown` content |

**Common sanitized/stripped elements:**
- `<input>`, `<textarea>`, `<select>`, `<button>` — Use Streamlit widgets instead
- `<form>` — Use `st.form()` instead
- `<script>`, `<iframe>` — Blocked for security
- Event handlers (`onclick`, `onmouseover`) — Stripped

**Working workaround for form-like UI:**
```python
# ❌ WRONG - Input elements stripped
st.markdown('<input type="text" placeholder="Search...">', unsafe_allow_html=True)

# ✅ CORRECT - Use div for visual mock, Streamlit for function
st.markdown('<div class="search-box">🔍 Search...</div>', unsafe_allow_html=True)
# Or use native widget:
st.text_input("Search", placeholder="Search...", label_visibility="collapsed")
```

---

## CSS Rendering Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Fixed position elements overlap | Navbar covers content | Add `padding-top` to main content container |
| CSS not applied | Styles appear but don't render | Check for typos, ensure `unsafe_allow_html=True` |
| Dark mode breaks layout | Colors inverted incorrectly | Use CSS variables or explicit color definitions |
| Styles leak between components | Unintended inheritance | Use unique class prefixes (e.g., `.my-app-card`) |
| CSS variables not working | `var(--color)` shows literally | Ensure CSS block with variables loads before usage |

**CSS debugging pattern:**
```python
# Add visible border to debug layout issues
st.markdown("""
<style>
.debug * { border: 1px solid red !important; }
</style>
""", unsafe_allow_html=True)
```

---

## Common Issues by Environment

### All Environments

#### Issue: Charts have different colors

**Symptom:** Same code produces blue bars locally, yellow bars in SiS.

**Cause:** Default chart palettes differ between Altair versions and Vega-Lite renderers.

**Solution:** Always use explicit colors in Altair charts:

```python
# ❌ WRONG - Default colors
st.bar_chart(df)

# ✅ CORRECT - Explicit Altair colors
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(...)
st.altair_chart(chart, use_container_width=True)
```

---

### Localhost Issues

#### Issue: Port 8501 already in use

**Symptom:** `Address already in use` error on startup.

**Solution:**
```bash
pkill -f "streamlit run"
# or
lsof -ti:8501 | xargs kill -9
```

#### Issue: Dependencies not found

**Symptom:** `ModuleNotFoundError` for pandas, altair, etc.

**Solution:**
```bash
uv sync
uv run streamlit run streamlit_app.py
```

---

### SiS Warehouse Issues

#### Issue: Stage does not exist

**Symptom:** `Stage 'X' does not exist or not authorized`

**Solution:** Check `snowflake.yml` has correct warehouse and that stage exists:
```sql
SHOW STAGES IN SCHEMA your_db.your_schema;
CREATE STAGE IF NOT EXISTS your_stage;
```

#### Issue: Cached version showing after redeploy

**Symptom:** Changes not visible after `snow streamlit deploy`

**Solution:** Force clean redeploy:
```sql
DROP STREAMLIT IF EXISTS your_app;
```
Then redeploy:
```bash
snow streamlit deploy your_app --connection conn --replace
```

---

### SiS Container Issues

#### Issue: `st.column_config` error

**Symptom:**
```
AttributeError: module 'streamlit' has no attribute 'column_config'
```

**Cause:** SiS Container runtime uses older Streamlit (~1.35) that lacks this feature.

**Solution:** Use pandas formatting instead:
```python
# ❌ BROKEN in SiS Container
st.dataframe(df, column_config={
    "Revenue": st.column_config.NumberColumn(format="$%d")
})

# ✅ WORKS everywhere
df["Revenue"] = df["Revenue"].apply(lambda x: f"${x:,}")
st.dataframe(df)
```

---

### Raw SPCS Issues

#### Issue: "No service hosts found" error

**Symptom:** Browser shows JSON error:
```json
{"responseType":"ERROR","detail":"Service MY_SERVICE not reachable: no service hosts found."}
```

**Causes (in order of likelihood):**
1. **Service still starting** — Compute pool provisioning + container pull takes 2-5 minutes
2. **Container crashed** — App failed to start (check logs)
3. **Readiness probe failing** — Health check endpoint not responding
4. **Compute pool suspended** — No nodes available

**Diagnosis:**
```sql
-- 1. Check service status (look for READY status)
SHOW SERVICES LIKE '%MY_SERVICE%';

-- 2. Check if container is running
DESCRIBE SERVICE MY_SERVICE;

-- 3. Check compute pool has nodes
SHOW COMPUTE POOLS;
DESCRIBE COMPUTE POOL MY_POOL;  -- Check MIN_NODES > 0

-- 4. Check container logs for crash
SELECT * FROM TABLE(GET_SERVICE_LOGS('MY_SERVICE', 'streamlit'))
ORDER BY timestamp DESC LIMIT 50;

-- 5. Check endpoint provisioning status
SHOW ENDPOINTS IN SERVICE MY_SERVICE;
```

**Solutions:**

**If service is PENDING/STARTING:** Wait 2-5 minutes for compute pool to provision nodes.

**If container crashed:** Check logs for Python errors:
```sql
SELECT * FROM TABLE(GET_SERVICE_LOGS('MY_SERVICE', 'streamlit'));
```
Common causes: missing dependencies, syntax errors, port binding issues.

**If compute pool suspended:**
```sql
ALTER COMPUTE POOL MY_POOL RESUME;
```

**If readiness probe failing:** Ensure your app exposes `/_stcore/health`:
```yaml
readinessProbe:
  port: 8501
  path: /_stcore/health
```

**If endpoint still provisioning:** Public endpoints take 2-5 minutes after service starts:
```sql
-- Poll until URL appears (not "Endpoints provisioning in progress...")
SHOW ENDPOINTS IN SERVICE MY_SERVICE;
```

---

#### Issue: Docker login fails with MFA

**Symptom:** `MFA authentication is required`

**Solution:** Use snow CLI for registry login:
```bash
snow spcs image-registry login --connection your_conn
```

#### Issue: Service fails with architecture error

**Symptom:**
```
SPCS only supports image for amd64 architecture
```

**Cause:** Image built for arm64 (Apple Silicon Mac).

**Solution:** Always build for linux/amd64:
```bash
docker build --platform linux/amd64 -t image:tag .
```

#### Issue: Compute pool type incompatible (Raw SPCS only)

**Symptom:**
```
Compute pool SYSTEM_COMPUTE_POOL_CPU can only support services of type [NOTEBOOK, MODEL_SERVING, STREAMLIT, ML_JOB]
```

**Cause:** `SYSTEM_COMPUTE_POOL_CPU` supports STREAMLIT apps (SiS Container) but NOT raw SPCS services (CREATE SERVICE).

**For SiS Container (CREATE STREAMLIT):** ✅ Use `SYSTEM_COMPUTE_POOL_CPU`:
```sql
CREATE STREAMLIT my_app
  FROM '@stage/'
  MAIN_FILE = 'streamlit_app.py'
  COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU;  -- ✅ Works for STREAMLIT
```

**For Raw SPCS (CREATE SERVICE):** ❌ Must create custom compute pool:
```sql
-- System pool doesn't work for CREATE SERVICE
CREATE COMPUTE POOL my_compute_pool
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_XS;

CREATE SERVICE my_service
  IN COMPUTE POOL my_compute_pool  -- Custom pool required
  FROM SPECIFICATION $$...$$;
```

#### Issue: "Insufficient CPU resources"

**Symptom:**
```
insufficient CPU resources to schedule all service instances
```

**Cause:** Compute pool at capacity - requested resources exceed available nodes.

**Solutions:**

1. **Reduce resource requests** (recommended):
```yaml
resources:
  requests:
    memory: 512Mi  # Reduced from 1Gi
    cpu: 0.25      # Reduced from 0.5
  limits:
    memory: 1Gi
    cpu: 0.5
```

2. **Check pool capacity:**
```sql
SELECT * FROM TABLE(SYSTEM$GET_COMPUTE_POOL_STATUS('MY_POOL'));
```

3. **Use a different pool or scale up:**
```sql
-- Scale up existing pool
ALTER COMPUTE POOL MY_POOL SET MAX_NODES = 3;

-- Or use a different pool
CREATE SERVICE ... IN COMPUTE POOL DIFFERENT_POOL ...
```

---

## Debugging Commands

### Localhost

```bash
# Check Streamlit version
uv run python -c "import streamlit; print(streamlit.__version__)"

# Run with debug logging
uv run streamlit run streamlit_app.py --logger.level=debug
```

### SiS (Both Runtimes)

```sql
-- Check app status
SHOW STREAMLITS;

-- Get app details
DESCRIBE STREAMLIT my_app;

-- View app URL
SELECT SYSTEM$GET_STREAMLIT_URL('MY_DB.MY_SCHEMA.MY_APP');
```

### Raw SPCS

```sql
-- Service status
SHOW SERVICES;
DESCRIBE SERVICE my_service;

-- Container logs
SELECT * FROM TABLE(GET_SERVICE_LOGS('my_service', 'streamlit')) 
ORDER BY timestamp DESC LIMIT 100;

-- Service endpoints
SHOW ENDPOINTS IN SERVICE my_service;

-- Compute pool status
SHOW COMPUTE POOLS;
DESCRIBE COMPUTE POOL my_pool;
```
