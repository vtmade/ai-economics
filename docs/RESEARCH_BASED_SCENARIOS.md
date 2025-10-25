# Research-Based Scenario Specifications

**Author:** Vinay Thakur
**Date:** October 25, 2025
**Based on:** RESEARCH_SYNTHESIS.md findings from 6 major research papers (2023-2025)

---

## Overview

This document translates empirical research findings into concrete simulation parameters. Each scenario is grounded in specific research papers and represents a plausible pathway for AI labor market impacts between 2025-2035.

---

## Scenario 1: Conservative Gradual (Epoch AI 20-Year Timeline)

**Research Basis:** Epoch AI conservative compute scaling assumptions

**Key Research Findings:**
- Full automation timeline: 20+ years (median estimate)
- 13-18% of occupations have all top tasks remotely performable
- 34% of job tasks can be performed remotely
- Conservative scenario: economy doubles within 20 years

**Simulation Parameters:**

### Timeline
- **Total steps:** 200 (representing 2025-2045, 1 step = 0.1 years)
- **Critical period:** Steps 50-150 (2030-2040)

### AI Adoption
```python
AI_ADOPTION_RATE = 0.02  # 2% per year adoption increase
AI_DIFFUSION_SPEED = 0.03  # Slow diffusion (β in logistic curve)
AI_MAX_ADOPTION = 0.35  # 35% ceiling (only tasks that can be remote)
```

### Automation Intensity
```python
AUTOMATION_RATE_ROUTINE = 0.25  # 25% of routine cognitive tasks
AUTOMATION_RATE_MANUAL = 0.05  # 5% of manual tasks
AUGMENTATION_RATE_NONROUTINE = 0.15  # 15% productivity boost
```

### Labor Market
```python
MATCHING_EFFICIENCY = 0.5  # Baseline
SEPARATION_RATE = 0.02  # 2% quarterly
RETRAINING_EFFECTIVENESS = 0.3  # 30% skill upgrade success
```

### Expected Outcomes (Research-Based)
- **Unemployment:** +2-3 percentage points by 2035
- **GDP:** +15-20% by 2045
- **Productivity:** +0.3-0.5pp annually
- **Displacement:** Gradual, mostly offset by new job creation

---

## Scenario 2: McKinsey Baseline (Moderate 2030 Effects)

**Research Basis:** McKinsey Global Institute (June 2023) - "The Economic Potential of Generative AI"

**Key Research Findings:**
- 60-70% of current employee time automatable
- $2.6-4.4 trillion annual economic impact
- 0.5-0.9 percentage point US productivity growth through 2030
- 34 percentage point increase in technical expertise automation potential
- Management tasks: 16% → 49% automatable

**Simulation Parameters:**

### Timeline
- **Total steps:** 150 (representing 2025-2040, 1 step = 0.1 years)
- **Critical period:** Steps 30-80 (2028-2033)

### AI Adoption
```python
AI_ADOPTION_RATE = 0.05  # 5% per year adoption increase
AI_DIFFUSION_SPEED = 0.08  # Moderate diffusion
AI_MAX_ADOPTION = 0.65  # 65% ceiling (mid-range of 60-70%)
```

### Automation Intensity
```python
AUTOMATION_RATE_ROUTINE = 0.60  # 60% of routine cognitive tasks
AUTOMATION_RATE_MANUAL = 0.15  # 15% of manual tasks
AUGMENTATION_RATE_NONROUTINE = 0.34  # 34% boost (McKinsey expertise jump)
```

### Task Composition Updates
```python
# High-skill workers (managers, professionals)
TASKS_HIGH_SKILL = {
    'routine_cognitive': 0.35,  # Increased from 0.3
    'nonroutine_cognitive': 0.50,  # Management + expertise
    'routine_manual': 0.05,
    'nonroutine_manual': 0.10
}

# Medium-skill workers
TASKS_MEDIUM_SKILL = {
    'routine_cognitive': 0.50,  # Office support
    'nonroutine_cognitive': 0.25,
    'routine_manual': 0.15,
    'nonroutine_manual': 0.10
}
```

### Labor Market
```python
MATCHING_EFFICIENCY = 0.5
SEPARATION_RATE = 0.025  # 2.5% quarterly (slightly elevated)
RETRAINING_EFFECTIVENESS = 0.4  # 40% with moderate policy
```

### Sectoral Impacts (for heterogeneous firms)
```python
HIGH_EXPOSURE_SECTORS = ['customer_service', 'office_support', 'banking_finance']
SECTOR_AUTOMATION_MULTIPLIER = 1.5  # 50% higher automation in exposed sectors
```

### Expected Outcomes (McKinsey Projections)
- **Unemployment:** +100-200K by 2030 (US scale adjusted)
- **GDP:** +0.5-0.9pp productivity annually
- **Wage effects:** Skill-biased, knowledge workers affected
- **Office support jobs:** -1.6M displaced
- **Time savings:** 60-70% of workforce equivalent

---

## Scenario 3: TBI Aggressive Displacement (Rapid 2025-2030)

**Research Basis:** Tony Blair Institute (November 2024) - "The Impact of AI on the Labour Market"

**Key Research Findings:**
- +180,000 unemployment by 2030 (UK)
- Peak displacement: 60,000-275,000 jobs per year
- 1-3 million jobs displaced by 2050
- +6% GDP by 2035
- 23% of private-sector workforce time savings

**Simulation Parameters:**

### Timeline
- **Total steps:** 150 (representing 2025-2040)
- **Critical period:** Steps 20-60 (2027-2031) - RAPID onset

### AI Adoption
```python
AI_ADOPTION_RATE = 0.10  # 10% per year - aggressive
AI_DIFFUSION_SPEED = 0.15  # Fast diffusion
AI_MAX_ADOPTION = 0.70  # 70% ceiling
```

### Automation Intensity
```python
AUTOMATION_RATE_ROUTINE = 0.70  # 70% of routine cognitive
AUTOMATION_RATE_MANUAL = 0.20  # 20% of manual
AUGMENTATION_RATE_NONROUTINE = 0.30  # 30% boost
```

### Labor Market (with friction)
```python
MATCHING_EFFICIENCY = 0.35  # REDUCED - labor market struggles to absorb
SEPARATION_RATE = 0.035  # 3.5% quarterly - elevated
RETRAINING_EFFECTIVENESS = 0.25  # 25% - insufficient policy response
RETRAINING_DELAY = 4  # 4-step delay in skill upgrade
```

### Sectoral Concentration
```python
# Admin, secretarial, customer service hit hardest
SECTOR_EXPOSURE = {
    'admin_secretarial': 0.85,
    'customer_service': 0.80,
    'banking_finance': 0.75,
    'professional_services': 0.45,
    'construction': 0.15
}
```

### Age Demographics (from RAND findings)
```python
# 22-25 year-olds most affected
YOUNG_WORKER_DISPLACEMENT_MULTIPLIER = 1.8
AGE_GROUP_22_25_SHARE = 0.15  # 15% of workforce
```

### Expected Outcomes (TBI Projections)
- **Unemployment:** +180K by 2030 (scaled to model size)
- **Peak displacement:** 60K-275K/year
- **GDP:** +6% by 2035
- **Time savings:** 23% of workforce equivalent
- **Recovery:** Partial by 2040 with new job creation

---

## Scenario 4: Anthropic Comprehensive Policy Response

**Research Basis:** Anthropic (2024) - "Economic Policy Responses to AI"

**Key Research Findings:**
- 9-category graduated policy framework
- $10,000/year per trainee workforce grants
- ~$700M annually for Automation Adjustment Assistance (baseline)
- Three-stage response: workforce development → fiscal support → wealth redistribution
- Faster displacement than expected: "Users increasingly delegate full tasks"

**Simulation Parameters:**

### Timeline
- **Total steps:** 150 (2025-2040)
- **Policy phases:** Steps 1-50 (prevention), 51-100 (mitigation), 101-150 (redistribution)

### AI Adoption (same as McKinsey baseline)
```python
AI_ADOPTION_RATE = 0.05
AI_DIFFUSION_SPEED = 0.08
AI_MAX_ADOPTION = 0.65
```

### Automation Intensity (same as McKinsey)
```python
AUTOMATION_RATE_ROUTINE = 0.60
AUTOMATION_RATE_MANUAL = 0.15
AUGMENTATION_RATE_NONROUTINE = 0.34
```

### Policy Interventions (KEY DIFFERENTIATOR)

#### Phase 1: Workforce Development (Steps 1-50)
```python
RETRAINING_ENABLED = True
RETRAINING_COST_PER_WORKER = 10000  # $10K annually (Anthropic estimate)
RETRAINING_EFFECTIVENESS = 0.60  # 60% success rate with proper funding
RETRAINING_COVERAGE = 0.80  # 80% of displaced workers reached
TRAINING_GRANT_AMOUNT = 10000  # Direct grants to workers
```

#### Phase 2: Fiscal Support (Steps 51-100)
```python
UNEMPLOYMENT_INSURANCE_BENEFIT = 0.70  # 70% wage replacement (up from 50%)
UI_DURATION = 26  # Extended duration (26 steps = ~2.6 years)
AUTOMATION_ADJUSTMENT_ASSISTANCE = True
AAA_BUDGET = 700_000_000  # $700M annually baseline (scales with displacement)
AAA_COVERAGE = 0.90  # 90% of automation-displaced workers
```

#### Phase 3: Wealth Redistribution (Steps 101-150, if needed)
```python
# Triggered if unemployment > threshold
WEALTH_TAX_ENABLED = False  # Initially off
WEALTH_TAX_THRESHOLD = 0.15  # Enable if unemployment > 15%
WEALTH_TAX_RATE = 0.02  # 2% annual on business wealth
VAT_RATE = 0.05  # 5% value-added tax
SOVEREIGN_WEALTH_FUND = True  # Capture AI returns
```

#### Continuous Policies
```python
# Tax incentives for human capital
HUMAN_CAPITAL_TAX_CREDIT = 0.20  # 20% credit for training investment
# Corporate tax reforms
PROFIT_SHIFTING_CLOSED = True  # Eliminate loopholes
EFFECTIVE_CORPORATE_TAX_RATE = 0.25  # Up from 0.21
```

### Labor Market
```python
MATCHING_EFFICIENCY = 0.60  # IMPROVED with AAA programs
SEPARATION_RATE = 0.020  # 2.0% - kept low by policy
RETRAINING_DELAY = 2  # Faster retraining (2 steps)
```

### Expected Outcomes (Anthropic Framework)
- **Unemployment:** Limited increase (<5pp) despite automation
- **GDP:** Higher than McKinsey baseline due to better transitions
- **Fiscal cost:** $10K/worker + $700M baseline AAA
- **Inequality:** Moderated by redistribution mechanisms
- **Labor share:** Maintained or improved

---

## Scenario 5: RAND Empirical Evidence (Data-Calibrated)

**Research Basis:** RAND Corporation (2024-2025) - "Macroeconomic Implications of Artificial Intelligence"

**Key Research Findings:**
- +$7,000 real per-capita GDP by 2035 from moderate AI gains
- Correlation 0.57 between high AI adoption occupations and unemployment gains
- 22-25 year-olds most affected demographically
- Software development, customer service, clerical work primary occupations
- "Limited visibility" - high uncertainty

**Simulation Parameters:**

### Timeline
- **Total steps:** 150 (2025-2040)
- **Calibration period:** Use steps 1-30 to match 2024-2025 empirical data

### AI Adoption (empirically calibrated)
```python
AI_ADOPTION_RATE = 0.05  # Moderate
AI_DIFFUSION_SPEED = 0.08
AI_MAX_ADOPTION = 0.60
```

### Unemployment-AI Correlation Target
```python
# Calibrate to achieve correlation ≈ 0.57
TARGET_CORRELATION = 0.57
OCCUPATIONAL_AI_EXPOSURE = {
    'software_dev': 0.75,  # High exposure
    'customer_service': 0.70,
    'clerical': 0.65,
    'manufacturing': 0.25,
    'healthcare': 0.20
}
```

### Automation Intensity
```python
AUTOMATION_RATE_ROUTINE = 0.55  # Moderate (55%)
AUTOMATION_RATE_MANUAL = 0.12
AUGMENTATION_RATE_NONROUTINE = 0.30
```

### Demographic Segmentation
```python
# Age group vulnerability
AGE_22_25_DISPLACEMENT_RATE = 0.08  # 8% higher than average
AGE_GROUP_SHARES = {
    '22-25': 0.12,
    '26-35': 0.25,
    '36-50': 0.40,
    '51-65': 0.23
}
```

### Labor Market
```python
MATCHING_EFFICIENCY = 0.45  # Moderate friction
SEPARATION_RATE = 0.025
RETRAINING_EFFECTIVENESS = 0.35  # Modest policy
```

### GDP Target
```python
# Calibrate to achieve +$7,000 per capita by step 100 (2035)
TARGET_GDP_GAIN = 7000  # per capita
PRODUCTIVITY_GAIN_TARGET = 0.006  # Annual (~0.6pp)
```

### Expected Outcomes (RAND Estimates)
- **GDP per capita:** +$7,000 by 2035
- **Unemployment-AI correlation:** 0.57
- **Demographic effects:** Young workers (22-25) hit hardest
- **Occupational pattern:** Software, customer service, clerical

---

## Cross-Scenario Comparison Matrix

| Parameter | Conservative | McKinsey | TBI Aggressive | Anthropic Policy | RAND Empirical |
|-----------|-------------|----------|----------------|------------------|----------------|
| **Adoption Rate** | 2%/year | 5%/year | 10%/year | 5%/year | 5%/year |
| **Max Adoption** | 35% | 65% | 70% | 65% | 60% |
| **Routine Automation** | 25% | 60% | 70% | 60% | 55% |
| **Augmentation** | 15% | 34% | 30% | 34% | 30% |
| **Matching Efficiency** | 0.50 | 0.50 | 0.35 ↓ | 0.60 ↑ | 0.45 |
| **Retraining Effect** | 30% | 40% | 25% ↓ | 60% ↑ | 35% |
| **Timeline** | 20 years | 15 years | 5-10 years | 15 years | 10 years |
| **Policy Response** | Minimal | Moderate | Insufficient | Comprehensive | Modest |
| **Unemployment Impact** | +2-3pp | +100-200K | +180K (rapid) | <+5pp | Varies by age |
| **GDP Impact by 2035** | +15-20% | +0.5-0.9pp/yr | +6% | Higher than McKinsey | +$7K per capita |

---

## Implementation Mapping to config.py

### Base Parameters (All Scenarios)
```python
# From config.py
NUM_WORKERS = 100  # Increased for better statistical properties
NUM_FIRMS = 20  # Increased for sectoral heterogeneity
NUM_STEPS = 150  # Standard timeline

# Production function (unchanged)
CAPITAL_SHARE_ALPHA = 0.30  # Cobb-Douglas
DEPRECIATION_RATE = 0.05
```

### Scenario-Specific Overrides

Each scenario will override base parameters:

**Conservative:**
```python
scenario_config = {
    'ai_adoption_rate': 0.02,
    'ai_diffusion_speed': 0.03,
    'ai_max_adoption': 0.35,
    'automation_rate_routine': 0.25,
    # ... etc
}
```

### Implementation Plan

1. **Update `config.py`:**
   - Add research-backed default values
   - Add scenario override dictionaries
   - Include research citations in comments

2. **Update `src/scenarios/runner.py`:**
   - Replace old scenarios with 5 research-based ones
   - Implement scenario-specific parameter loading
   - Add validation against research targets

3. **Update `src/ai_models/ai_impact.py`:**
   - Adjust task automation calculation to match research rates
   - Implement sectoral heterogeneity
   - Add demographic effects (age groups)

4. **Update `src/agents/firm.py`:**
   - Add sector-specific automation exposure
   - Implement differentiated AI adoption by sector

5. **Update `src/agents/worker.py`:**
   - Add age demographic attribute
   - Implement age-specific displacement vulnerability

6. **Update `src/agents/government.py`:**
   - Implement Anthropic policy framework
   - Add phased policy activation
   - Include fiscal cost tracking

---

## Validation Targets

Each scenario should be validated against research projections:

### Conservative (Epoch AI)
- [ ] Economy doubles within 20 years
- [ ] Gradual displacement pattern
- [ ] ~35% maximum adoption

### McKinsey Baseline
- [ ] 0.5-0.9pp annual productivity growth
- [ ] 60-70% work time automatable
- [ ] Office support jobs: significant displacement
- [ ] Knowledge workers affected

### TBI Aggressive
- [ ] +180K unemployment by 2030 (scaled)
- [ ] Peak displacement 60K-275K/year
- [ ] +6% GDP by 2035
- [ ] 23% workforce time savings

### Anthropic Policy
- [ ] Unemployment limited despite automation
- [ ] $10K/worker training costs
- [ ] Graduated policy activation
- [ ] Better outcomes than baseline

### RAND Empirical
- [ ] +$7K per capita GDP by 2035
- [ ] 0.57 correlation: AI adoption & unemployment
- [ ] 22-25 age group most affected
- [ ] Software, customer service, clerical hit hardest

---

## Research Quality Assessment

| Scenario | Research Credibility | Parameter Confidence | Timeline Confidence |
|----------|---------------------|---------------------|---------------------|
| Conservative | High (technical analysis) | High | Low (long-term) |
| McKinsey | High (extensive data) | High | Medium |
| TBI Aggressive | Medium (GPT-4 estimates) | Medium | Medium |
| Anthropic Policy | High (direct deployment data) | High | Medium |
| RAND Empirical | Very High (academic) | Medium (limited data) | Low (early stage) |

**Overall Confidence:**
- Direction of effects: **High**
- Magnitude of effects: **Medium** (wide ranges)
- Precise timing: **Low** (2-3 year uncertainty)

---

## Next Steps

1. ✅ Document complete → this file
2. ⏳ Update `config.py` with research parameters
3. ⏳ Revise scenario implementations
4. ⏳ Run all 5 scenarios
5. ⏳ Validate against research targets
6. ⏳ Generate research-backed final report

---

**References:**
- McKinsey Global Institute (2023). "The Economic Potential of Generative AI"
- Anthropic (2024). "Economic Policy Responses to AI"
- RAND Corporation (2024-2025). "Macroeconomic Implications of Artificial Intelligence"
- Rabobank (2024). "The Economic Impact of AI: Four Scenarios"
- Epoch AI (2024-2025). "The Economic Consequences of Automating Remote Work"
- Tony Blair Institute (2024). "The Impact of AI on the Labour Market"

See `docs/RESEARCH_SYNTHESIS.md` for detailed research summaries.

---

**Document Version:** 1.0
**Author:** Vinay Thakur
**Date:** October 25, 2025
