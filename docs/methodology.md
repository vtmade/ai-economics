# Methodology Guide

## AI Labor Market Simulation: Technical Documentation

This document provides a comprehensive explanation of the model's theoretical foundation, implementation details, and calibration methodology.

---

## Table of Contents

1. [Overview](#overview)
2. [Theoretical Framework](#theoretical-framework)
3. [Agent Specifications](#agent-specifications)
4. [Market Mechanisms](#market-mechanisms)
5. [AI Impact Modeling](#ai-impact-modeling)
6. [Calibration](#calibration)
7. [Validation](#validation)
8. [Limitations](#limitations)

---

## Overview

This simulation uses an **agent-based computational economics** (ACE) approach to model labor markets under AI adoption. The model captures:

- **Heterogeneity**: Agents differ in skills, capital, and preferences
- **Bounded Rationality**: Agents use simple heuristics, not perfect optimization
- **Endogenous Dynamics**: Outcomes emerge from agent interactions
- **Out-of-Equilibrium Behavior**: No assumption of market clearing or steady state

### Model Philosophy

We follow the ACE tradition (Tesfatsion, 2006) where:
- No representative agent assumption
- Explicit modeling of search, matching, and adjustment frictions
- Focus on transition dynamics, not just steady states
- Computational approach allows for complexity not tractable analytically

---

## Theoretical Framework

### Task-Based Framework

Following **Acemoglu & Restrepo (2018, 2020)**, we model AI's impact through tasks:

#### Task Categories

1. **Routine Manual**: Repetitive physical tasks (assembly line, data entry)
   - High automation susceptibility (0.8)
   - Low augmentation potential (0.1)

2. **Routine Cognitive**: Rule-based mental tasks (bookkeeping, scheduling)
   - High automation susceptibility (0.7)
   - Medium augmentation potential (0.3)

3. **Non-Routine Manual**: Adaptive physical tasks (caregiving, repair)
   - Medium automation susceptibility (0.3)
   - Low augmentation potential (0.2)

4. **Non-Routine Cognitive**: Creative/analytical tasks (research, strategy)
   - Low automation susceptibility (0.2)
   - High augmentation potential (0.7)

#### Worker Task Composition

Workers perform bundles of tasks based on skill level:

- **Low Skill**: 60% routine manual, 20% routine cognitive, 15% non-routine manual, 5% non-routine cognitive
- **Medium Skill**: 20% routine manual, 40% routine cognitive, 20% non-routine manual, 20% non-routine cognitive
- **High Skill**: 5% routine manual, 15% routine cognitive, 20% non-routine manual, 60% non-routine cognitive

### Labor Market Search Model

Based on **Diamond-Mortensen-Pissarides (DMP)** framework:

#### Matching Function

```
M = m * U^η * V^(1-η)
```

Where:
- M = Number of matches formed
- U = Unemployed workers
- V = Vacancies
- m = Matching efficiency parameter (0.5)
- η = Matching elasticity (0.5 for Cobb-Douglas)

#### Job Finding Rate

```
f = M / U = m * θ^(1-η)
```

Where θ = V/U is labor market tightness

#### Vacancy Filling Rate

```
q = M / V = m * θ^(-η)
```

### Production

Firms use **Cobb-Douglas production function**:

```
Y = A * K^α * L^(1-α)
```

Where:
- Y = Output
- A = Total factor productivity
- K = Capital stock
- L = Effective labor input
- α = Capital share (0.3)
- 1-α = Labor share (0.7)

Effective labor is sum of worker productivities:

```
L = Σ_i skill_i * (1 + AI_augmentation_i)
```

### Worker Behavior

#### Utility Function

Workers maximize lifetime utility:

```
U = Σ_t β^t [u(C_t) + v(employed_t)]
```

Where:
- C_t = Consumption
- employed_t = Employment status
- β = Discount factor
- u(C) = ln(C + 1) (log utility from consumption)
- v(employed) = +10 if employed, 0 if unemployed

#### Consumption Decision

Based on **permanent income hypothesis**:

```
C_t = (1 - s) * Y_t^P
```

Where:
- s = Savings rate (0.2)
- Y^P = Permanent income (approximated by current income + savings return)

#### Job Search

Unemployed workers:
1. Pay search cost (c = $50/period)
2. Receive offers with probability = matching efficiency
3. Accept if wage ≥ reservation wage

**Reservation Wage**:
```
w^R = 0.7 * previous_wage
```

Reservation wage declines with unemployment duration.

### Firm Behavior

#### Profit Maximization

```
π = P * Y - w * L - r * K - C_AI
```

Where:
- P = Output price
- w = Wage bill
- r = Capital cost
- C_AI = AI operating costs (if adopted)

#### Hiring Decision

Firms hire until marginal revenue product of labor equals wage:

```
MRP_L = P * MPL = w
```

Where marginal product of labor:

```
MPL = (1-α) * Y / L
```

#### Wage Setting

Firms adjust wages based on:
- Unfilled vacancies → increase wage
- Low profits → decrease wage
- Market wage pressure

**Wage Adjustment**:
```
w_t = w_{t-1} * (1 + λ * (desired_workers - actual_workers) / actual_workers)
```

Where λ = wage adjustment speed (0.1)

#### AI Adoption Decision

Firms adopt AI if net present value is positive:

```
NPV = Σ_t (CostSavings_t + ProductivityGain_t) / (1+r)^t - AdoptionCost
```

**Cost Savings**:
```
CostSavings = w * L * operating_cost_reduction
```

**Productivity Gain**:
```
ProductivityGain = P * Y * AI_productivity_boost
```

Adoption follows **logistic diffusion curve**:

```
Adoption_Rate(t) = L / (1 + exp(-k(t - t_0)))
```

Where:
- L = Maximum adoption rate (scenario-specific)
- k = Diffusion speed
- t_0 = Inflection point (t = 50)

---

## Agent Specifications

### Worker Agent

**State Variables**:
- skill_level ∈ {low, medium, high}
- skill_value ∈ [0, 1]
- employed ∈ {True, False}
- wage ∈ ℝ+
- savings ∈ ℝ
- task_composition: Dict[task_type → share]

**Parameters**:
- consumption_propensity = 0.8
- learning_rate = 0.01
- skill_depreciation = 0.005
- reservation_wage_factor = 0.7

**Decision Sequence**:
1. If employed → work, receive wage, update skills via learning
2. If unemployed → search, pay costs, consider offers, skills depreciate
3. Make consumption decision
4. Update savings

### Firm Agent

**State Variables**:
- capital ∈ ℝ+
- workers: List[Worker]
- vacancies ∈ ℤ+
- wage_offered ∈ ℝ+
- ai_adopted ∈ {True, False}

**Parameters**:
- capital_share α = 0.3
- depreciation_rate δ = 0.05
- markup μ = 0.2
- investment_rate = 0.15

**Decision Sequence**:
1. Produce with current workforce
2. Calculate profits
3. Consider AI adoption (if not already adopted)
4. Adjust workforce (hire/fire)
5. Adjust wages
6. Invest in capital

### Government Agent

**Policies**:
1. **Unemployment Insurance**
   - Replacement rate: 50% of previous wage
   - Duration: 20 periods
   - Funded by 2% payroll tax

2. **Retraining Programs**
   - Cost: $2,000 per worker
   - Duration: 10 periods
   - Success rate: 70%
   - Skill improvement: +0.3
   - Government subsidy: 100%

3. **Universal Basic Income** (optional)
   - Amount: Configurable
   - Funded by income tax

---

## Market Mechanisms

### Labor Market

#### Matching Process

Each period:
1. Identify unemployed workers
2. Identify firms with vacancies
3. Randomly pair workers and vacancies
4. Match succeeds with probability m (matching efficiency)
5. If matched, negotiate wage
6. Worker accepts if wage ≥ reservation wage

#### Wage Negotiation

**Nash Bargaining** with equal bargaining power:

```
w = (w_R + w_max) / 2
```

Where:
- w_R = Worker's reservation wage
- w_max = Firm's maximum willingness to pay (based on MPL)

Actual wage also reflects **wage stickiness**:

```
w_final = (1 - γ) * w_negotiated + γ * w_previous
```

Where γ = stickiness parameter (0.3)

### Goods Market

#### Price Adjustment

Prices adjust based on excess demand:

```
P_t = P_{t-1} * (1 + λ_P * (D - S) / S)
```

Where:
- D = Total demand (consumption + investment)
- S = Total supply (firm production)
- λ_P = Price adjustment speed (0.15)

#### Demand

**Consumption Demand**:
```
D_C = Σ_workers C_i / P
```

**Investment Demand**:
```
D_I = Σ_firms (π_i * investment_rate) / P
```

**Total Demand**:
```
D = D_C + D_I
```

**Price Elasticity**: Demand adjusted by elasticity ε = 1.2

---

## AI Impact Modeling

### Automation Effect

For worker i with task composition {task_j: share_j}:

**Displacement Risk**:
```
Risk_i = Σ_j (share_j * automation_susceptibility_j * automation_intensity)
```

**Labor Reduction**:

When firm adopts AI, it reduces workforce by:
```
ΔL = -automation_intensity * 0.5 * L
```

Workers laid off based on displacement risk (highest risk first).

### Augmentation Effect

**Productivity Enhancement**:
```
Productivity_AI = Productivity_base * (1 + Σ_j (share_j * augmentation_potential_j * augmentation_intensity))
```

Higher for workers performing more non-routine cognitive tasks.

### Aggregate Effects

#### Employment

```
ΔEmployment = -Automation_Displacement + Productivity_JobCreation
```

Where job creation from productivity:
```
JobCreation = (Productivity_Gain * Employment) * 0.5
```

#### Wages

Skill-biased wage changes:
```
Δw_low = -automation_intensity * 0.4 * AI_adoption_rate
Δw_medium = -automation_intensity * 0.2 * AI_adoption_rate
Δw_high = +augmentation_intensity * 0.3 * AI_adoption_rate
```

#### Labor Share

```
Labor_Share = (Total_Wages) / (Total_Revenue)
```

Automation reduces labor share; augmentation effects depend on parameters.

---

## Calibration

### Data Sources

1. **Labor Market Statistics**
   - Bureau of Labor Statistics (BLS) Current Population Survey
   - Target unemployment rate: 4-6%
   - Target wage ratios (high/low skill): 2.5-3.0

2. **Skill Distribution**
   - Based on O*NET occupational task data
   - Low: 30%, Medium: 50%, High: 20%

3. **Production Parameters**
   - Capital share α = 0.3 (standard macro literature)
   - Labor share = 0.7 (Karabarbounis & Neiman, 2014)

4. **AI Adoption Forecasts**
   - McKinsey Global Institute
   - PwC AI Impact Study
   - Diffusion curves from technology adoption literature

### Parameter Calibration

| Parameter | Value | Source |
|-----------|-------|--------|
| Capital Share (α) | 0.3 | Standard RBC models |
| Depreciation Rate (δ) | 0.05 | BEA fixed asset tables |
| Matching Efficiency (m) | 0.5 | Petrongolo & Pissarides (2001) |
| Wage Stickiness (γ) | 0.3 | Barattieri et al. (2014) |
| Consumption Propensity | 0.8 | NIPA personal savings rate |
| Learning Rate | 0.01 | Mincer earnings functions |
| Automation Intensity | 0.3-0.5 | Frey & Osborne (2017) |
| Augmentation Intensity | 0.2-0.4 | Brynjolfsson et al. (2018) |

### Steady State Targets

Model calibrated to match:
- Unemployment rate: 5% (±1%)
- Wage inequality (90/10): 3.0
- Labor share: 0.65-0.70
- Employment rate by skill: Low 85%, Medium 92%, High 96%

---

## Validation

### Internal Validation

1. **Replication**: Multiple runs with same seed produce identical results ✓
2. **Face Validity**: Behavior matches economic intuition ✓
3. **Extreme Conditions**: Model stable under parameter variations ✓

### External Validation

Comparing to empirical literature:

1. **Unemployment-Vacancy Relationship**
   - Model produces downward-sloping Beveridge curve
   - Consistent with U.S. data (Blanchard & Diamond, 1989)

2. **Wage Dispersion**
   - Gini coefficient: 0.3-0.4
   - Matches U.S. income inequality (Census data)

3. **AI Impact Estimates**
   - Job automation: 10-30% at risk
   - Similar to Frey & Osborne (2017), Arntz et al. (2016)

---

## Limitations

### Simplifications

1. **No Capital-Skill Complementarity**: Capital and labor are substitutes in production, missing complementarity effects

2. **Homogeneous Firms**: All firms use same production technology (except AI adoption)

3. **Closed Economy**: No international trade or offshoring

4. **Perfect Information**: Agents know current state fully

5. **Exogenous Technology**: AI capabilities don't improve over time

6. **No Occupational Mobility**: Workers don't switch skill categories (except via retraining)

### Robustness

Key results are robust to:
- Matching function specification
- Production function parameters (within reasonable ranges)
- Initial distributions of skills and capital

Results sensitive to:
- AI adoption speed (faster = more disruption)
- Automation vs. augmentation balance (determines winners/losers)
- Retraining effectiveness (affects policy success)

---

## References

- Acemoglu, D., & Restrepo, P. (2018). The race between man and machine. American Economic Review, 108(6), 1488-1542.
- Acemoglu, D., & Restrepo, P. (2020). Robots and jobs: Evidence from US labor markets. Journal of Political Economy, 128(6), 2188-2244.
- Arntz, M., Gregory, T., & Zierahn, U. (2016). The risk of automation for jobs in OECD countries. OECD Social, Employment and Migration Working Papers.
- Brynjolfsson, E., & McAfee, A. (2014). The second machine age. WW Norton & Company.
- Frey, C. B., & Osborne, M. A. (2017). The future of employment. Technological Forecasting and Social Change, 114, 254-280.
- Pissarides, C. A. (2000). Equilibrium unemployment theory. MIT press.
- Tesfatsion, L. (2006). Agent-based computational economics: A constructive approach to economic theory. Handbook of computational economics, 2, 831-880.
