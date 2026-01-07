#!/usr/bin/env python3
"""
Self-Assessment Script for Streamlit-from-Image Skill

Validates generated Streamlit apps and optionally auto-fixes issues
using modern Python tooling (ruff, ty).

Usage:
    python self-assess.py [project_directory]        # Check only
    python self-assess.py [project_directory] --fix  # Check + auto-fix

Output: JSON with pass/fail status and specific issues to fix.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


class SelfAssessment:
    def __init__(self, project_dir: Path, auto_fix: bool = False, localhost_only: bool = False):
        self.project_dir = project_dir
        self.auto_fix = auto_fix
        self.localhost_only = localhost_only  # Skip deployment file checks
        self.results = {
            "passed": True,
            "score": 0,
            "max_score": 0,
            "checks": [],
            "critical_issues": [],
            "warnings": [],
            "suggestions": [],
            "auto_fixed": [],
            "localhost_only": localhost_only,
        }

    def add_check(self, name: str, passed: bool, message: str, critical: bool = False):
        """Add a check result."""
        self.results["max_score"] += 1
        if passed:
            self.results["score"] += 1
            self.results["checks"].append({"name": name, "status": "PASS", "message": message})
        else:
            self.results["checks"].append({"name": name, "status": "FAIL", "message": message})
            if critical:
                self.results["passed"] = False
                self.results["critical_issues"].append(f"{name}: {message}")
            else:
                self.results["warnings"].append(f"{name}: {message}")

    def check_required_files(self):
        """Check all required files exist.
        
        In localhost-only mode, only streamlit_app.py and pyproject.toml are required.
        Deployment files (environment.yml, snowflake.yml, spcs/) are warnings, not critical.
        """
        # Files always required (localhost)
        localhost_required = [
            ("streamlit_app.py", True),
            ("pyproject.toml", True),
        ]
        
        # Files required only for Snowflake deployment
        # In localhost-only mode, these are warnings, not critical
        deployment_files = [
            ("environment.yml", False if self.localhost_only else True),
            ("requirements.txt", False),  # Always optional
            ("snowflake.yml", False if self.localhost_only else True),
            ("spcs/Dockerfile", False if self.localhost_only else True),
            ("spcs/spec.yaml", False if self.localhost_only else True),
            ("spcs/requirements-spcs.txt", False if self.localhost_only else True),
        ]

        # Check localhost files
        for file, critical in localhost_required:
            path = self.project_dir / file
            exists = path.exists()
            self.add_check(
                f"File: {file}",
                exists,
                f"{'Found' if exists else 'MISSING'}: {file}",
                critical=critical,
            )
        
        # Check deployment files (skip if localhost_only and file doesn't exist)
        for file, critical in deployment_files:
            path = self.project_dir / file
            exists = path.exists()
            
            if self.localhost_only and not exists:
                # In localhost-only mode, missing deployment files are just info
                self.results["suggestions"].append(
                    f"Deployment file not yet generated: {file} (will be created on 'deploy to snowflake')"
                )
            else:
                self.add_check(
                    f"File: {file}",
                    exists,
                    f"{'Found' if exists else 'MISSING'}: {file}",
                    critical=critical,
                )

    def check_no_column_config(self):
        """Check that st.column_config is not used (breaks SiS Container)."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()

        # Check for actual usage patterns, not just mentions in comments
        usage_patterns = [
            r"st\.column_config\.",          # st.column_config.NumberColumn etc
            r"column_config\s*=\s*\{",       # column_config={...}
            r"column_config\s*=\s*dict",     # column_config=dict(...)
        ]

        has_column_config_usage = any(
            re.search(pattern, content) for pattern in usage_patterns
        )

        self.add_check(
            "No st.column_config",
            not has_column_config_usage,
            "st.column_config USAGE found - MUST REMOVE (breaks SiS Container)"
            if has_column_config_usage
            else "No st.column_config usage (good)",
            critical=True,
        )

    def check_altair_explicit_colors(self):
        """Check that Altair charts use explicit colors."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()

        # Check for Altair usage
        uses_altair = "import altair" in content or "from altair" in content
        has_charts = "alt.Chart" in content or "mark_bar" in content or "mark_line" in content

        if not has_charts:
            self.add_check(
                "Altair charts",
                True,
                "No Altair charts detected (OK if using other methods)",
            )
            return

        if not uses_altair:
            self.add_check(
                "Altair import",
                False,
                "Using Altair methods without importing altair",
                critical=True,
            )
            return

        # Check for explicit colors
        has_explicit_color = bool(re.search(r'color\s*=\s*["\']#[0-9A-Fa-f]{6}', content))
        has_color_scale = "alt.Scale" in content and "range=" in content

        self.add_check(
            "Explicit chart colors",
            has_explicit_color or has_color_scale,
            "Charts use explicit colors (good)"
            if (has_explicit_color or has_color_scale)
            else "Charts may use default colors - ADD explicit color='#XXXXXX' for consistency",
            critical=False,
        )

    def check_no_simple_charts(self):
        """Check that simple st.bar_chart/line_chart are not used."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()

        simple_charts = []
        if re.search(r"st\.bar_chart\s*\(", content):
            simple_charts.append("st.bar_chart")
        if re.search(r"st\.line_chart\s*\(", content):
            simple_charts.append("st.line_chart")
        if re.search(r"st\.area_chart\s*\(", content):
            simple_charts.append("st.area_chart")
        if re.search(r"st\.scatter_chart\s*\(", content):
            simple_charts.append("st.scatter_chart")

        self.add_check(
            "No simple charts",
            len(simple_charts) == 0,
            f"Found {', '.join(simple_charts)} - REPLACE with Altair for color consistency"
            if simple_charts
            else "No simple st.*_chart() usage (good)",
            critical=False,
        )

    def check_environment_yml_channel(self):
        """Check environment.yml uses snowflake channel."""
        env_file = self.project_dir / "environment.yml"
        if not env_file.exists():
            return

        content = env_file.read_text()
        has_snowflake_channel = "- snowflake" in content or (
            "channels:" in content and 
            "snowflake" in content.split("channels:")[1].split("dependencies:")[0]
            if "channels:" in content and "dependencies:" in content else False
        )

        self.add_check(
            "Snowflake channel in environment.yml",
            has_snowflake_channel,
            "Uses snowflake channel (good)"
            if has_snowflake_channel
            else "MUST use 'snowflake' channel, not 'conda-forge'",
            critical=True,
        )

    def check_dockerfile_platform(self):
        """Check Dockerfile uses correct base image."""
        dockerfile = self.project_dir / "spcs" / "Dockerfile"
        if not dockerfile.exists():
            return

        content = dockerfile.read_text()
        has_python_base = "FROM python:" in content

        self.add_check(
            "Dockerfile base image",
            has_python_base,
            "Uses Python base image"
            if has_python_base
            else "Dockerfile should use python:3.11-slim or python:3.12-slim base",
            critical=False,
        )

        self.results["suggestions"].append(
            "Build with: docker build --platform linux/amd64"
        )

    def check_spec_yaml_public_endpoint(self):
        """Check spec.yaml has public endpoint."""
        spec_file = self.project_dir / "spcs" / "spec.yaml"
        if not spec_file.exists():
            return

        content = spec_file.read_text()
        has_public = "public: true" in content.lower()

        self.add_check(
            "SPCS public endpoint",
            has_public,
            "Endpoint is public (good)" if has_public else "Add 'public: true' to endpoint",
            critical=False,
        )

    def check_syntax_validity(self):
        """Check Python syntax is valid."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        try:
            compile(app_file.read_text(), str(app_file), "exec")
            self.add_check("Python syntax", True, "Syntax is valid", critical=True)
        except SyntaxError as e:
            self.add_check(
                "Python syntax",
                False,
                f"Syntax error at line {e.lineno}: {e.msg}",
                critical=True,
            )

    def check_imports(self):
        """Check required imports are present."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()

        required_imports = [
            ("streamlit", "import streamlit"),
            ("pandas", "import pandas"),
            ("altair", "import altair"),
        ]

        for name, pattern in required_imports:
            has_import = pattern in content or f"from {name}" in content
            self.add_check(
                f"Import: {name}",
                has_import,
                f"{name} imported" if has_import else f"Missing import: {name}",
                critical=(name == "streamlit"),
            )

    def check_line_count(self):
        """Check app has reasonable size."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        lines = len(app_file.read_text().splitlines())

        self.add_check(
            "App size",
            lines >= 50,
            f"App has {lines} lines"
            if lines >= 50
            else f"App only has {lines} lines - may be incomplete",
            critical=False,
        )

    def check_content_quality(self):
        """Check for placeholder content vs real content."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()
        issues = []

        # Check for generic "Predictive Item" placeholder
        if re.search(r'["\']Predictive Item["\']', content, re.IGNORECASE):
            issues.append("Generic 'Predictive Item' text found - use specific names like 'Revenue Forecast'")

        # Check for placeholder lines (literal "───" characters used as placeholders)
        if content.count("───") > 3:
            issues.append("Too many placeholder lines (───) - replace with real content")

        # Check for charts without titles
        chart_count = len(re.findall(r'alt\.Chart\(', content))
        # Look for titled sections - headers like "Monthly Revenue", "**Title**", or "### Title"
        titled_sections = len(re.findall(r'st\.markdown\(["\'].*(?:\*\*|#{1,3}\s).*["\']\)', content))
        
        if chart_count > 0 and titled_sections < chart_count:
            issues.append(f"Found {chart_count} charts but only {titled_sections} title headers - add st.markdown('**Title**') before each chart")

        # Check for st.metric usage (good sign of real content)
        metric_count = len(re.findall(r'st\.metric\(', content))
        
        if metric_count == 0:
            issues.append("No st.metric() found - dashboard should have KPI metrics with real values")

        # Check for realistic-looking numbers ($ amounts, percentages)
        has_dollar_amounts = bool(re.search(r'\$[\d,]+', content))
        has_percentages = bool(re.search(r'\d+\.?\d*%', content))
        has_deltas = bool(re.search(r'[↑↓][+\-]?\d+', content))

        if not (has_dollar_amounts or has_percentages):
            issues.append("No realistic metrics ($ or %) found - add real-looking values")

        # Check for action text patterns (good sign of rich content)
        action_patterns = [
            r'View Details',
            r'Review',
            r'Export',
            r'Optimize',
            r'Investigate',
        ]
        action_count = sum(1 for p in action_patterns if re.search(p, content, re.IGNORECASE))

        if action_count < 2:
            issues.append("Few action buttons found - add interactive elements like 'View Details', 'Export', etc.")

        # Check for right panel content
        right_panel_indicators = [
            r"TODAY'S|VISITORS|PENDING|TASKS",
            r"AI SUGGESTIONS|Enter Prompt",
            r"Recent Activity|Activity feed",
        ]
        right_panel_count = sum(1 for p in right_panel_indicators if re.search(p, content, re.IGNORECASE))

        if right_panel_count < 2:
            issues.append("Right panel content may be missing - add metrics, suggestions, prompt input")

        # Final assessment
        if issues:
            self.add_check(
                "Content quality",
                False,
                "; ".join(issues[:3]),  # Limit to first 3 issues
                critical=False,
            )
        else:
            self.add_check(
                "Content quality",
                True,
                "Content appears to have real data, titles, and rich elements",
                critical=False,
            )

    def check_chart_titles_and_labels(self):
        """Check that charts have proper titles and axis labels."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()

        # Check for axis labels in Altair charts
        has_x_title = bool(re.search(r'alt\.X\([^)]*title\s*=', content))
        has_y_title = bool(re.search(r'alt\.Y\([^)]*title\s*=', content))
        has_tooltips = bool(re.search(r'tooltip\s*=\s*\[', content))

        chart_count = len(re.findall(r'alt\.Chart\(', content))
        
        if chart_count == 0:
            return

        issues = []
        if not has_x_title:
            issues.append("X-axis labels missing - add title= to alt.X()")
        if not has_y_title:
            issues.append("Y-axis labels missing - add title= to alt.Y()")
        if not has_tooltips:
            issues.append("Chart tooltips missing - add tooltip=[...] to encode()")

        if issues:
            self.add_check(
                "Chart titles/labels",
                False,
                "; ".join(issues),
                critical=False,
            )
        else:
            self.add_check(
                "Chart titles/labels",
                True,
                "Charts have axis labels and tooltips",
                critical=False,
            )

    def check_layout_elements(self):
        """Check for mandatory layout elements (icon-nav, tiles-panel)."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()
        issues = []

        # Check for left icon navigation
        has_icon_nav = bool(re.search(r'class="icon-nav"', content)) or \
                       bool(re.search(r'icon-nav-item', content))
        
        if not has_icon_nav:
            issues.append("Left icon navigation (icon-nav) missing - add vertical nav with circles")

        # Check for right tiles panel
        has_tiles_panel = bool(re.search(r'class="tiles-panel"', content)) or \
                          bool(re.search(r'tiles-tab-label', content))
        
        if not has_tiles_panel:
            issues.append("Right tiles panel missing - add collapsible tiles bar")

        # Check for top navbar
        has_navbar = bool(re.search(r'class="top-navbar"', content)) or \
                     bool(re.search(r'nav-logo|nav-company', content))
        
        if not has_navbar:
            issues.append("Top navigation bar missing - add header with logo, search, profile")

        if issues:
            self.add_check(
                "Layout elements",
                False,
                "; ".join(issues[:2]),  # Limit to first 2
                critical=False,
            )
        else:
            self.add_check(
                "Layout elements",
                True,
                "Has icon-nav, tiles-panel, and navbar",
                critical=False,
            )

    def check_interactivity(self):
        """Check for interactive elements."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()
        
        # Count interactive elements
        button_count = len(re.findall(r'st\.button\(', content))
        session_state = "st.session_state" in content
        interactive_charts = ".interactive()" in content
        expanders = len(re.findall(r'st\.expander\(', content))
        tabs = "st.tabs(" in content
        
        interactivity_score = 0
        details = []
        
        if button_count >= 3:
            interactivity_score += 1
            details.append(f"{button_count} buttons")
        if session_state:
            interactivity_score += 1
            details.append("session_state")
        if interactive_charts:
            interactivity_score += 1
            details.append("interactive charts")
        if expanders >= 2:
            interactivity_score += 1
            details.append(f"{expanders} expanders")
        if tabs:
            interactivity_score += 1
            details.append("tabs")

        self.add_check(
            "Interactivity",
            interactivity_score >= 3,
            f"Interactive elements: {', '.join(details)}"
            if interactivity_score >= 3
            else f"Limited interactivity (score: {interactivity_score}/5) - add more buttons, expanders, interactive charts",
            critical=False,
        )

    def check_chart_variety(self):
        """Check for variety of chart types."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()
        
        chart_types = []
        if "mark_bar" in content:
            chart_types.append("bar")
        if "mark_line" in content:
            chart_types.append("line")
        if "mark_area" in content:
            chart_types.append("area")
        if "mark_arc" in content:
            chart_types.append("pie/donut")
        if "mark_point" in content or "mark_circle" in content:
            chart_types.append("scatter")

        self.add_check(
            "Chart variety",
            len(chart_types) >= 3,
            f"Chart types: {', '.join(chart_types)}"
            if chart_types
            else "No Altair charts found",
            critical=False,
        )

    def check_dark_mode_toggle(self):
        """Check for dark/light mode toggle."""
        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        content = app_file.read_text()
        
        has_toggle = bool(re.search(r'st\.toggle\(.*[Dd]ark|[Tt]heme', content))
        has_theme_vars = bool(re.search(r'--bg-primary|dark.*mode|theme.*toggle', content, re.IGNORECASE))

        self.add_check(
            "Dark/Light mode",
            has_toggle or has_theme_vars,
            "Theme toggle present" if (has_toggle or has_theme_vars) else "Consider adding dark/light mode toggle",
            critical=False,
        )

    def check_pyproject_has_ruff(self):
        """Check pyproject.toml has ruff configuration."""
        pyproject = self.project_dir / "pyproject.toml"
        if not pyproject.exists():
            return

        content = pyproject.read_text()
        has_ruff = "[tool.ruff]" in content

        self.add_check(
            "Ruff configuration",
            has_ruff,
            "pyproject.toml has ruff config"
            if has_ruff
            else "Add [tool.ruff] section to pyproject.toml",
            critical=False,
        )

    def check_python_version(self):
        """Check Python version is 3.13+."""
        pyproject = self.project_dir / "pyproject.toml"
        if not pyproject.exists():
            return

        content = pyproject.read_text()
        
        # Check for Python 3.13+
        has_py313 = bool(re.search(r'requires-python\s*=\s*["\']>=3\.1[3-9]', content))
        
        self.add_check(
            "Python 3.13+",
            has_py313,
            "Python >=3.13 specified"
            if has_py313
            else "Update requires-python to >=3.13",
            critical=False,
        )

    def check_streamlit_version(self):
        """Check Streamlit version is 1.51+."""
        files_to_check = [
            ("pyproject.toml", r'streamlit[><=]*1\.5[1-9]|streamlit>=1\.5[1-9]'),
            ("requirements.txt", r'streamlit[><=]*1\.5[1-9]|streamlit>=1\.5[1-9]'),
            ("spcs/requirements-spcs.txt", r'streamlit[><=]*1\.5[1-9]|streamlit>=1\.5[1-9]'),
        ]

        for file, pattern in files_to_check:
            path = self.project_dir / file
            if not path.exists():
                continue

            content = path.read_text()
            has_correct_version = bool(re.search(pattern, content, re.IGNORECASE))

            self.add_check(
                f"Streamlit 1.51+ in {file}",
                has_correct_version,
                f"Streamlit >=1.51 in {file}"
                if has_correct_version
                else f"Update Streamlit to >=1.51 in {file}",
                critical=False,
            )

    def run_ruff_check(self):
        """Run ruff linter and optionally fix issues."""
        if not shutil.which("ruff"):
            self.results["suggestions"].append("Install ruff: uv tool install ruff")
            return

        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        # Run ruff check
        result = subprocess.run(
            ["ruff", "check", str(app_file), "--output-format=json"],
            capture_output=True,
            text=True,
            cwd=self.project_dir,
        )

        try:
            issues = json.loads(result.stdout) if result.stdout else []
        except json.JSONDecodeError:
            issues = []

        if issues:
            issue_count = len(issues)
            if self.auto_fix:
                # Auto-fix with ruff
                fix_result = subprocess.run(
                    ["ruff", "check", str(app_file), "--fix"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_dir,
                )
                # Format with ruff
                subprocess.run(
                    ["ruff", "format", str(app_file)],
                    capture_output=True,
                    text=True,
                    cwd=self.project_dir,
                )
                self.results["auto_fixed"].append(f"ruff: Fixed {issue_count} issues")
                self.add_check(
                    "Ruff linting",
                    True,
                    f"Auto-fixed {issue_count} linting issues",
                    critical=False,
                )
            else:
                self.add_check(
                    "Ruff linting",
                    False,
                    f"Found {issue_count} linting issues - run with --fix to auto-correct",
                    critical=False,
                )
        else:
            self.add_check("Ruff linting", True, "No linting issues", critical=False)

    def run_ruff_format_check(self):
        """Check ruff formatting."""
        if not shutil.which("ruff"):
            return

        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        result = subprocess.run(
            ["ruff", "format", "--check", str(app_file)],
            capture_output=True,
            text=True,
            cwd=self.project_dir,
        )

        needs_formatting = result.returncode != 0

        if needs_formatting and self.auto_fix:
            subprocess.run(
                ["ruff", "format", str(app_file)],
                capture_output=True,
                text=True,
                cwd=self.project_dir,
            )
            self.results["auto_fixed"].append("ruff format: Reformatted code")
            self.add_check("Ruff formatting", True, "Auto-formatted code", critical=False)
        elif needs_formatting:
            self.add_check(
                "Ruff formatting",
                False,
                "Code needs formatting - run with --fix or 'ruff format .'",
                critical=False,
            )
        else:
            self.add_check("Ruff formatting", True, "Code is properly formatted", critical=False)

    def run_ty_check(self):
        """Run ty type checker (if available)."""
        if not shutil.which("ty"):
            self.results["suggestions"].append("Install ty: uv tool install ty")
            return

        app_file = self.project_dir / "streamlit_app.py"
        if not app_file.exists():
            return

        result = subprocess.run(
            ["ty", "check", str(app_file)],
            capture_output=True,
            text=True,
            cwd=self.project_dir,
        )

        has_errors = result.returncode != 0 and "error" in result.stdout.lower()

        if has_errors:
            error_lines = [l for l in result.stdout.splitlines() if "error" in l.lower()][:3]
            self.add_check(
                "Type checking (ty)",
                False,
                f"Type errors found: {'; '.join(error_lines)}",
                critical=False,
            )
        else:
            self.add_check("Type checking (ty)", True, "No type errors", critical=False)

    def run_all_checks(self):
        """Run all validation checks."""
        # File structure checks
        self.check_required_files()

        # Code quality checks
        self.check_no_column_config()
        self.check_altair_explicit_colors()
        self.check_no_simple_charts()
        self.check_syntax_validity()
        self.check_imports()
        self.check_line_count()

        # Content quality checks (catches placeholder issues)
        self.check_content_quality()
        self.check_chart_titles_and_labels()

        # Layout and interactivity checks (catches missing nav elements)
        self.check_layout_elements()
        self.check_interactivity()
        self.check_chart_variety()
        self.check_dark_mode_toggle()

        # Config checks
        self.check_environment_yml_channel()
        self.check_dockerfile_platform()
        self.check_spec_yaml_public_endpoint()
        self.check_pyproject_has_ruff()
        self.check_python_version()
        self.check_streamlit_version()

        # Tooling checks (with auto-fix if enabled)
        self.run_ruff_check()
        self.run_ruff_format_check()
        self.run_ty_check()

        # Calculate final score
        self.results["score_percent"] = round(
            100 * self.results["score"] / self.results["max_score"]
        ) if self.results["max_score"] > 0 else 0

        return self.results


def main():
    # Parse arguments
    auto_fix = "--fix" in sys.argv
    localhost_only = "--localhost-only" in sys.argv or "--localhost" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    project_dir = Path(args[0]) if args else Path.cwd()

    if not project_dir.exists():
        print(json.dumps({"error": f"Directory not found: {project_dir}"}))
        sys.exit(1)

    # Auto-detect localhost-only mode if only streamlit_app.py and pyproject.toml exist
    if not localhost_only:
        has_app = (project_dir / "streamlit_app.py").exists()
        has_pyproject = (project_dir / "pyproject.toml").exists()
        missing_deploy = not (project_dir / "environment.yml").exists()
        if has_app and has_pyproject and missing_deploy:
            localhost_only = True
            print("ℹ️  Auto-detected localhost-only mode (no deployment files yet)", file=sys.stderr)

    assessment = SelfAssessment(project_dir, auto_fix=auto_fix, localhost_only=localhost_only)
    results = assessment.run_all_checks()

    # Output JSON for Claude to parse
    print(json.dumps(results, indent=2))

    # Human-readable summary to stderr
    print("\n" + "=" * 60, file=sys.stderr)
    print(f"SELF-ASSESSMENT: {results['score']}/{results['max_score']} ({results['score_percent']}%)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    if results["auto_fixed"]:
        print("\n🔧 AUTO-FIXED:", file=sys.stderr)
        for fix in results["auto_fixed"]:
            print(f"   • {fix}", file=sys.stderr)

    if results["critical_issues"]:
        print("\n❌ CRITICAL ISSUES (must fix):", file=sys.stderr)
        for issue in results["critical_issues"]:
            print(f"   • {issue}", file=sys.stderr)

    if results["warnings"]:
        print("\n⚠️  WARNINGS:", file=sys.stderr)
        for warning in results["warnings"]:
            print(f"   • {warning}", file=sys.stderr)

    if results["suggestions"]:
        print("\n💡 SUGGESTIONS:", file=sys.stderr)
        for suggestion in results["suggestions"]:
            print(f"   • {suggestion}", file=sys.stderr)

    if results["passed"]:
        print("\n✅ RESULT: PASSED - Ready for deployment", file=sys.stderr)
    else:
        print("\n❌ RESULT: FAILED - Fix critical issues above", file=sys.stderr)

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
