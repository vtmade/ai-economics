# Economic Glossary

## Key Terms and Concepts

This glossary provides definitions of economic terms used in the AI Labor Market Simulation.

---

## A

### Agent-Based Model (ABM)
A computational model where autonomous agents interact according to rules, producing emergent macro-level patterns. Unlike equation-based models, ABMs explicitly represent heterogeneous individuals.

**Example**: Our simulation has individual worker and firm agents, each making their own decisions.

### Augmentation
The enhancement of worker productivity through technology, as opposed to replacement. AI augmentation makes workers more effective at their tasks.

**Example**: AI tools that help doctors diagnose diseases faster augment medical skills rather than replacing doctors.

### Automation
The substitution of technology for human labor in performing tasks. Automation reduces labor demand in affected occupations.

**Example**: Self-checkout machines automate cashier tasks.

---

## B

### Bargaining Power
The relative ability of parties in a negotiation to influence outcomes in their favor. In labor markets, refers to workers' vs. employers' ability to influence wages.

**In Model**: Workers and firms have equal bargaining power (0.5) in wage negotiations.

### Beveridge Curve
The inverse relationship between unemployment and job vacancies. When unemployment is high, vacancies tend to be low, and vice versa.

**In Model**: The simulation produces Beveridge curves for each scenario, showing how AI affects this relationship.

---

## C

### Calibration
The process of choosing model parameters to match real-world data or stylized facts.

**In Model**: Parameters are calibrated to match U.S. labor market statistics like unemployment rates and wage ratios.

### Capital
Physical assets used in production (machinery, equipment, buildings, software). In the model, firms accumulate capital through investment.

**In Model**: Firms have capital stock K that depreciates and can be increased through investment.

### Capital Share
The fraction of total income that goes to capital owners (as opposed to workers). Calculated as capital income / total income.

**In Model**: Set to α = 0.3, meaning 30% of output value accrues to capital, 70% to labor.

### Cobb-Douglas Production Function
A commonly used production function: Y = A × K^α × L^(1-α), where output depends on capital (K) and labor (L) with constant returns to scale.

**In Model**: Firms produce using Cobb-Douglas with α = 0.3.

### Consumption
Household spending on goods and services. A key driver of aggregate demand.

**In Model**: Workers consume based on permanent income hypothesis, consuming 80% of income.

---

## D

### Depreciation
The reduction in value of capital over time due to wear and obsolescence.

**In Model**: Capital depreciates at 5% per period.

### Diffusion
The spread of a technology through an economy over time. Often follows an S-shaped (logistic) curve.

**In Model**: AI adoption follows logistic diffusion with scenario-specific speeds.

### Displacement
Workers losing jobs due to automation or technological change.

**In Model**: When firms adopt AI, workers with high routine task content are at greater displacement risk.

---

## E

### Elasticity
The responsiveness of one variable to changes in another, measured as % change in Y / % change in X.

**In Model**: Demand elasticity of 1.2 means 1% price increase causes 1.2% demand decrease.

### Employment Rate
The fraction of workers who are employed. Complement of unemployment rate.

**In Model**: Tracked separately for low, medium, and high-skill workers.

### Endogenous
Variables determined within the model (as opposed to exogenous). Most key variables are endogenous.

**In Model**: Wages, employment, prices, AI adoption are all endogenous outcomes.

### Equilibrium
A state where economic forces are balanced and there's no tendency to change. ABMs often focus on transition dynamics rather than equilibrium.

**In Model**: The model reaches a stochastic steady state but emphasizes transition paths.

---

## F

### Friction
Costs or delays that prevent markets from clearing instantaneously. Search and matching frictions prevent instant unemployment adjustment.

**In Model**: Matching efficiency of 0.5 represents search frictions - not all worker-vacancy pairs match.

---

## G

### GDP (Gross Domestic Product)
The total value of goods and services produced in an economy.

**In Model**: Calculated as total output value: GDP = Price × Total Production.

### Gini Coefficient
A measure of inequality ranging from 0 (perfect equality) to 1 (perfect inequality). Measures income concentration.

**In Model**: Calculated from worker income distribution each period.

---

## H

### Heterogeneity
Variation among agents. Realistic models incorporate heterogeneity rather than assuming representative agents.

**In Model**: Workers have different skills, savings, wages; firms have different capital, productivity.

### Human Capital
The skills, knowledge, and capabilities embodied in workers. Analogous to physical capital.

**In Model**: Represented by worker skill levels that can increase (learning) or decrease (depreciation).

---

## I

### Investment
Spending on capital goods that increases productive capacity.

**In Model**: Firms invest 15% of profits in new capital each period.

---

## L

### Labor Force Participation
The fraction of working-age population that is either employed or actively seeking work.

**In Model**: All agents participate (simplified assumption).

### Labor Market Tightness
The ratio of vacancies to unemployed workers (θ = V/U). High tightness favors workers; low tightness favors firms.

**In Model**: Affects matching rates and bargaining outcomes.

### Labor Share
The fraction of total income paid to workers as wages. Complement of capital share.

**In Model**: Calculated as total wages / total revenue. May decline with automation.

### Learning by Doing
Skill improvement through work experience.

**In Model**: Employed workers' skills increase at rate 0.01 per period.

---

## M

### Marginal Product of Labor (MPL)
The additional output produced by one more unit of labor, holding capital constant.

**In Model**: MPL = (1-α) × Y / L for Cobb-Douglas production.

### Marginal Revenue Product (MRP)
The additional revenue from employing one more worker: MRP = Price × MPL.

**In Model**: Firms hire until MRP = wage.

### Matching Function
A relationship showing how many job matches form as a function of unemployed workers and vacancies.

**In Model**: M = m × U^0.5 × V^0.5 (Cobb-Douglas matching).

### Markup
The amount by which firms price above marginal cost.

**In Model**: Firms apply 20% markup to costs.

---

## N

### Nash Bargaining
A solution concept for two-party negotiations, giving weights to each party's bargaining power.

**In Model**: Used for wage determination with equal weights (0.5, 0.5).

### NPV (Net Present Value)
The sum of discounted future cash flows minus initial cost. Used to evaluate investments.

**In Model**: Firms adopt AI if NPV of expected savings exceeds adoption cost.

---

## P

### Permanent Income Hypothesis
Theory that consumption depends on expected lifetime income, not just current income.

**In Model**: Workers smooth consumption based on income and savings.

### Polarization
Labor market phenomenon where middle-skill jobs decline while low and high-skill jobs grow.

**In Model**: Can emerge when AI automates middle-skill routine tasks.

### Productivity
Output per unit of input, often measured as output per worker.

**In Model**: Worker productivity ranges from 0.1 to 1.0, augmented by AI.

---

## R

### Replacement Rate
In unemployment insurance, the fraction of previous wage paid as benefits.

**In Model**: UI replacement rate = 50%.

### Reservation Wage
The minimum wage at which a worker will accept a job offer.

**In Model**: Set to 70% of previous wage, declining with unemployment duration.

### Routine Tasks
Tasks that follow explicit rules and can be specified in computer code. More susceptible to automation.

**In Model**: Both routine manual and routine cognitive tasks have high automation susceptibility.

---

## S

### Search and Matching
Models of labor markets where finding jobs/workers takes time and effort.

**In Model**: Based on Diamond-Mortensen-Pissarides framework.

### Skill-Biased Technical Change (SBTC)
Technological change that increases demand for high-skill workers relative to low-skill workers.

**In Model**: AI exhibits SBTC, benefiting high-skill workers more.

### Steady State
A condition where key variables remain constant over time (in expectation).

**In Model**: Analysis focuses on steady-state averages over final 50 periods.

---

## T

### Task-Based Framework
An approach to modeling technology impact by decomposing jobs into tasks with varying automation/augmentation potential.

**In Model**: Core framework - workers perform bundles of routine and non-routine tasks.

### Total Factor Productivity (TFP)
The portion of output growth not explained by input growth. Represents technological efficiency.

**In Model**: Base TFP = 1.0, can be enhanced by AI adoption.

---

## U

### Unemployment Insurance (UI)
Government program providing income support to unemployed workers.

**In Model**: Pays 50% of previous wage for up to 20 periods, funded by 2% payroll tax.

### Unemployment Rate
The fraction of labor force that is unemployed and seeking work.

**In Model**: Calculated as unemployed workers / total workers.

### Universal Basic Income (UBI)
Unconditional cash transfer to all citizens regardless of employment status.

**In Model**: Optional policy tool, funded by income tax.

---

## V

### Vacancy
An unfilled job opening posted by a firm.

**In Model**: Firms post vacancies when they want to expand workforce.

### Vacancy Rate
The fraction of total jobs (filled + vacant) that are vacant.

**In Model**: V / (Employment + V).

---

## W

### Wage Inequality
Dispersion in wages across workers, often measured by ratios (90th/10th percentile) or Gini coefficient.

**In Model**: Measured as high-skill wage / low-skill wage ratio and via Gini coefficient.

### Wage Stickiness
The tendency for wages to adjust slowly to market conditions rather than instantly.

**In Model**: Parameter γ = 0.3 means 30% of previous wage carries over in new wage.

---

## Units in the Model

### Time
- 1 period ≈ 1 year (annual frequency)
- Typical simulation: 200 periods ≈ 20 years

### Money
- Dollar amounts are nominal
- Typical wages: $300-$1500 per period
- Prices adjust endogenously

### Skills
- Normalized to [0, 1] scale
- Low: ~0.3, Medium: ~0.6, High: ~0.9

---

## Further Reading

### Books
- Pissarides (2000): *Equilibrium Unemployment Theory*
- Acemoglu & Autor (2011): *Skills, Tasks and Technologies*
- Tesfatsion & Judd (2006): *Handbook of Computational Economics*

### Papers
- Acemoglu & Restrepo (2018): *The Race Between Man and Machine*
- Autor et al. (2003): *The Skill Content of Recent Technological Change*
- Mortensen & Pissarides (1994): *Job Creation and Job Destruction*
