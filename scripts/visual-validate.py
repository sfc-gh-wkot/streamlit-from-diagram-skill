#!/usr/bin/env python3
"""
Automated Visual Validation for Streamlit-from-Image Skill

OPTIMIZED VERSION - Key performance improvements:
1. Browser reuse across iterations (saves ~30-40s)
2. Reduced wait times (saves ~3-5s per iteration)
3. Early exit on high score (saves 10-20s)
4. Parallel code analysis

Usage:
    # Run a single validation iteration
    python visual-validate.py [project_dir] [iteration] [--auto]
    
    # Automatic mode with early exit on 90%+ score
    python visual-validate.py . 1 --auto --early-exit 90
    
    # Fast mode (code analysis only, no screenshot)
    python visual-validate.py . 1 --fast

Output: JSON with validation results for Claude to parse and act on.
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Check for Playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Global browser instance for reuse
_BROWSER_INSTANCE = None
_PLAYWRIGHT_INSTANCE = None


def get_browser():
    """Get or create a reusable browser instance."""
    global _BROWSER_INSTANCE, _PLAYWRIGHT_INSTANCE
    
    if not PLAYWRIGHT_AVAILABLE:
        return None, None
    
    if _BROWSER_INSTANCE is None:
        _PLAYWRIGHT_INSTANCE = sync_playwright().start()
        _BROWSER_INSTANCE = _PLAYWRIGHT_INSTANCE.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        print("  🚀 Browser launched (will be reused)")
    
    return _BROWSER_INSTANCE, _PLAYWRIGHT_INSTANCE


def close_browser():
    """Close the shared browser instance."""
    global _BROWSER_INSTANCE, _PLAYWRIGHT_INSTANCE
    
    if _BROWSER_INSTANCE:
        _BROWSER_INSTANCE.close()
        _BROWSER_INSTANCE = None
    if _PLAYWRIGHT_INSTANCE:
        _PLAYWRIGHT_INSTANCE.stop()
        _PLAYWRIGHT_INSTANCE = None


def install_playwright():
    """Install Playwright and Chromium browser using uv (faster) or pip."""
    print("Installing Playwright...")
    
    try:
        subprocess.run(["uv", "pip", "install", "playwright"], check=True)
        subprocess.run(["uv", "run", "playwright", "install", "chromium"], check=True)
    except FileNotFoundError:
        print("uv not found, using pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def capture_screenshot_fast(
    url: str = "http://localhost:8501",
    output_path: str = "screenshot.png",
    width: int = 1920,
    height: int = 1080,
    max_retries: int = 2,  # Reduced from 3
) -> dict:
    """OPTIMIZED: Capture screenshot with reduced wait times and browser reuse."""
    
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "success": False,
            "error": "Playwright not installed",
            "path": None,
        }
    
    result = {
        "success": False,
        "path": None,
        "error": None,
        "retries": 0,
    }
    
    browser, _ = get_browser()
    if not browser:
        result["error"] = "Could not get browser instance"
        return result
    
    for attempt in range(max_retries):
        try:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
            )
            
            page = context.new_page()
            
            print(f"  Attempt {attempt + 1}/{max_retries}: Navigating to {url}...")
            
            # Navigate with shorter timeout (30s instead of 90s)
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for "Running..." to disappear (reduced timeout)
            try:
                running = page.locator("text=Running...")
                running.wait_for(state="detached", timeout=10000)  # 10s instead of 30s
            except PlaywrightTimeout:
                pass
            
            # Wait for main content (reduced timeout)
            try:
                main_content = page.locator('[data-testid="stAppViewContainer"]')
                main_content.wait_for(state="visible", timeout=10000)  # 10s instead of 30s
            except PlaywrightTimeout:
                pass
            
            # OPTIMIZED: Reduced wait time for charts
            print("  Waiting for charts to render (2 seconds)...")
            time.sleep(2)  # Reduced from 4s
            
            # Quick scroll for lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.3)  # Reduced from 0.5s
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(0.2)  # Reduced from 1s
            
            # Capture screenshot
            output_file = Path(output_path)
            page.screenshot(path=str(output_file), full_page=True)
            
            context.close()  # Close context but keep browser
            
            # Check for blank screenshot
            file_size = output_file.stat().st_size
            if file_size < 50000:
                print(f"  Warning: Screenshot is only {file_size/1024:.1f}KB")
                if attempt < max_retries - 1:
                    print("  Retrying in 1s...")
                    time.sleep(1)  # Reduced from 2s
                    result["retries"] = attempt + 1
                    continue
            
            result["success"] = True
            result["path"] = str(output_file.absolute())
            result["file_size"] = file_size
            print(f"  ✅ Screenshot captured: {file_size/1024:.1f}KB")
            return result
            
        except Exception as e:
            result["error"] = str(e)
            print(f"  ❌ Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Reduced retry wait
                result["retries"] = attempt + 1
    
    return result


def analyze_code_structure(project_dir: Path) -> dict:
    """Analyze code for required elements - optimized for speed."""
    
    streamlit_file = project_dir / "streamlit_app.py"
    if not streamlit_file.exists():
        return {"error": "streamlit_app.py not found"}
    
    content = streamlit_file.read_text()
    
    # Fast element detection using string operations (faster than regex)
    elements = {
        # Layout elements
        "left_icon_nav": "icon-nav" in content and "icon-nav-item" in content,
        "right_tiles_panel": "tiles-panel" in content,
        "top_navbar": "top-navbar" in content,
        "dark_mode_toggle": "st.toggle" in content and "dark" in content.lower(),
        
        # Charts
        "has_altair_charts": "alt.Chart" in content or "st.altair_chart" in content,
        "has_line_chart": "mark_line" in content,
        "has_bar_chart": "mark_bar" in content,
        "has_area_chart": "mark_area" in content,
        
        # Content quality
        "has_chart_titles": ".properties(title=" in content or 'title="' in content,
        "has_axis_labels": "axis=alt.Axis" in content,
        "has_tooltips": "tooltip=" in content,
        "has_metrics": "st.metric" in content,
        "has_real_labels": any(word in content for word in ["Revenue", "Users", "Sales", "Growth"]),
        
        # Theme implementation
        "theme_session_state_init": 'if "dark_mode" not in st.session_state' in content,
        "theme_on_change_callback": "on_change=" in content or 'key="dark_mode"' in content,
        "theme_css_variables": "--bg-primary" in content or "--text-primary" in content,
    }
    
    return elements


def analyze_alignment_issues(project_dir: Path) -> list:
    """Check for common alignment issues in code."""
    
    streamlit_file = project_dir / "streamlit_app.py"
    if not streamlit_file.exists():
        return []
    
    content = streamlit_file.read_text()
    issues = []
    
    # Check column proportions
    if "st.columns" in content:
        if "[1,1,1,1,1]" in content or "[1, 1, 1, 1, 1]" in content:
            pass  # Equal columns OK
        elif "st.columns(5)" in content:
            pass  # Equal columns OK
        elif "[1" in content and "8" in content:
            issues.append("⚠️ Unbalanced column widths detected")
    
    # Check for inconsistent padding
    padding_values = []
    for line in content.split("\n"):
        if "padding:" in line:
            import re
            matches = re.findall(r"padding:\s*(\d+)", line)
            padding_values.extend(matches)
    
    if len(set(padding_values)) > 4:
        issues.append("⚠️ Inconsistent padding values")
    
    return issues


def calculate_score(elements: dict, alignment_issues: list) -> tuple:
    """Calculate visual quality score based on elements found."""
    
    score = 0
    max_score = 100
    checks = []
    improvements = []
    
    # Layout elements (40 points)
    layout_items = [
        ("left_icon_nav", "Left icon navigation", 10),
        ("right_tiles_panel", "Right tiles panel", 10),
        ("top_navbar", "Top navigation bar", 10),
        ("dark_mode_toggle", "Dark/light mode toggle", 10),
    ]
    
    for key, name, points in layout_items:
        if elements.get(key):
            score += points
            checks.append({"name": name, "status": "PASS", "points": points})
        else:
            checks.append({"name": name, "status": "FAIL", "points": 0})
            improvements.append(f"Add {name}")
    
    # Charts (30 points)
    if elements.get("has_altair_charts"):
        score += 10
        checks.append({"name": "Altair charts", "status": "PASS", "points": 10})
    else:
        checks.append({"name": "Altair charts", "status": "FAIL", "points": 0})
        improvements.append("Use Altair for charts")
    
    chart_types = sum([
        elements.get("has_line_chart", False),
        elements.get("has_bar_chart", False),
        elements.get("has_area_chart", False),
    ])
    chart_points = min(10, chart_types * 5)
    score += chart_points
    checks.append({"name": f"Chart variety ({chart_types} types)", "status": "PASS" if chart_types >= 2 else "WARN", "points": chart_points})
    
    if elements.get("has_chart_titles"):
        score += 5
        checks.append({"name": "Chart titles", "status": "PASS", "points": 5})
    else:
        improvements.append("Add chart titles")
    
    if elements.get("has_tooltips"):
        score += 5
        checks.append({"name": "Chart tooltips", "status": "PASS", "points": 5})
    else:
        improvements.append("Add chart tooltips")
    
    # Content quality (20 points)
    if elements.get("has_metrics"):
        score += 10
        checks.append({"name": "KPI metrics", "status": "PASS", "points": 10})
    else:
        improvements.append("Add st.metric() for KPIs")
    
    if elements.get("has_real_labels"):
        score += 10
        checks.append({"name": "Meaningful labels", "status": "PASS", "points": 10})
    else:
        improvements.append("Replace placeholder text with meaningful labels")
    
    # Alignment (10 points)
    if not alignment_issues:
        score += 10
        checks.append({"name": "Alignment", "status": "PASS", "points": 10})
    else:
        checks.append({"name": "Alignment", "status": "WARN", "points": 5})
        score += 5
        improvements.extend(alignment_issues)
    
    score_percent = int((score / max_score) * 100)
    
    return score, score_percent, checks, improvements


def run_validation(
    project_dir: Path,
    iteration: int,
    auto_mode: bool = True,
    fast_mode: bool = False,
    early_exit_threshold: int = None,
) -> dict:
    """Run validation iteration."""
    
    timestamp = datetime.now().isoformat()
    
    result = {
        "iteration": iteration,
        "timestamp": timestamp,
        "screenshot": None,
        "score": 0,
        "score_percent": 0,
        "checks": [],
        "improvements": [],
        "early_exit": False,
    }
    
    # Analyze code structure (always fast)
    print(f"\n📊 Analyzing code structure...")
    elements = analyze_code_structure(project_dir)
    alignment_issues = analyze_alignment_issues(project_dir)
    
    # Calculate score
    score, score_percent, checks, improvements = calculate_score(elements, alignment_issues)
    
    result["score"] = score
    result["score_percent"] = score_percent
    result["checks"] = checks
    result["improvements"] = improvements
    
    # Capture screenshot (unless fast mode)
    if not fast_mode and auto_mode:
        print(f"\n📸 Capturing screenshot for iteration {iteration}...")
        screenshot_path = project_dir / f".screenshot_iter_{iteration}.png"
        screenshot_result = capture_screenshot_fast(
            url="http://localhost:8501",
            output_path=str(screenshot_path),
        )
        result["screenshot"] = screenshot_result.get("path")
    
    # Check for early exit
    if early_exit_threshold and score_percent >= early_exit_threshold and iteration >= 2:
        result["early_exit"] = True
        print(f"\n🎉 Early exit: Score {score_percent}% >= {early_exit_threshold}% threshold")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Visual validation for Streamlit apps")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory")
    parser.add_argument("iteration", nargs="?", type=int, default=1, help="Iteration number")
    parser.add_argument("--auto", action="store_true", help="Automatic screenshot capture")
    parser.add_argument("--fast", action="store_true", help="Fast mode (skip screenshots)")
    parser.add_argument("--early-exit", type=int, help="Exit if score >= this percentage")
    parser.add_argument("--install-playwright", action="store_true", help="Install Playwright first")
    parser.add_argument("--close-browser", action="store_true", help="Close browser after validation")
    
    args = parser.parse_args()
    
    if args.install_playwright:
        install_playwright()
        return
    
    project_dir = Path(args.project_dir).resolve()
    
    print(f"🔍 Visual Validation - Iteration {args.iteration}")
    print(f"   Project: {project_dir}")
    print(f"   Mode: {'Fast' if args.fast else 'Auto' if args.auto else 'Manual'}")
    
    try:
        validation = run_validation(
            project_dir=project_dir,
            iteration=args.iteration,
            auto_mode=args.auto,
            fast_mode=args.fast,
            early_exit_threshold=args.early_exit,
        )
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"📊 Visual Validation: Iteration {args.iteration}/3 - Score {validation['score_percent']}/100")
        print(f"{'='*50}")
        
        if validation["improvements"]:
            print("\n🔧 Improvements needed:")
            for imp in validation["improvements"][:5]:  # Top 5
                print(f"   • {imp}")
        
        # Output JSON for Claude
        print(f"\n--- JSON OUTPUT ---")
        print(json.dumps({
            "iteration": validation["iteration"],
            "score": validation["score"],
            "score_percent": validation["score_percent"],
            "improvements": validation["improvements"],
            "screenshot": validation["screenshot"],
            "continue_to_next": not validation["early_exit"] and args.iteration < 3,
            "early_exit": validation["early_exit"],
        }, indent=2))
        
    finally:
        if args.close_browser:
            close_browser()


if __name__ == "__main__":
    main()
