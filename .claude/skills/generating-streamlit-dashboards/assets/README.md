# Assets Directory

This folder contains templates, examples, and test files for the skill.

## Structure

| Path | Purpose | When to Use |
|------|---------|-------------|
| `templates/css/` | Modular CSS files for navigation, panels, themes | Copy into `streamlit_app.py` as needed |
| `templates/html/` | HTML component snippets | Copy into `st.markdown()` calls |
| `templates/*.template` | Config file templates for deployment | Copy and customize for Phase 3 |
| `example-wireframe.png` | Test input for skill evaluation | Use in evaluations and self-tests |
| `screenshots-catalog.md` | Example screenshots reference | Reference for visual validation |

## Template Files

### CSS Templates (`templates/css/`)

| File | Purpose |
|------|---------|
| `base-theme.css` | Core variables and common styles |
| `dark-theme.css` | Dark mode overrides |
| `icon-nav.css` | Left icon navigation styling |
| `tiles-panel.css` | Right tiles panel styling |
| `top-navbar.css` | Top navigation bar styling |

### HTML Templates (`templates/html/`)

| File | Purpose |
|------|---------|
| `icon-nav.html` | Left icon navigation markup |
| `tiles-panel.html` | Right tiles panel markup |
| `top-navbar.html` | Top navigation bar markup |
| `insight-card.html` | Sidebar card templates |
| `right-panel.html` | Right panel templates |

### Config Templates (`templates/`)

| File | Target Environment |
|------|-------------------|
| `pyproject.toml.template` | Localhost (uv) |
| `environment.yml.template` | SiS Warehouse (Conda) |
| `requirements.txt.template` | SiS Container (pip) |
| `snowflake.yml.template` | Snowflake CLI config |
| `gitignore.template` | All environments |
| `Dockerfile.template` | Raw SPCS |
| `spec.yaml.template` | Raw SPCS |
| `requirements-spcs.txt.template` | Raw SPCS |

## Usage

### Phase 1 (Localhost)

Only use:
- `pyproject.toml.template`
- `gitignore.template`
- CSS/HTML templates as needed

### Phase 3 (Snowflake Deployment)

Use based on target:
- **SiS Warehouse**: `environment.yml.template`, `snowflake.yml.template`
- **SiS Container**: `requirements.txt.template`, `snowflake.yml.template`
- **Raw SPCS**: All `spcs/` templates

## Test File

`example-wireframe.png` is used for:
1. Skill self-testing
2. Evaluation scenarios
3. Visual validation testing

To test the skill:
```bash
# Provide example-wireframe.png as input
# Expected: Working app at http://localhost:8501
```
