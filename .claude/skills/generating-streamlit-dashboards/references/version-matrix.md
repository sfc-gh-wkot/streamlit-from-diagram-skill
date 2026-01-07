# Version Compatibility Matrix

## Contents

- [Minimum Requirements](#minimum-requirements)
- [Environment Constraints](#environment-constraints)
- [Streamlit Feature Compatibility](#streamlit-feature-compatibility)
- [Altair Feature Compatibility](#altair-feature-compatibility)
- [Must AVOID (SiS Container)](#must-avoid-sis-container)
- [Must USE (Cross-Environment Safe)](#must-use-cross-environment-safe)
- [SiS Container Deployment Rules](#sis-container-deployment-rules)
- [Reference URLs](#reference-urls)
- [Tooling Requirements](#tooling-requirements)

---

## Minimum Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| **Python** | 3.11+ | 3.13.x | Use latest stable |
| **Streamlit** | 1.51+ | Latest in SiS | Check release notes |
| **pandas** | 2.0+ | Latest | Widely compatible |
| **numpy** | 1.24+ | Latest | Widely compatible |
| **Altair** | 4.0+ | 5.0+ | 5.0+ for localhost, 4.x for SiS Container |

---

## Environment Constraints

### Localhost

Full control - use latest PyPI versions.

### SiS Warehouse

- Uses Conda packages from `snowflake` channel
- **NO version specifiers** allowed in `environment.yml`
- Check [SiS Release Notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake) for current versions

### SiS Container (Preview)

- Uses pip packages
- May have older Streamlit version (~1.35)
- Altair 4.x (no xOffset, yOffset)
- Limited external network access

### Raw SPCS

Full control - use any PyPI version in Docker.

---

## Streamlit Feature Compatibility

| Feature | Recommended | Why |
|---------|-------------|-----|
| Toggle switch | `st.checkbox()` | `st.toggle()` not in older versions |
| Column formatting | Pandas `.apply()` | `st.column_config` not in SiS Container |
| Editable table | `st.dataframe()` | `st.data_editor` not in older versions |
| Hide index | `df.index = [""] * len(df)` | `hide_index=True` not in SiS Container |
| Chat input | `st.text_input()` | `st.chat_input` not in older versions |
| Bar chart | `alt.Chart().mark_bar()` | `st.bar_chart()` colors vary |
| Fonts | System fonts | External fonts blocked by CSP |

<details>
<summary>Feature Version Requirements (reference only)</summary>

| Feature | Min Version | SiS Container Status |
|---------|-------------|---------------------|
| `st.toggle()` | 1.23+ | ⚠️ Maybe not available |
| `st.column_config` | 1.35+ | ❌ Not available |
| `st.data_editor` | 1.23+ | ⚠️ Maybe not available |
| `st.dataframe(hide_index=True)` | 1.16+ | ❌ Not available |
| `st.chat_input` | 1.23+ | ⚠️ Maybe not available |

</details>

---

## Altair Feature Compatibility

| Feature | Current Method | Alternative for SiS Container |
|---------|----------------|------------------------------|
| Grouped bars | `xOffset` encoding | `column` faceting |
| Stacked rows | `yOffset` encoding | `row` faceting |
| Dynamic expressions | `alt.expr()` | `alt.datum` |
| Interactive params | `alt.param()` | `alt.selection()` |

<details>
<summary>Legacy Altair 4.x Patterns (for SiS Container)</summary>

SiS Container uses Altair 4.x which lacks `xOffset`/`yOffset`. Use faceting instead:

```python
# Altair 5.x (localhost) - grouped bars with xOffset
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X("category:N"),
    xOffset=alt.XOffset("group:N"),  # Not in 4.x!
    y=alt.Y("value:Q"),
    color="group:N"
)

# Altair 4.x compatible - use column faceting
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X("group:N", title=""),
    y=alt.Y("value:Q"),
    color="group:N",
    column=alt.Column("category:N", title="")  # Facet instead
).properties(width=100)
```

</details>

---

## Must AVOID (SiS Container)

```python
# ❌ Breaks in SiS Container
st.toggle("Dark Mode")                      # Use st.checkbox()
st.column_config.NumberColumn()             # Use pandas formatting
st.data_editor(df)                          # Use st.dataframe()
st.dataframe(df, hide_index=True)           # Use df.index = [""] * len(df)

# ❌ Altair 5.0+ features
chart.encode(xOffset="field:N")             # Use column= faceting
chart.encode(yOffset="field:N")             # Use row= faceting

# ❌ Inconsistent colors
st.bar_chart(df)                            # Use Altair with explicit colors
st.line_chart(df)

# ❌ Blocked by CSP
@import url('https://fonts.googleapis.com/...')
```

---

## Must USE (Cross-Environment Safe)

```python
# ✅ st.checkbox instead of st.toggle
dark_mode = st.checkbox("🌙 Dark Mode", key="dark_mode")

# ✅ Hide index without hide_index parameter
df.index = [""] * len(df)
st.dataframe(df, use_container_width=True)

# ✅ Explicit Altair with hardcoded colors
alt.Chart(df).mark_bar(color="#4A90D9").encode(...)

# ✅ Grouped bars using column faceting (Altair 4.x compatible)
alt.Chart(data).mark_bar().encode(
    x=alt.X("Group:N"),
    y=alt.Y("Value:Q"),
    color="Group:N",
    column=alt.Column("Category:N"),
).properties(width=100)

# ✅ Pandas formatting
df["Revenue"] = df["Revenue"].apply(lambda x: f"${x:,}")

# ✅ System fonts only
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

---

## SiS Container Deployment Rules

1. **No `runtime:` in snowflake.yml** - Deploy via SQL instead
2. **No `RUNTIME_NAME`** - Just specify `COMPUTE_POOL`
3. **No `EXTERNAL_ACCESS_INTEGRATIONS`** - Not needed for demo dashboards
4. **Use `st.checkbox()`** - `st.toggle()` may not be available
5. **Prefer system resources:**
   - `SYSTEM_COMPUTE_POOL_CPU`
   - `SYSTEM$STREAMLIT_NOTEBOOK_WH`

---

## Reference URLs

| Resource | URL |
|----------|-----|
| SiS Release Notes | https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake |
| SiS Limitations | https://docs.snowflake.com/en/developer-guide/streamlit/limitations |
| PyPI Streamlit | https://pypi.org/project/streamlit/ |
| Altair Docs | https://altair-viz.github.io/ |

---

## Tooling Requirements

```bash
# Install/update latest tooling
uv self update              # Update uv itself
uv tool install ruff        # Latest ruff
uv tool install ty          # Latest ty
```

| Tool | Purpose | Command |
|------|---------|---------|
| **uv** | Package management | `uv sync`, `uv run` |
| **ruff** | Linting + formatting | `ruff check --fix && ruff format` |
| **ty** | Type checking | `ty check` |
