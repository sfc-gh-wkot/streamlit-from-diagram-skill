# Streamlit from Diagram Skill

A Claude Code project-level skill that generates Streamlit dashboards from wireframes, sketches, or screenshots.

## What is this?

This is a **Claude Code Agent Skill** that teaches Claude how to transform visual wireframes into fully functional Streamlit applications. It supports deployment to multiple environments:

1. **Localhost** — Local development with uv
2. **SiS Warehouse** — Streamlit in Snowflake (Warehouse runtime)
3. **SiS Container** — Streamlit in Snowflake (Container runtime)
4. **Raw SPCS** — Custom Docker on Snowpark Container Services

## Installation

### Option 1: Clone into your project

Clone this repository and copy the `.claude/` directory into your project:

```bash
git clone https://github.com/YOUR_USERNAME/streamlit-from-diagram-skill.git
cp -r streamlit-from-diagram-skill/.claude your-project/
```

### Option 2: Use as a standalone project

Clone and use this repository directly as your project workspace:

```bash
git clone https://github.com/YOUR_USERNAME/streamlit-from-diagram-skill.git
cd streamlit-from-diagram-skill
```

## Usage

Once the skill is in your project's `.claude/skills/` directory, Claude Code will automatically detect and use it when you:

1. Share a wireframe/screenshot image
2. Ask Claude to "create a Streamlit dashboard from this wireframe"
3. Ask Claude to "generate a dashboard that looks like this"

### Quick Start

```
# In Claude Code, share your wireframe image and say:
"Create a Streamlit dashboard from this wireframe"
```

Claude will:
1. Analyze the wireframe thoroughly
2. Generate `streamlit_app.py` and `pyproject.toml`
3. Run linting (ruff)
4. Start the app locally at http://localhost:8501

### Optional Commands

- **"validate visually"** — Run visual validation with Playwright screenshots
- **"deploy to snowflake"** — Generate deployment files for Snowflake environments

## Skill Structure

```
.claude/skills/streamlit-from-diagram-skill/
├── SKILL.md                    # Main skill definition
├── assets/                     # Documentation assets
│   └── screenshots-catalog.md
├── examples/                   # Template files
│   ├── streamlit_app.py
│   ├── pyproject.toml
│   ├── environment.yml
│   ├── requirements.txt
│   ├── snowflake.yml
│   └── spcs/
│       ├── Dockerfile
│       ├── requirements-spcs.txt
│       └── spec.yaml
├── references/                 # Reference documentation
│   ├── component-mapping.md
│   ├── deployment-checklist.md
│   ├── example-dashboard.md
│   ├── spcs-setup.md
│   └── troubleshooting.md
└── scripts/                    # Validation scripts
    ├── auto-screenshot.py
    ├── fast-health-check.sh
    ├── init-project.sh
    ├── self-assess.py
    ├── setup-spcs.sql
    ├── validate-compat.py
    └── visual-validate.py
```

## Requirements

- **Claude Code** — This skill is designed for [Claude Code](https://code.claude.com)
- **uv** — Modern Python package manager
- **ruff** — Python linter and formatter
- **Playwright** (optional) — For visual validation

## Learn More

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Snowflake Streamlit Documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)

## License

MIT License - See skill files for details.
