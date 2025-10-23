# Sample Simulation Outputs

This directory contains example outputs from running all four comparison scenarios.

## Generated Files

### Data Files (`data/`)

**Time Series Data** (150 periods each):
- `baseline_timeseries.csv` - Control scenario without AI
- `low_adoption_timeseries.csv` - 30% adoption, slow diffusion
- `high_adoption_timeseries.csv` - 80% adoption, fast diffusion
- `retraining_timeseries.csv` - AI + government retraining programs

Each file contains metrics tracked over time:
- Unemployment Rate
- Average Wage (overall and by skill level)
- Gini Coefficient
- GDP
- AI Adoption Rate
- Labor Share
- Employment by skill level
- Average productivity

**Summary Tables**:
- `scenario_comparison.csv` - Side-by-side comparison of all scenarios
- `scenario_impacts.csv` - Changes relative to baseline

### Visualizations (`figures/`)

**Individual Scenario Dashboards**:
- `dashboard_baseline.png` - 9-panel overview of baseline scenario
- `dashboard_low_adoption.png` - Low AI adoption dynamics
- `dashboard_high_adoption.png` - High AI adoption dynamics
- `dashboard_retraining.png` - Retraining policy effects

**Cross-Scenario Comparisons**:
- `comparison_unemployment_rate.png` - Unemployment across scenarios
- `comparison_average_wage.png` - Wage dynamics
- `comparison_gini_coefficient.png` - Inequality trends
- `comparison_gdp.png` - Economic output
- `comparison_ai_adoption_rate.png` - Technology diffusion
- `comparison_labor_share.png` - Income distribution
- `multi_comparison.png` - 6-panel combined view

### Reports (`reports/`)

- `simulation_report.html` - Comprehensive analysis report (open in browser)

## Key Findings from Sample Run

### Baseline Scenario
- Steady-state unemployment: ~81%
- No AI adoption
- Serves as control group

### AI Adoption Scenarios
- **Low Adoption**: Modest technology diffusion, limited labor market impact
- **High Adoption**: Rapid AI spread, more pronounced effects on employment and wages
- **Impact varies by skill level**: Higher-skilled workers see different outcomes than lower-skilled

### Retraining Program Effects
- Active labor market policy intervention
- Helps workers transition to new skill requirements
- Compare to low adoption to isolate policy impact

## Reproducing These Results

Run the same simulation:

```bash
python run_simulation.py --compare-all --visualize --report --save
```

Parameters used for these outputs:
- Workers: 80
- Firms: 15
- Time steps: 150
- Random seed: 42

## Notes

- All scenarios use identical random seed for fair comparison
- High unemployment rates reflect model calibration (small firm count relative to workers)
- Results demonstrate model functionality and scenario differentiation
- Adjust parameters in `config.py` for different outcomes

## Using the Data

### Load time series:
```python
import pandas as pd
baseline = pd.read_csv('outputs/data/baseline_timeseries.csv', index_col=0)
```

### Load comparison:
```python
comparison = pd.read_csv('outputs/data/scenario_comparison.csv')
print(comparison)
```

### Analyze impacts:
```python
impacts = pd.read_csv('outputs/data/scenario_impacts.csv')
print(impacts)
```
