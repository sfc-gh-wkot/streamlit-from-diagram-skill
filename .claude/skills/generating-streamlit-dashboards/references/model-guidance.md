# Model-Specific Guidance

Guidance for different Claude model variants when using this skill.

## Model Compatibility Table

| Model | Guidance | File Loading Strategy |
|-------|----------|----------------------|
| **Claude Haiku** | May need chart patterns copied into context | Load `chart-patterns.md` and `component-mapping.md` proactively; grep patterns may not be followed reliably |
| **Claude Sonnet** | Works well with reference file navigation | Use grep patterns to find specific sections; load files on-demand |
| **Claude Opus** | Can infer patterns from minimal examples | Rely on SKILL.md alone when possible; avoid loading verbose references unless needed |

## Loading Priority by Phase

Different phases benefit from different reference files:

### Phase 1: Localhost Generation
- **Primary:** `workflow-details.md`, `component-mapping.md`
- **Secondary:** `layout-patterns.md`, `css-patterns.md`
- **On-demand:** `chart-patterns.md` (for specific chart types)

### Phase 2: Visual Validation
- **Primary:** `chart-patterns.md` (for improvements)
- **Secondary:** `troubleshooting.md`
- **On-demand:** `interactivity-patterns.md`

### Phase 3: Snowflake Deployment
- **Primary:** `snowflake-deployment.md`, `security-rules.md`
- **Secondary:** `version-matrix.md`
- **On-demand:** `troubleshooting.md`

## Haiku-Specific Recommendations

Claude Haiku may struggle with:
- Following grep patterns to navigate large files
- Inferring content from minimal examples
- Complex multi-step reasoning

**Mitigation strategies:**
1. Load full reference files rather than relying on grep
2. Provide explicit examples in context
3. Break complex tasks into smaller steps

```python
# Example: Load chart patterns for Haiku
# Instead of: grep -n "mark_bar" references/chart-patterns.md
# Do: Read the full chart-patterns.md file into context
```

## Sonnet-Specific Recommendations

Claude Sonnet balances capability with efficiency:
- Follows grep patterns reliably
- Can navigate between reference files
- Handles multi-step workflows well

**Optimization strategies:**
1. Use grep to find specific patterns
2. Load files on-demand based on task requirements
3. Trust the model to follow references

## Opus-Specific Recommendations

Claude Opus can:
- Infer patterns from SKILL.md alone
- Generate high-quality output with minimal examples
- Handle edge cases without explicit documentation

**Efficiency strategies:**
1. Start with SKILL.md only
2. Load references only when encountering specific issues
3. Allow creative interpretation of wireframes

## Context Window Management

For all models, keep context focused:

| Model | Approx. Context Budget | Strategy |
|-------|------------------------|----------|
| Haiku | 200K tokens | Load essential refs upfront, avoid back-and-forth |
| Sonnet | 200K tokens | Load on-demand, use grep for specific sections |
| Opus | 200K tokens | Minimal loading, trust inference |

## Common Patterns by Model

### Haiku: Explicit Chart Example
```python
# Load full example for Haiku
# From chart-patterns.md:
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:N", title="Month"),
    y=alt.Y("value:Q", title="Revenue ($)"),
    tooltip=["month", alt.Tooltip("value:Q", format="$,.0f")]
)
```

### Sonnet: Reference Navigation
```bash
# Use grep to find patterns
grep -n "mark_bar\|mark_line" references/chart-patterns.md
# Then read specific line ranges
```

### Opus: Minimal Context
```python
# Opus can infer from SKILL.md Must Use section
# Generate charts with explicit colors and titles
```
