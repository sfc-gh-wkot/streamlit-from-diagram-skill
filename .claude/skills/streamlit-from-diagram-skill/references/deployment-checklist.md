# Pre-Deployment Checklist

## Code Compatibility

### Required Changes

- [ ] **No `st.column_config`** - Use pandas formatting instead
- [ ] **Explicit Altair charts** - All charts use `alt.Chart()` with hardcoded colors
- [ ] **System fonts only** - No external font imports
- [ ] **Python 3.11 syntax** - No Python 3.12+ features

## Configuration Files

### Localhost (pyproject.toml)

- [ ] Python version `>=3.11`
- [ ] Streamlit pinned to `==1.51.0`
- [ ] All dependencies listed
- [ ] Ruff configuration included

### SiS Warehouse (environment.yml)

- [ ] Channel is `snowflake` (not conda-forge)
- [ ] Streamlit version `=1.51.0` (single equals)

### SiS Container (requirements.txt)

- [ ] Streamlit `==1.51.0` (double equals)
- [ ] Only PyPI packages

### Snow CLI (snowflake.yml)

- [ ] `definition_version: 2`
- [ ] Entity name matches desired Streamlit name
- [ ] Correct `query_warehouse`
- [ ] `artifacts` lists all needed files

### SPCS Dockerfile

- [ ] Base image `python:3.11-slim`
- [ ] `uv` installed for dependency management
- [ ] Health check configured
- [ ] Port 8501 exposed

### SPCS spec.yaml

- [ ] Image path correct (full path with DB/SCHEMA/REPO)
- [ ] `public: true` on endpoint
- [ ] Readiness probe configured
- [ ] Resource limits appropriate

## File Structure

```
project/
├── streamlit_app.py        # Main application
├── pyproject.toml          # Localhost deps
├── environment.yml         # Warehouse deps
├── requirements.txt        # Container deps
├── snowflake.yml           # snow CLI config
└── spcs/
    ├── Dockerfile          # Container image
    ├── spec.yaml           # Service spec
    └── requirements-spcs.txt # SPCS deps
```

## Pre-Deploy Tests

### 1. Local Test

```bash
uv sync
uv run streamlit run streamlit_app.py
# Verify at http://localhost:8501
```

### 2. Lint Check

```bash
uv run ruff check .
uv run ruff format --check .
```

### 3. Docker Build Test

```bash
cd spcs
cp ../streamlit_app.py .
docker build --platform linux/amd64 -t test:latest .
docker run -p 8501:8501 test:latest
```

## Deployment Order

1. **Localhost** (always test first)
2. **SiS Warehouse** (most stable SiS option)
3. **SiS Container** (check for compatibility issues)
4. **Raw SPCS** (requires most setup)
