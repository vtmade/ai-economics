# Quick Start Guide

Get the AI Labor Market Simulation running in 5 minutes.

## Installation

### 1. Clone and Setup

```bash
cd ai-economics
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python run_simulation.py --help
```

## Running Your First Simulation

### Option A: Single Scenario (Fast - 2 minutes)

```bash
python run_simulation.py --scenario baseline --steps 200
```

This runs the baseline (no AI) scenario with default settings.

### Option B: Compare All Scenarios (Complete - 10 minutes)

```bash
python run_simulation.py --compare-all --visualize --report
```

This runs all scenarios, creates visualizations, and generates a comprehensive report.

**Output:**
- `outputs/data/` - CSV files with time series and summary statistics
- `outputs/figures/` - Publication-quality PNG/PDF charts
- `outputs/reports/` - HTML report (open in browser)

## Understanding the Output

### Key Metrics to Watch

1. **Unemployment Rate**: % of workers without jobs
2. **Gini Coefficient**: Income inequality (0=perfect equality, 1=perfect inequality)
3. **Average Wage**: Mean worker wage
4. **AI Adoption Rate**: % of firms using AI
5. **Labor Share**: % of income going to workers vs capital

### Interpreting Results

**Baseline Scenario** (No AI):
- Establishes control group
- Shows natural labor market dynamics

**Low/High Adoption** (AI Impact):
- Compare to baseline to see AI effects
- Higher adoption → larger effects
- Watch for skill-biased impacts (high-skill vs low-skill)

**Retraining** (Policy Intervention):
- Compare to low adoption to see policy effectiveness
- Shows how government programs can mitigate disruption

## Interactive Analysis

For step-by-step simulation walkthrough:

```bash
jupyter notebook notebooks/tutorial.ipynb
```

## Common Use Cases

### Research: Test a Hypothesis

```python
from src.scenarios.runner import ScenarioRunner

runner = ScenarioRunner(random_seed=42)

# Hypothesis: High augmentation with low automation is best
results = runner.run_scenario(
    'custom',
    custom_params={
        'automation_intensity': 0.2,  # Low automation
        'augmentation_intensity': 0.6  # High augmentation
    }
)

print(f"Unemployment: {results['summary']['avg_unemployment_rate']:.2%}")
print(f"Inequality: {results['summary']['final_gini']:.3f}")
```

### Economic Analysis: Explore Market Dynamics

Investigate how:
- Technology exhibits skill-biased characteristics
- Labor market frictions affect adjustment speeds
- Policy interventions influence equilibrium outcomes

Run comparisons, analyze visualizations, interpret results.

### Policy Analysis: Evaluate Interventions

Compare scenarios with different:
- Retraining subsidy rates
- UBI amounts
- Unemployment insurance generosity

Measure cost-effectiveness of each policy.

## Customization

### Modify Parameters

Edit `config.py` to change:
- Number of agents (workers, firms)
- Economic parameters (capital share, depreciation)
- AI characteristics (automation vs augmentation)
- Policy settings (retraining, UI, UBI)

### Extend the Model

Add new features:
- Different AI types
- Regional labor markets
- Occupational switching
- Firm entry/exit

See `docs/research_guide.md` for extension ideas.

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the project root
pwd  # Should show .../ai-economics

# Reinstall dependencies
pip install -r requirements.txt
```

### Memory Issues

Reduce simulation size:
```bash
python run_simulation.py --scenario baseline --workers 50 --firms 10 --steps 100
```

### Slow Performance

- Reduce `--steps` (100 instead of 200)
- Use fewer workers/firms
- Don't run all scenarios at once

## Next Steps

1. **Run Tutorial**: `jupyter notebook notebooks/tutorial.ipynb`
2. **Read Methodology**: `docs/methodology.md` - understand the model
3. **Browse Glossary**: `docs/glossary.md` - learn economic terms
4. **Research Guide**: `docs/research_guide.md` - design experiments
5. **Customize**: Edit `config.py` and run your own scenarios

## Example Workflow

```bash
# 1. Quick exploration
python run_simulation.py --scenario high_adoption --visualize

# 2. Systematic comparison
python run_simulation.py --compare-all --save

# 3. Generate report for presentation
python run_simulation.py --compare-all --visualize --report

# 4. Custom research (in Python)
jupyter notebook notebooks/tutorial.ipynb
# ... design and run custom scenarios ...
```

## Getting Help

- **Documentation**: See `docs/` folder
- **Examples**: See `notebooks/tutorial.ipynb`
- **Issues**: Check README for contact info

## What to Expect

### Baseline Results (Typical)
- Unemployment: ~5%
- Gini: ~0.30
- Wages: $400-$900 depending on skill

### High AI Adoption Results (Typical)
- Initial unemployment spike to ~8-10%
- Eventual stabilization at ~6-7%
- Increased inequality (Gini ~0.38)
- Wage polarization (high-skill up, low-skill down)

### Retraining Effects (Typical)
- Reduces unemployment by 1-2 percentage points vs low adoption
- Modest inequality reduction
- Improved skill distribution

**Note**: Exact values depend on random seed and parameters.

## Congratulations!

You're ready to explore AI's labor market impacts. Happy simulating! 🚀

---

*For detailed information, see the full documentation in the `docs/` folder.*
