# Skill Evaluations

Test scenarios for validating skill effectiveness across models.

## Running Evaluations

Each evaluation scenario is a JSON file with:
- `query`: User request to test
- `files`: Required input files (use `assets/example-wireframe.png`)
- `precondition`: State required before test (optional)
- `expected_behavior`: List of expected outcomes
- `grading`: Scoring rubric with thresholds

## Grading Structure

Each evaluation includes a `grading` object:

```json
{
  "grading": {
    "pass_threshold": 1.0,
    "partial_pass_threshold": 0.7,
    "critical_behaviors": ["behavior that MUST pass"],
    "scoring": {
      "pass": "All expected behaviors observed",
      "partial": ">=70% behaviors observed, all critical behaviors pass",
      "fail": "Any critical behavior missing OR <70% behaviors observed"
    }
  }
}
```

## Evaluation Files

| File | Tests | Critical Behaviors |
|------|-------|-------------------|
| `basic-localhost.json` | Phase 1 localhost generation | .gitignore first, STOP after localhost |
| `visual-validation.json` | Phase 2 validation loop | JSON parsing, iteration control |
| `snowflake-deploy.json` | Phase 3 deployment | Token security, trigger detection |
| `edge-cases.json` | Edge detection, complex layouts | No placeholder content |

## Scoring Criteria

- **Pass**: All expected behaviors observed (100%)
- **Partial**: ≥70% behaviors observed AND all critical behaviors pass
- **Fail**: Any critical behavior missing OR <70% behaviors observed

## Model Testing Notes

Test each evaluation with all target models:
- **Claude Haiku**: May need more explicit guidance
- **Claude Sonnet**: Balanced performance
- **Claude Opus**: Best reasoning, may over-engineer
