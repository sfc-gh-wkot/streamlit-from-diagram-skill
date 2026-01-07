# Troubleshooting Guide

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

#### Issue: Compute pool type incompatible

**Symptom:**
```
Compute pool SYSTEM_COMPUTE_POOL_CPU can only support services of type [NOTEBOOK, MODEL_SERVING, STREAMLIT, ML_JOB]
```

**Cause:** System compute pools are restricted. Raw SPCS services need custom pools.

**Solution:** Create dedicated compute pool:
```sql
CREATE COMPUTE POOL my_compute_pool
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_XS;
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
