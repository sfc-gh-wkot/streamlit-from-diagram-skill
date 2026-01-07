#!/usr/bin/env python3
"""
Automated Screenshot Capture for Streamlit Visual Validation

OPTIMIZED VERSION - Key performance improvements:
1. Reduced wait times (4s → 2s for charts)
2. Faster retry logic (5s → 1s)
3. Shorter timeouts (90s → 30s)

Usage:
    python auto-screenshot.py [url] [output_path]
    python auto-screenshot.py http://localhost:8501 screenshot_iter_1.png

    # With reduced wait time (fast mode)
    python auto-screenshot.py http://localhost:8501 screenshot.png --wait 1
"""

import argparse
import base64
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: Playwright not installed. Run:")
    print("  uv pip install playwright")
    print("  uv run playwright install chromium")
    sys.exit(1)


def wait_for_streamlit_load(page, timeout: int = 15000, fast: bool = False):
    """Wait for Streamlit app to fully load.
    
    OPTIMIZED waiting strategy:
    1. Wait for "Running..." indicator to disappear (10s max)
    2. Wait for main content container (10s max)
    3. Reduced chart render wait (2s instead of 4s)
    4. Quick scroll for lazy loading (0.5s instead of 1.5s)
    """
    # Wait for "Running..." to disappear
    try:
        running_indicator = page.locator("text=Running...")
        running_indicator.wait_for(state="detached", timeout=timeout)
    except PlaywrightTimeout:
        pass
    
    # Wait for main content
    try:
        main_content = page.locator('[data-testid="stAppViewContainer"]')
        main_content.wait_for(state="visible", timeout=timeout)
    except PlaywrightTimeout:
        try:
            main_content = page.locator('.main')
            main_content.wait_for(state="visible", timeout=5000)
        except PlaywrightTimeout:
            pass
    
    # Chart render wait (reduced)
    wait_time = 1 if fast else 2
    print(f"  Waiting for charts ({wait_time}s)...")
    time.sleep(wait_time)
    
    # Quick scroll for lazy loading
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.2)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.3)


def capture_screenshot(
    url: str = "http://localhost:8501",
    output_path: str = "screenshot.png",
    width: int = 1920,
    height: int = 1080,
    full_page: bool = True,
    wait_time: int = 2,  # Reduced from 3
    max_retries: int = 2,  # Reduced from 3
    fast: bool = False,
) -> dict:
    """Capture a screenshot with optimized timing."""
    
    result = {
        "success": False,
        "path": None,
        "base64": None,
        "error": None,
        "url": url,
        "retries": 0,
        "file_size": 0,
    }
    
    for attempt in range(max_retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    device_scale_factor=1,
                )
                
                page = context.new_page()
                
                print(f"Attempt {attempt + 1}/{max_retries}: Navigating to {url}...")
                page.goto(url, wait_until="networkidle", timeout=30000)  # Reduced from 90000
                
                wait_for_streamlit_load(page, fast=fast)
                
                if wait_time > 0 and not fast:
                    print(f"  Additional wait: {wait_time}s...")
                    time.sleep(wait_time)
                
                output_file = Path(output_path)
                print(f"  Capturing screenshot...")
                
                screenshot_bytes = page.screenshot(
                    path=str(output_file),
                    full_page=full_page,
                )
                
                browser.close()
                
                file_size = output_file.stat().st_size
                result["file_size"] = file_size
                
                if file_size < 50000:
                    print(f"  ⚠️ Screenshot is only {file_size/1024:.1f}KB - may be blank")
                    if attempt < max_retries - 1:
                        print("  Retrying in 1s...")
                        time.sleep(1)  # Reduced from 5s
                        result["retries"] = attempt + 1
                        continue
                
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
                
                result["success"] = True
                result["path"] = str(output_file.absolute())
                result["base64"] = screenshot_base64[:100] + "..."
                
                print(f"✅ Screenshot saved: {file_size/1024:.1f}KB → {result['path']}")
                return result
                
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print("  Retrying in 1s...")
                time.sleep(1)  # Reduced from variable waits
                result["retries"] = attempt + 1
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Capture Streamlit screenshot")
    parser.add_argument("url", nargs="?", default="http://localhost:8501", help="Streamlit URL")
    parser.add_argument("output", nargs="?", default="screenshot.png", help="Output path")
    parser.add_argument("--width", type=int, default=1920, help="Viewport width")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height")
    parser.add_argument("--wait", type=int, default=2, help="Additional wait time (seconds)")
    parser.add_argument("--fast", action="store_true", help="Fast mode (minimal waits)")
    parser.add_argument("--no-full-page", action="store_true", help="Capture viewport only")
    
    args = parser.parse_args()
    
    print(f"📸 Streamlit Screenshot Capture")
    print(f"   URL: {args.url}")
    print(f"   Output: {args.output}")
    print(f"   Mode: {'Fast' if args.fast else 'Normal'}")
    
    result = capture_screenshot(
        url=args.url,
        output_path=args.output,
        width=args.width,
        height=args.height,
        full_page=not args.no_full_page,
        wait_time=args.wait,
        fast=args.fast,
    )
    
    if not result["success"]:
        print(f"\n❌ Failed: {result['error']}")
        sys.exit(1)
    
    print(f"\n✅ Success!")
    return result


if __name__ == "__main__":
    main()
