# Changelog

All notable changes to this skill are documented in this file.

## [2.6.1] - 2026-01-08

### Added

- **Code Quality Standards section** in SKILL.md - Prominent notice requiring:
  - Modern Python (3.11+, type hints, f-strings)
  - Modular code (separated concerns)
  - Testable code (pure functions for data/charts)
  - Easy to navigate (logical structure, clear comments)
  - Easy to comprehend (descriptive names, docstrings)
- Quick example showing good vs bad code patterns

## [2.6.0] - 2026-01-08

### Changed

- **SKILL.md reduced from 563 lines (2,473 words) to 360 lines (1,401 words)** - Now within Anthropic's recommended <500 lines / 1,500-2,000 words
- **Description rewritten in third-person with quoted trigger phrases** per Anthropic best practices:
  - Positive: `"create dashboard from wireframe"`, `"convert this design to Streamlit"`, etc.
  - Negative: `"debug my Streamlit app"`, `"fix this Streamlit error"`, etc.
- **Writing style converted to imperative form** - Removed all second-person ("Use judgment" → "Select appropriate content")
- **Removed duplicated Interactive Elements Pattern** - Now references `interactivity-patterns.md`
- **Consolidated Quick Start Example** - Detailed tables moved to `content-requirements.md`

### Added

- **`references/content-requirements.md`** - Rich content requirements, transformation tables, sample data guidelines (extracted from SKILL.md)
- **`references/testability.md`** - Testability guidelines, pure function patterns, test templates (extracted from SKILL.md)
- **Model Loading Strategy table** in SKILL.md - Shows what each model (Haiku/Sonnet/Opus) should load upfront
- **Enhanced `evaluations/README.md`** with:
  - Example pass/partial/fail results
  - Manual testing checklist
  - New evaluation creation guide
- **Enhanced `scripts/validate-compat.py` docstring** with usage examples and detected issues

### Fixed

- Removed content duplication between SKILL.md and reference files
- All reference files now one level deep from SKILL.md (no nested references)

### Compliance

This version aligns with Anthropic Claude Code Skills best practices:
- ✅ SKILL.md body under 500 lines
- ✅ Third-person description with specific trigger phrases
- ✅ Imperative/infinitive writing style throughout
- ✅ Progressive disclosure with lean SKILL.md
- ✅ References one level deep
- ✅ At least 4 evaluations with grading rubrics
- ✅ Scripts with clear documentation

## [2.5.0] - 2026-01-08

### Added

- **`references/interactivity-patterns.md`** - New reference for session state, expandable cards, mock responses, chart interactivity
- **`references/model-guidance.md`** - Extracted model-specific guidance (Haiku/Sonnet/Opus) from SKILL.md
- **HTML Sanitization Rules** in troubleshooting.md - Documents Streamlit's HTML sanitizer behavior and workarounds
- **CSS Rendering Issues** section in troubleshooting.md - Common CSS problems and fixes
- **Lessons from Common Failures** section at top of troubleshooting.md - Quick reference table of failure patterns
- **Modular Project Structure** section in workflow-details.md - Architecture for complex dashboards (>300 lines)
- **Rich Content Requirements** checklist in SKILL.md - Minimum content requirements for UI elements
- **Testability Guidelines** section in SKILL.md - Pure function patterns for testable code
- **`@st.cache_data` pattern** in SKILL.md Must Use section
- **"What Good Output Looks Like"** section in SKILL.md with 5 quality requirements:
  - Sample Data (realistic numbers, not placeholders)
  - Visible Labels (axis labels, titles, legends)
  - Lightweight Interactivity (hover states, `.interactive()`)
  - Sample Content (domain-specific, story-telling text)
  - Mock Clickability (actionable buttons, AI suggestions, prompt input)
- **Sidebar Card Transformations** table showing "Predictive Item" → rich content mappings
- **KPI Card Transformations** table with specific formatting examples
- **Chart Requirements** section with complete Altair example including title, axis labels, tooltips
- **Right Panel Elements** table mapping tiles, AI suggestions, prompt input patterns
- **Interactive Elements Pattern** code example for AI suggestion buttons and prompt input
- Enhanced **Quick Start Example** with:
  - Detailed wireframe-to-output transformation table
  - Sample data requirements (formatted values, realistic variation)
  - Extended success criteria checklist

### Changed

- **SKILL.md description** now uses explicit POSITIVE/NEGATIVE TRIGGERS format
- **Model Compatibility Notes** moved to `references/model-guidance.md`, SKILL.md now has brief summary
- **Must Avoid** section expanded with HTML sanitizer warnings (form elements, Unicode in HTML)
- **Quick Reference table** updated with new reference files

### Fixed

- Documented HTML form element stripping that causes raw HTML to display as text
- Documented Unicode character issues that break `st.markdown` rendering

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
