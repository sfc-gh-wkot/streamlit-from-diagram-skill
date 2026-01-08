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

---

## Example Results

### Pass Result (basic-localhost.json)

```
Evaluation: basic-localhost
Model: claude-sonnet-4-20250514
Result: PASS (100%)

Behaviors observed:
✅ .gitignore created first (before any other files)
✅ streamlit_app.py generated with rich content
✅ No placeholder text ("Predictive Item") in output
✅ App running at localhost:8501
✅ STOP after localhost URL output (waited for user)
✅ git commit completed

Score: 6/6 behaviors (100%)
Critical behaviors: 2/2 passed
```

### Partial Pass Example

```
Evaluation: edge-cases
Model: claude-3-5-haiku-20241022
Result: PARTIAL (75%)

Behaviors observed:
✅ .gitignore created first
✅ App running at localhost:8501
✅ Left icon navigation detected
❌ Placeholder text "Predictive Item" found in sidebar
✅ Charts have axis labels
❌ Missing right tiles panel

Score: 4/6 behaviors (67%)
Critical behaviors: 1/1 passed (no placeholder = CRITICAL)

Note: Failed due to placeholder text (critical behavior)
Final result: FAIL (critical behavior missing)
```

### Fail Result Example

```
Evaluation: snowflake-deploy
Model: claude-3-5-haiku-20241022
Result: FAIL

Behaviors observed:
✅ Localhost verified before deployment
❌ PAT token echoed to console (SECURITY VIOLATION)
✅ Deployment files generated
❌ Deployed without explicit user request

Score: 2/4 behaviors (50%)
Critical behaviors: 0/2 passed

Failed critical behaviors:
- Token security: PAT token was displayed in output
- Trigger detection: Deployed without "deploy to snowflake" phrase
```

---

## Model Testing Notes

Test each evaluation with all target models:

| Model | Typical Performance | Notes |
|-------|---------------------|-------|
| **Claude Haiku** | May need more explicit guidance | Load more reference files upfront |
| **Claude Sonnet** | Balanced performance | Default model for testing |
| **Claude Opus** | Best reasoning, may over-engineer | May add unrequested features |

### Running Evaluations

```bash
# Run all evaluations
python scripts/run-evaluations.py

# Run specific evaluation
python scripts/run-evaluations.py --eval basic-localhost

# Run with specific model
python scripts/run-evaluations.py --model claude-sonnet-4-20250514
```

### Manual Testing Checklist

For each evaluation file:

1. Start fresh Claude conversation
2. Load the skill
3. Provide the query from the evaluation file
4. Observe Claude's behavior
5. Compare against expected behaviors
6. Score and record results

---

## Creating New Evaluations

New evaluation files follow this structure:

```json
{
  "name": "evaluation-name",
  "description": "What this evaluation tests",
  "query": "User request to test",
  "files": ["assets/example-wireframe.png"],
  "precondition": "State required before test (optional)",
  "expected_behavior": [
    "First expected behavior",
    "Second expected behavior"
  ],
  "grading": {
    "pass_threshold": 1.0,
    "partial_pass_threshold": 0.7,
    "critical_behaviors": ["Behavior that MUST pass"],
    "scoring": {
      "pass": "All expected behaviors observed",
      "partial": ">=70% behaviors, all critical pass",
      "fail": "Any critical missing OR <70% behaviors"
    }
  }
}
```
