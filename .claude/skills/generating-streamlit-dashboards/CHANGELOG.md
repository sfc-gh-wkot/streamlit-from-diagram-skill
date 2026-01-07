# Changelog

All notable changes to this skill are documented in this file.

## [2.4.0] - 2026-01-08

### Added

- **Quick Start Example** in SKILL.md showing input/output expectations
- **Negative triggers** in description ("DOES NOT TRIGGER" section)
- **Degrees of freedom markers** ([LOW/MEDIUM/HIGH FREEDOM]) for each phase
- **Model-specific loading hints** with file loading strategy per model
- **`layout-patterns.md`** - Extracted navigation, panels, cards patterns
- **`css-patterns.md`** - Extracted all CSS patterns and theming
- **`assets/README.md`** - Documentation of asset folder structure
- **`scripts/run-evaluations.py`** - Runnable evaluation test harness
- **Skill Failure Modes** section in troubleshooting.md with common issues table
- **Collapsible legacy sections** in version-matrix.md for version-sensitive info

### Changed

- **`component-mapping.md` reduced from 573 to ~200 lines** - Now references layout-patterns.md, css-patterns.md, and chart-patterns.md
- **Description format** now includes explicit TRIGGERS and DOES NOT TRIGGER sections
- **Version-matrix.md** uses `<details>` collapsible sections for legacy patterns
- **Model compatibility notes** expanded with file loading strategy column

### Fixed

- Removed duplicated CSS/HTML patterns between component-mapping.md and new split files
- Time-sensitive version information now in collapsible "reference only" sections

## [2.3.0] - 2026-01-08

### Changed

- **Description optimized**: Added explicit trigger keywords for better skill discovery ("create dashboard", "build app from wireframe", "convert this design to Streamlit")
- **Edge Scan section condensed**: Removed duplication with workflow-details.md; now references detailed procedures
- **Script Reference table expanded**: Added usage examples with flags (`--auto`, `--fast`, `--early-exit`)
- **Security warnings strengthened**: Added ⚠️ ALL-CAPS warnings for NEVER/ALWAYS/DO NO HARM rules
- **Nested references removed**: component-mapping.md now has inline chart example instead of referencing chart-patterns.md

### Added

- Model compatibility notes section in SKILL.md (Haiku/Sonnet/Opus guidance)
- Grading rubric to all evaluation JSON files:
  - `pass_threshold`, `partial_pass_threshold`
  - `critical_behaviors` array
  - `scoring` object with pass/partial/fail definitions
- Enhanced evaluations/README.md with grading structure documentation

### Fixed

- Evaluation test files now use existing `assets/example-wireframe.png` instead of missing `test-files/` paths
- Removed cross-references between reference files (kept references one level deep from SKILL.md)

## [2.2.0] - 2026-01-08

### Changed

- **BREAKING**: Renamed skill from `streamlit-snowflake-from-image` to `generating-streamlit-dashboards` (gerund form per Anthropic best practices)
- **BREAKING**: Moved CSS templates from `references/css/` to `assets/templates/css/`
- **BREAKING**: Moved HTML templates from `references/html/` to `assets/templates/html/`
- Removed non-standard frontmatter fields (`version`, `license`, `allowed-tools`)
- Enhanced description with more trigger keywords for better discovery
- Consolidated redundant Altair patterns (component-mapping.md now references chart-patterns.md)

### Added

- Table of Contents to all reference files over 100 lines:
  - component-mapping.md
  - chart-patterns.md
  - workflow-details.md
  - troubleshooting.md
  - snowflake-deployment.md
  - version-matrix.md
  - security-rules.md
- Copyable workflow checklists in Anthropic's recommended format
- `evaluations/` folder with test scenarios:
  - basic-localhost.json
  - visual-validation.json
  - snowflake-deploy.json
  - edge-cases.json

### Fixed

- Path references updated to new template locations
- Reduced redundancy between reference files

## [2.1.0] - 2026-01-07

### Changed

- **BREAKING**: Moved CSS templates from `assets/css/` to `references/css/`
- **BREAKING**: Moved HTML templates from `assets/html/` to `references/html/`
- **BREAKING**: Moved `examples/` folder to `references/examples/`
- Updated SKILL.md description to use third-person voice (per Anthropic best practices)
- Removed emojis from SKILL.md description
- Consolidated security rules into single source of truth (`references/security-rules.md`)
- Reduced duplication between SKILL.md and workflow-details.md

### Added

- `references/security-rules.md` - consolidated security guidelines
- Grep patterns section in SKILL.md for finding content in large files
- JSON output schema documentation for visual-validate.py
- Script dependencies table in SKILL.md
- Tool usage by phase documentation
- Skill self-test instructions section

### Fixed

- Path references in workflow-details.md now point to correct locations
- snowflake-deployment.md now references security-rules.md instead of duplicating

## [2.0.0] - 2026-01-07

### Changed

- **BREAKING**: Reduced SKILL.md from ~4,300 lines to ~300 lines
- **BREAKING**: Moved CSS/HTML templates to `assets/` folder
- **BREAKING**: Moved config templates to `assets/templates/` folder
- Consolidated iteration count to 3 (with early exit at 90%)
- Simplified output message requirements

### Added

- `assets/css/` folder with modular CSS files:
  - `base-theme.css` - Core variables and styles
  - `icon-nav.css` - Left icon navigation
  - `tiles-panel.css` - Right collapsible panel
  - `top-navbar.css` - Top navigation bar
  - `dark-theme.css` - Dark mode overrides
- `assets/html/` folder with HTML templates:
  - `icon-nav.html` - Left icon navigation markup
  - `tiles-panel.html` - Right tiles panel markup
  - `top-navbar.html` - Top navigation bar markup
  - `insight-card.html` - Sidebar card templates
  - `right-panel.html` - Right panel templates
- `assets/templates/` folder with config templates:
  - `pyproject.toml.template`
  - `environment.yml.template`
  - `requirements.txt.template`
  - `snowflake.yml.template`
  - `Dockerfile.template`
  - `spec.yaml.template`
  - `requirements-spcs.txt.template`
  - `gitignore.template`
- `references/workflow-details.md` - Complete workflow procedures
- `references/chart-patterns.md` - Altair chart examples
- `references/version-matrix.md` - Compatibility tables
- `references/snowflake-deployment.md` - Deployment guide
- `allowed-tools` field in SKILL.md frontmatter
- `license` field in SKILL.md frontmatter
- This CHANGELOG.md file
- LICENSE.txt file

### Removed

- Embedded CSS blocks from SKILL.md (moved to assets/)
- Embedded HTML templates from SKILL.md (moved to assets/)
- Embedded config templates from SKILL.md (moved to assets/templates/)
- Contradictory "5 iterations exactly" language
- Rigid "copy exactly" output format requirements
- Duplicate content between SKILL.md and references/

### Fixed

- Resolved contradictory iteration counts (now: 3 max with early exit)
- Removed duplicate CSS/HTML patterns appearing multiple times
- Simplified script invocation documentation

## [1.20.0] - Previous Release

- Original monolithic SKILL.md (~4,300 lines)
- All templates embedded inline
- Mixed 3/5 iteration guidance
