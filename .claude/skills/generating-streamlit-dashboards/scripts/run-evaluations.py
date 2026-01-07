#!/usr/bin/env python3
"""
Run skill evaluations and report pass/fail.

Usage:
    python scripts/run-evaluations.py                    # Run all evaluations
    python scripts/run-evaluations.py basic-localhost    # Run specific evaluation
    python scripts/run-evaluations.py --list             # List available evaluations
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def get_evaluations_dir() -> Path:
    """Get the evaluations directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "evaluations"


def list_evaluations() -> list[Path]:
    """List all evaluation JSON files."""
    evals_dir = get_evaluations_dir()
    return sorted(evals_dir.glob("*.json"))


def load_evaluation(eval_path: Path) -> dict[str, Any]:
    """Load an evaluation file."""
    with open(eval_path) as f:
        return json.load(f)


def check_preconditions(scenario: dict[str, Any]) -> tuple[bool, str]:
    """Check if preconditions for a scenario are met."""
    precondition = scenario.get("precondition", "")
    
    if "Localhost app already running" in precondition:
        # Check if Streamlit is running on 8501
        try:
            result = subprocess.run(
                ["curl", "-sf", "http://localhost:8501/_stcore/health"],
                capture_output=True,
                timeout=5
            )
            if result.returncode != 0:
                return False, "Localhost app not running at port 8501"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, "Could not check localhost health"
    
    return True, ""


def evaluate_scenario(scenario: dict[str, Any], grading: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate a single scenario.
    
    Returns a result dict with:
    - passed: bool
    - score: float (0-1)
    - missing_behaviors: list[str]
    - critical_missing: list[str]
    """
    result = {
        "id": scenario["id"],
        "query": scenario["query"],
        "passed": False,
        "score": 0.0,
        "missing_behaviors": [],
        "critical_missing": [],
        "notes": ""
    }
    
    # Check preconditions
    precond_ok, precond_msg = check_preconditions(scenario)
    if not precond_ok:
        result["notes"] = f"Precondition failed: {precond_msg}"
        return result
    
    # In a real implementation, this would:
    # 1. Send the query to Claude with the skill loaded
    # 2. Observe the actions taken
    # 3. Check each expected_behavior against what happened
    # 4. Calculate score based on grading rubric
    
    expected = scenario.get("expected_behavior", [])
    critical = grading.get("critical_behaviors", [])
    
    # Placeholder: Mark as needing manual evaluation
    result["notes"] = "Manual evaluation required - run scenario and check behaviors"
    result["expected_count"] = len(expected)
    result["critical_count"] = len(critical)
    
    return result


def run_evaluation(eval_path: Path) -> dict[str, Any]:
    """Run a single evaluation file."""
    eval_data = load_evaluation(eval_path)
    
    results = {
        "name": eval_data["name"],
        "description": eval_data["description"],
        "scenarios": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "manual_review": 0
        }
    }
    
    grading = eval_data.get("grading", {})
    
    for scenario in eval_data.get("scenarios", []):
        result = evaluate_scenario(scenario, grading)
        results["scenarios"].append(result)
        results["summary"]["total"] += 1
        
        if result["passed"]:
            results["summary"]["passed"] += 1
        elif result["notes"].startswith("Manual"):
            results["summary"]["manual_review"] += 1
        else:
            results["summary"]["failed"] += 1
    
    return results


def print_results(results: dict[str, Any]) -> None:
    """Print evaluation results."""
    print(f"\n{'='*60}")
    print(f"Evaluation: {results['name']}")
    print(f"Description: {results['description']}")
    print(f"{'='*60}")
    
    for scenario in results["scenarios"]:
        status = "✅ PASS" if scenario["passed"] else "⏳ MANUAL" if "Manual" in scenario.get("notes", "") else "❌ FAIL"
        print(f"\n{status} Scenario: {scenario['id']}")
        print(f"   Query: {scenario['query']}")
        if scenario.get("notes"):
            print(f"   Notes: {scenario['notes']}")
        if scenario.get("expected_count"):
            print(f"   Expected behaviors: {scenario['expected_count']}")
        if scenario.get("critical_count"):
            print(f"   Critical behaviors: {scenario['critical_count']}")
    
    summary = results["summary"]
    print(f"\n{'─'*60}")
    print(f"Summary: {summary['passed']}/{summary['total']} passed, "
          f"{summary['failed']} failed, {summary['manual_review']} need manual review")


def main():
    parser = argparse.ArgumentParser(description="Run skill evaluations")
    parser.add_argument("evaluation", nargs="?", help="Specific evaluation to run (without .json)")
    parser.add_argument("--list", action="store_true", help="List available evaluations")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()
    
    evals_dir = get_evaluations_dir()
    
    if not evals_dir.exists():
        print(f"Error: Evaluations directory not found: {evals_dir}", file=sys.stderr)
        sys.exit(1)
    
    if args.list:
        print("Available evaluations:")
        for eval_path in list_evaluations():
            if eval_path.name != "README.md":
                eval_data = load_evaluation(eval_path)
                print(f"  - {eval_path.stem}: {eval_data.get('description', 'No description')}")
        return
    
    # Determine which evaluations to run
    if args.evaluation:
        eval_path = evals_dir / f"{args.evaluation}.json"
        if not eval_path.exists():
            print(f"Error: Evaluation not found: {eval_path}", file=sys.stderr)
            sys.exit(1)
        eval_files = [eval_path]
    else:
        eval_files = [p for p in list_evaluations() if p.suffix == ".json"]
    
    all_results = []
    for eval_path in eval_files:
        results = run_evaluation(eval_path)
        all_results.append(results)
        
        if args.json:
            continue
        print_results(results)
    
    if args.json:
        print(json.dumps(all_results, indent=2))
    
    # Exit with error if any failed
    total_failed = sum(r["summary"]["failed"] for r in all_results)
    if total_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
