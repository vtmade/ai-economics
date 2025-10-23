# Research Guide

## Using the AI Labor Market Simulation for Research

This guide helps researchers design experiments, test hypotheses, and analyze results using the simulation.

---

## Table of Contents

1. [Research Applications](#research-applications)
2. [Experimental Design](#experimental-design)
3. [Hypothesis Testing](#hypothesis-testing)
4. [Sensitivity Analysis](#sensitivity-analysis)
5. [Extension Ideas](#extension-ideas)
6. [Publication Guidelines](#publication-guidelines)

---

## Research Applications

### 1. Policy Analysis

**Research Questions:**
- What is the optimal design of retraining programs?
- How effective is UBI vs. unemployment insurance?
- Should policies focus on preventing displacement or easing transitions?

**Approach:**
- Compare scenarios with different policy parameters
- Measure outcomes: employment, inequality, welfare
- Conduct cost-benefit analysis of interventions

**Example Experiment:**
```python
# Test different retraining subsidy rates
subsidy_rates = [0.0, 0.25, 0.50, 0.75, 1.0]
results = {}

for rate in subsidy_rates:
    custom_params = {
        'retraining_subsidy_rate': rate
    }
    results[rate] = runner.run_scenario('retraining',
                                       custom_params=custom_params)

# Analyze: unemployment reduction per dollar spent
```

### 2. Technology Characteristics

**Research Questions:**
- Does augmentation vs. automation balance matter?
- How do diffusion speed and adoption rates affect outcomes?
- What if AI capabilities improve over time?

**Approach:**
- Vary AI parameters systematically
- Identify which characteristics drive outcomes
- Test non-linear effects and interactions

**Example Experiment:**
```python
# 2x2 design: automation × augmentation
automation_levels = [0.3, 0.6]
augmentation_levels = [0.2, 0.5]

for auto in automation_levels:
    for aug in augmentation_levels:
        params = {
            'automation_intensity': auto,
            'augmentation_intensity': aug
        }
        # Run and compare
```

### 3. Labor Market Dynamics

**Research Questions:**
- How long do labor market disruptions last?
- What factors speed/slow adjustment?
- Are there hysteresis effects (permanent scarring)?

**Approach:**
- Analyze transition paths, not just steady states
- Track individual workers over time
- Examine skill evolution and mobility

### 4. Inequality and Distribution

**Research Questions:**
- How does AI affect within-group vs. between-group inequality?
- What determines winners and losers?
- Can policy interventions reduce inequality while preserving efficiency?

**Approach:**
- Decompose inequality measures (Gini, percentile ratios)
- Track welfare of different groups
- Analyze consumption vs. income inequality

### 5. Comparative Statics

**Research Questions:**
- How do results vary with market structure?
- Does initial inequality affect outcomes?
- Are there critical thresholds or tipping points?

**Approach:**
- Vary initial conditions systematically
- Change structural parameters
- Map parameter space to outcomes

---

## Experimental Design

### Single-Factor Experiments

**Purpose**: Isolate effect of one parameter

**Design**:
1. Choose baseline configuration
2. Vary one parameter across range
3. Hold all else constant
4. Run multiple replications

**Example**: AI adoption rate sweep
```python
adoption_rates = np.linspace(0, 1, 11)  # 0%, 10%, ..., 100%

for rate in adoption_rates:
    # Run 10 replications
    for seed in range(10):
        runner = ScenarioRunner(random_seed=seed)
        results = runner.run_scenario('custom',
                                     custom_params={'adoption_rate': rate})
        # Store results
```

**Analysis**:
- Plot outcome variables vs. parameter
- Identify linear/non-linear relationships
- Find optimal values or thresholds

### Factorial Experiments

**Purpose**: Test interactions between multiple factors

**Design**: 2^k or 3^k factorial
- 2 levels: low/high
- 3 levels: low/medium/high

**Example**: 2×2×2 design
```python
factors = {
    'adoption_rate': [0.3, 0.8],
    'automation_intensity': [0.3, 0.6],
    'retraining_enabled': [False, True]
}

for adopt in factors['adoption_rate']:
    for auto in factors['automation_intensity']:
        for retrain in factors['retraining_enabled']:
            # Run scenario
            # 2×2×2 = 8 treatment combinations
```

**Analysis**:
- ANOVA to test main effects and interactions
- Identify which factors matter most
- Find complementarities or substitutes

### Monte Carlo Analysis

**Purpose**: Quantify uncertainty and variability

**Design**:
1. Run same scenario many times with different random seeds
2. Estimate distributions of outcomes
3. Calculate confidence intervals

**Example**:
```python
n_replications = 100
unemployment_results = []

for seed in range(n_replications):
    runner = ScenarioRunner(random_seed=seed)
    results = runner.run_scenario('high_adoption')
    unemployment_results.append(results['summary']['avg_unemployment_rate'])

# Analyze distribution
mean = np.mean(unemployment_results)
std = np.std(unemployment_results)
ci = (np.percentile(unemployment_results, 2.5),
      np.percentile(unemployment_results, 97.5))

print(f"Mean: {mean:.3f} (95% CI: {ci[0]:.3f}-{ci[1]:.3f})")
```

### Comparative Scenarios

**Purpose**: Evaluate policy counterfactuals

**Design**:
1. Define baseline (e.g., current policy)
2. Define treatment scenarios (policy alternatives)
3. Use same random seed for fair comparison
4. Calculate differences

**Example**:
```python
seed = 42

baseline = ScenarioRunner(seed).run_scenario('low_adoption')
treatment = ScenarioRunner(seed).run_scenario('retraining')

# Calculate treatment effect
effect = (treatment['summary']['avg_unemployment_rate'] -
          baseline['summary']['avg_unemployment_rate'])

print(f"Retraining reduces unemployment by {-effect*100:.2f} pp")
```

---

## Hypothesis Testing

### Formulating Hypotheses

**Template**:
- **H0** (Null): AI adoption has no effect on unemployment
- **H1** (Alternative): AI adoption increases unemployment

### Testing Approaches

#### 1. Difference-in-Means Test

Compare outcomes between scenarios:

```python
from scipy import stats

# Run baseline many times
baseline_unemployment = [run_once('baseline') for _ in range(30)]

# Run treatment many times
treatment_unemployment = [run_once('high_adoption') for _ in range(30)]

# t-test
t_stat, p_value = stats.ttest_ind(baseline_unemployment,
                                   treatment_unemployment)

print(f"t-statistic: {t_stat:.3f}, p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Reject null hypothesis: AI significantly affects unemployment")
```

#### 2. Regression Analysis

Estimate relationship between parameters and outcomes:

```python
import statsmodels.api as sm

# Run many scenarios with varying parameters
data = []
for _ in range(100):
    params = {
        'adoption_rate': np.random.uniform(0, 1),
        'automation_intensity': np.random.uniform(0, 1),
        'augmentation_intensity': np.random.uniform(0, 1)
    }
    result = runner.run_scenario('custom', custom_params=params)

    data.append({
        'unemployment': result['summary']['avg_unemployment_rate'],
        'adoption': params['adoption_rate'],
        'automation': params['automation_intensity'],
        'augmentation': params['augmentation_intensity']
    })

df = pd.DataFrame(data)

# Regression
X = df[['adoption', 'automation', 'augmentation']]
X = sm.add_constant(X)
y = df['unemployment']

model = sm.OLS(y, X).fit()
print(model.summary())
```

#### 3. Time Series Analysis

Test for structural breaks or trends:

```python
# Extract time series from one run
results = runner.run_scenario('high_adoption', steps=200)
unemployment_series = results['results']['Unemployment Rate']

# Test for trend
from scipy.stats import linregress

time = np.arange(len(unemployment_series))
slope, intercept, r_value, p_value, std_err = linregress(time, unemployment_series)

print(f"Trend: {slope:.6f} per period (p={p_value:.4f})")
```

### Power Analysis

Determine how many replications needed:

```python
from statsmodels.stats.power import ttest_power

# Expected effect size (Cohen's d)
effect_size = 0.5  # Medium effect

# Calculate required sample size for 80% power
n = ttest_power(effect_size, nobs=None, alpha=0.05, power=0.8)
print(f"Need {n:.0f} replications per scenario")
```

---

## Sensitivity Analysis

### One-at-a-Time (OAT) Sensitivity

Vary each parameter individually:

```python
baseline_params = {
    'adoption_rate': 0.5,
    'automation_intensity': 0.4,
    'augmentation_intensity': 0.3,
    'diffusion_speed': 0.05
}

baseline_result = runner.run_scenario('custom', custom_params=baseline_params)
baseline_unemployment = baseline_result['summary']['avg_unemployment_rate']

# Test each parameter
for param, base_value in baseline_params.items():
    # Vary ±20%
    for multiplier in [0.8, 1.2]:
        test_params = baseline_params.copy()
        test_params[param] = base_value * multiplier

        result = runner.run_scenario('custom', custom_params=test_params)
        test_unemployment = result['summary']['avg_unemployment_rate']

        sensitivity = (test_unemployment - baseline_unemployment) / baseline_unemployment
        print(f"{param} {multiplier}: {sensitivity*100:+.2f}% change in unemployment")
```

### Global Sensitivity Analysis

Using Sobol indices or Monte Carlo:

```python
# Latin Hypercube Sampling
from scipy.stats import qmc

# Define parameter ranges
bounds = {
    'adoption_rate': (0.0, 1.0),
    'automation_intensity': (0.0, 0.8),
    'augmentation_intensity': (0.0, 0.8),
    'diffusion_speed': (0.01, 0.15)
}

# Generate sample points
n_samples = 100
sampler = qmc.LatinHypercube(d=len(bounds))
samples = sampler.random(n=n_samples)

# Scale to bounds
param_names = list(bounds.keys())
for i, (param, (low, high)) in enumerate(bounds.items()):
    samples[:, i] = samples[:, i] * (high - low) + low

# Run scenarios
results_data = []
for sample in samples:
    params = dict(zip(param_names, sample))
    result = runner.run_scenario('custom', custom_params=params)

    results_data.append({
        **params,
        'unemployment': result['summary']['avg_unemployment_rate'],
        'gini': result['summary']['final_gini'],
        'gdp': result['summary']['avg_gdp']
    })

df = pd.DataFrame(results_data)

# Analyze correlations
print(df.corr()['unemployment'].sort_values(ascending=False))
```

---

## Extension Ideas

### 1. Heterogeneous AI

**Current**: All AI is the same
**Extension**: Different types of AI (e.g., vision vs. language models)

```python
# Add to model
ai_types = {
    'vision_ai': {
        'automation_susceptibility': {
            'routine_manual': 0.9,
            'routine_cognitive': 0.3
        }
    },
    'language_ai': {
        'automation_susceptibility': {
            'routine_manual': 0.2,
            'routine_cognitive': 0.8
        }
    }
}
```

### 2. Endogenous Innovation

**Current**: AI capabilities are fixed
**Extension**: AI improves through R&D investment

```python
# Add to firm decision
def invest_in_ai_rd(self):
    if self.profits > rd_threshold:
        self.ai_capability += learning_rate * rd_investment
        # Better AI → more automation/augmentation
```

### 3. Occupational Mobility

**Current**: Workers can't change skill categories easily
**Extension**: Workers can switch occupations with costs

```python
# Add to worker
def consider_occupation_switch(self):
    if self.unemployment_duration > threshold:
        # Calculate switching cost
        # Evaluate new occupation prospects
        # Switch if NPV positive
```

### 4. Spatial Labor Markets

**Current**: Single integrated labor market
**Extension**: Multiple regions with migration

```python
# Add regions
class Region:
    def __init__(self, ai_adoption_rate, wage_level):
        self.workers = []
        self.firms = []

# Workers can migrate between regions
```

### 5. Firm Entry and Exit

**Current**: Fixed number of firms
**Extension**: Firms can enter (if profits high) or exit (if losses)

```python
def check_entry_exit(self):
    # Exit if losses exceed threshold
    if self.capital < exit_threshold:
        self.exit_market()

    # Entry if industry profitable
    if avg_profit > entry_cost:
        new_firm = Firm(...)
```

### 6. Network Effects

**Current**: Firms adopt independently
**Extension**: Adoption influenced by peers/suppliers

```python
# Add network
def calculate_adoption_probability(self):
    base_prob = logistic_diffusion(t)

    # Network effect
    peer_adoption = sum(peer.ai_adopted for peer in self.network) / len(self.network)
    network_boost = network_effect_strength * peer_adoption

    return base_prob + network_boost
```

---

## Publication Guidelines

### Reporting Standards

#### Transparency

**Include**:
- All parameter values used
- Random seeds for replication
- Number of replications
- Software versions

**Example**:
> "Simulations were run using the AI Labor Market Simulator v1.0 (Python 3.9, Mesa 2.1). We used default parameters (see Table 1) except where noted. Each scenario was replicated 50 times with seeds 0-49. Code available at [GitHub URL]."

#### Robustness

**Report**:
- Sensitivity to key parameters
- Confidence intervals from Monte Carlo
- Alternative specifications

**Example Table**:
| Parameter | Baseline | -20% | +20% | Outcome Change |
|-----------|----------|------|------|----------------|
| Automation | 0.4 | 0.32 | 0.48 | +1.2pp unemployment |

#### Validation

**Demonstrate**:
- Model matches stylized facts
- Results align with empirical literature
- Mechanisms are plausible

**Example**:
> "The baseline model produces an unemployment-vacancy relationship consistent with the Beveridge curve (Figure 3), matching the negative correlation observed in U.S. data (Blanchard & Diamond, 1989)."

### Visualization Best Practices

#### 1. Show Uncertainty

```python
# Plot with confidence intervals
plt.plot(time, mean_unemployment, label='Mean')
plt.fill_between(time, ci_lower, ci_upper, alpha=0.3, label='95% CI')
```

#### 2. Compare to Baselines

Always include a no-AI baseline for context

#### 3. Use Multiple Metrics

Don't rely on single measure - show employment, wages, inequality, welfare

#### 4. Time Series + Steady State

Report both dynamics and long-run outcomes

### Common Pitfalls

❌ **Single Run**: Run multiple replications
❌ **Cherry-Picking**: Report all outcomes, not just significant ones
❌ **Over-Interpretation**: Remember model limitations
❌ **Assuming Equilibrium**: Highlight transition dynamics
❌ **Ignoring Heterogeneity**: Report distributional effects

### Citation

If using this simulator in research:

```bibtex
@software{ai_labor_market_sim,
  title = {AI Labor Market Economics Simulator},
  author = {[Your Name]},
  year = {2025},
  version = {1.0},
  url = {https://github.com/yourusername/ai-economics}
}
```

---

## Research Workflow Template

### 1. Define Question
- What do you want to know?
- Why does it matter?
- What would answer look like?

### 2. Design Experiment
- What scenarios to compare?
- What parameters to vary?
- How many replications?

### 3. Implement
```python
# Your research code here
```

### 4. Analyze
- Statistical tests
- Visualizations
- Robustness checks

### 5. Interpret
- Economic mechanisms
- Policy implications
- Limitations

### 6. Document
- Methods
- Results
- Code and data

---

## Getting Help

### Resources
- [Methodology Documentation](methodology.md)
- [Economic Glossary](glossary.md)
- [GitHub Issues](https://github.com/yourusername/ai-economics/issues)

### Community
- Share your research findings
- Contribute extensions
- Report bugs or suggest features

---

*This research guide is a living document. Contributions and suggestions welcome!*
