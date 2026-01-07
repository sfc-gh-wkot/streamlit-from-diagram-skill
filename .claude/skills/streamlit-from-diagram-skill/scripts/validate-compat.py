#!/usr/bin/env python3
"""Validate Streamlit code for cross-environment compatibility."""

import re
import sys
from pathlib import Path


def check_file(filepath: Path) -> tuple[list, list]:
    """Check a single file for compatibility issues."""
    content = filepath.read_text()
    issues, warnings = [], []

    if "column_config" in content:
        issues.append(f"{filepath}: ❌ st.column_config not supported in SiS Container")

    if re.search(r"st\.bar_chart\(", content):
        warnings.append(f"{filepath}: ⚠️ st.bar_chart colors vary, use Altair")

    if re.search(r"st\.line_chart\(", content):
        warnings.append(f"{filepath}: ⚠️ st.line_chart colors vary, use Altair")

    if "import altair" not in content and "alt.Chart" in content:
        issues.append(f"{filepath}: ❌ Using Altair without import")

    return issues, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-compat.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    all_issues, all_warnings = [], []

    if target.is_file():
        i, w = check_file(target)
        all_issues.extend(i)
        all_warnings.extend(w)
    elif target.is_dir():
        for py_file in target.rglob("*.py"):
            if "__pycache__" not in str(py_file):
                i, w = check_file(py_file)
                all_issues.extend(i)
                all_warnings.extend(w)

    print("\n" + "=" * 50)
    print("COMPATIBILITY CHECK")
    print("=" * 50)

    if all_issues:
        print("\n❌ ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")

    if all_warnings:
        print("\n⚠️ WARNINGS:")
        for warning in all_warnings:
            print(f"  {warning}")

    if not all_issues and not all_warnings:
        print("\n✅ All checks passed!")

    sys.exit(1 if all_issues else 0)


if __name__ == "__main__":
    main()
