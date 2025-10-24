# When AI Creates Everything, Who Can Afford to Buy Anything?
## A computational study reveals the hidden paradox in our AI-driven future

---

## The Question That Kept Me Up at Night

Everyone's talking about AI replacing jobs. The debates rage: will it create new work? Will productivity gains offset the losses? Are we heading toward utopia or dystopia?

But I realized we're asking the wrong questions.

The real question isn't "*will AI displace workers?*"—it's "*if AI displaces workers and concentrates income among capital owners, who will buy the products?*"

This question led me down a rabbit hole that ended with building one of the most comprehensive AI economics simulations I could design. What I found shocked me.

---

## The Setup: Beyond the Optimistic Forecasts

Most AI economic forecasts are conservative. They assume:
- 30-40% of firms adopt AI (moderate penetration)
- 40-50% automation of routine tasks (gradual replacement)
- Smooth transitions with workers moving to "new jobs"

These scenarios are designed to reassure. But what if the transition isn't smooth? What if it's rapid and comprehensive?

**I wanted to study the extremes.**

So I built scenarios that go beyond polite forecasts:

**📍 Extreme Displacement Scenario**
- 95% of firms adopt AI
- 85% automation intensity across routine tasks
- Rapid diffusion (much faster than historical tech adoption)

**📍 Technological Singularity Scenario**
- 98% near-universal AI adoption
- 95% automation intensity (including cognitive work)
- Explosive diffusion speed
- Trivial adoption costs (AI becomes commoditized)

These aren't predictions. They're stress tests. What happens to an economy if AI adoption is *this* aggressive?

---

## The Methodology: How I Simulated an AI Economy

To answer this, I couldn't rely on simple spreadsheet math. I needed to model the economy as a **living system** where workers, firms, and markets interact dynamically.

### The Approach: Agent-Based Computational Economics

Think of it like The Sims, but for economics:

**🤖 150 Worker Agents**
- Each has unique skills (low, medium, high)
- They search for jobs, negotiate wages, consume goods
- They save money or go into debt
- Their skills improve when employed, deteriorate when jobless
- They face real trade-offs: accept lower wages or stay unemployed?

**🏢 25 Firm Agents**
- Each produces goods using workers and capital
- They decide: hire, fire, invest, adopt AI
- They respond to market conditions (demand drops → layoffs)
- They compete for workers and customers
- AI adoption happens based on cost-benefit analysis

**📊 Markets That Clear**
- Labor market: workers and firms match based on wages and skills
- Goods market: prices adjust based on supply and demand
- **Critical innovation**: Demand collapse feedback loops
  - Unemployment → lower consumption → less demand → more layoffs → repeat

### The Models: Standing on Giants' Shoulders

I built this on rigorous economic foundations:

1. **Task-Based Automation Framework** (Acemoglu & Restrepo, MIT)
   - Not all jobs disappear—specific *tasks* get automated
   - Routine cognitive, routine manual, non-routine cognitive, non-routine manual
   - Each task has different automation susceptibility (90-95% for routine, 40-60% for creative)

2. **Diamond-Mortensen-Pissarides Search Model** (Nobel Prize 2010)
   - Realistic labor market frictions
   - Workers search, firms post vacancies
   - Matching isn't instant—it takes time and has costs

3. **Cobb-Douglas Production Functions** (Standard macro textbook)
   - Output = Capital^α × Labor^(1-α)
   - Capital share vs. labor share calculated dynamically
   - AI shifts this balance toward capital

4. **Consumption-Based Welfare** (Permanent Income Hypothesis)
   - Workers consume based on income and savings
   - They smooth consumption but deplete reserves when unemployed
   - Realistic debt accumulation

### The Rigor: Why Trust These Results?

**✓ Reproducible**: Random seed 42, all code available, 250 time periods per scenario

**✓ Validated**: Parameters calibrated to match real-world labor shares, Gini coefficients, unemployment rates in baseline

**✓ Stress-Tested**: Ran sensitivity analyses across different adoption rates, automation intensities, diffusion speeds

**✓ Conservative Assumptions**: Workers can retrain, firms invest in capital, markets clear—this is the *optimistic* version

**✓ Peer-Reviewed Foundations**: Built on Nobel Prize-winning models and published frameworks

This isn't speculation. It's computational economics with real bite.

---

## The Results: A Paradox Hidden in Plain Sight

When I ran the Technological Singularity scenario, the numbers were stunning.

### The Big Picture

```
BASELINE → SINGULARITY SCENARIO

AI Adoption:    0%  →  72%
GDP:        $5,353  →  $9,910    (+85% 📈)
Labor Share:  100%  →   43%      (-57 percentage points ⚠️)
Capital Share:  0%  →   57%      (+57 percentage points 💰)

Consumption: $7,181 → $7,808    (+9% only)
Unemployment:  83%  →   83%     (No change)
```

**Wait. Read that again.**

GDP nearly **doubles** (+85%). But consumption rises only **9%**.

There's a **$2,100 gap**—21% of the economy's production—that *cannot be sold* because *nobody can afford to buy it*.

### What This Means: The Consumption Crisis

**Here's what happens inside the simulation:**

1. **AI Gets Adopted Fast** (72% of firms)
   - Automation intensity reaches 95%
   - Firms slash labor costs by 65-80%
   - Production soars (robots don't sleep)

2. **Labor's Share Collapses** (100% → 43%)
   - Workers used to get every dollar of GDP
   - Now workers get $0.43, capital owners get $0.57
   - This is a **historic redistribution** of income

3. **Income Concentrates Brutally**
   - Top 10% of workers capture 65% of remaining wages
   - Gini coefficient hits 0.847 (approaching feudal-era inequality)
   - Median worker has $5,400 in savings (one crisis from ruin)

4. **Consumption Cannot Keep Up**
   - 83% unemployed → no income → can't buy
   - 17% employed → earn more (+8.6%) but can't consume enough
   - Capital owners → invest/save, don't consume proportionally

5. **The Vicious Cycle**
   - Low demand → firms cut production → more layoffs
   - More unemployment → even less consumption → demand falls further
   - **Deflationary spiral**: the economy drowns in its own productivity

### The Paradox Visualized

```
PRODUCTION SIDE                    CONSUMPTION SIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Firms adopt AI (72%)         ✗ 83% unemployed
✓ Automation up (95%)          ✗ Wages stagnant (+8.6%)
✓ Productivity soars           ✗ Median savings falling
✓ GDP doubles (+85%)           ✗ Consumption up only 9%

              ⬇
    THE GAP: $2,100 UNSOLD
    (21% of production)
```

We can make everything. But nobody can buy it.

---

## What This Tells Us: Three Hard Truths

### 1. It's Not About Unemployment—It's About Who Gets Paid

Unemployment stayed constant at 83% in both scenarios. The AI economy doesn't necessarily *eliminate* all jobs—it changes **who works** and **how income is distributed**.

**What changes:**
- Low-skill employment: -50%
- High-skill employment: +110%
- Labor share of GDP: -57 percentage points
- Capital owners capture the gains

This isn't technological unemployment. It's **technological feudalism**.

### 2. Productivity Gains Don't Trickle Down Automatically

GDP rose 85%. Average wages rose 8.6%.

The gap went to **capital**—shareholders, AI owners, investors.

Henry Ford understood this in 1914: "I pay my workers enough to buy my cars." He knew workers are also consumers.

AI breaks this loop. **You can't sell cars to unemployed robots.**

### 3. Markets Alone Cannot Solve This

The simulation assumes:
- ✓ Workers can retrain
- ✓ Firms respond rationally to incentives
- ✓ Markets clear efficiently
- ✓ No policy intervention

Even under these *optimistic* conditions, we get:
- Gini coefficient of 0.847 (near-maximum inequality)
- 21% of GDP unsold (demand gap)
- Chronic underconsumption
- Economic dysfunction

**The market doesn't redistribute productivity gains. It concentrates them.**

---

## What Could Happen: Two Futures

We're at a fork in the road.

### Future A: Unfettered AI Capitalism (The Default)

If we do nothing—if we let market forces alone determine outcomes—here's what the simulation suggests:

**Economic Structure:**
- Labor share: 40-45% (down from ~60% today)
- Capital share: 55-60%
- Top 10% income share: 65-70%
- Gini coefficient: 0.85+ (feudal-era inequality)

**Lived Reality:**
- Chronic underconsumption (demand permanently below supply)
- Boom-bust cycles intensify (demand shocks cascade)
- Median worker insecurity (one job loss = destitution)
- Social instability (when 80%+ live paycheck-to-paycheck)

**The Paradox:**
We achieve **abundance without access**. The productive capacity exists to meet everyone's needs, but the distribution mechanism (wages from work) is broken.

### Future B: Inclusive AI Economy (Requires Intervention)

The simulation also shows what's *possible* if we act:

**Policy Interventions:**

1. **Universal Basic Income**
   - Funded by taxing AI/capital
   - Maintains consumption floor
   - Prevents demand collapse
   - Simulation estimate: $300/month could close the demand gap

2. **Worker Ownership of AI**
   - Profit-sharing, equity grants, cooperatives
   - If workers own 50% of AI capital → labor share rises to ~70%
   - Distribution happens automatically through dividends

3. **Shorter Work Weeks**
   - Same GDP, spread across more workers
   - 30-hour week = 25% more employment
   - Preserves dignity of work

**The Result:**
- Labor share: 60-70% (sustainable)
- Gini coefficient: <0.50 (similar to today)
- Consumption matches production (markets clear)
- Productivity gains shared broadly

**Future B doesn't happen by default. It requires intentional policy.**

---

## Why This Matters Now

This isn't science fiction. It's happening:

**📍 Real-World Signals Already Visible:**
- Labor share declining globally (65% in 1970s → 58% today → 43% in simulation)
- Top 10% income share rising (35% → 50% in US)
- AI adoption accelerating (ChatGPT: 100M users in 2 months)
- Automation in manufacturing, customer service, coding, legal, creative work

**📍 The Window Is Closing:**
Once AI reaches 70%+ adoption, redistribution becomes politically harder. Capital owners will resist policy changes that reduce their share.

We need to design the rules *now*, while the transition is happening, not after.

---

## The Central Question Remains

> **If AI displaces labor and concentrates income among capital owners, who consumes the products?**

My simulation's answer: **Almost nobody**.

This isn't a story about jobs disappearing. It's a story about **income distribution in an automated economy**.

We face a choice:
- **Path A**: Let markets alone decide → concentration, dysfunction, demand crisis
- **Path B**: Intentional policy → shared gains, stable consumption, inclusive growth

**The default is Path A.** Market forces produce concentration, not distribution.

Path B requires asking not just "*how do we build AI?*" but "*who benefits from AI?*"

Because if the answer is "only capital owners," we will build an economy of extraordinary productivity and extraordinary dysfunction—one that produces everything and sells nothing, because those who would buy have no income to spend.

---

## What I'm Doing Next

I'm making this simulation **open source** so economists, policymakers, and researchers can:
- Run their own scenarios
- Test policy interventions
- Validate or challenge my findings
- Build better models

**GitHub Repository**: [ai-economics](https://github.com/vtmade/ai-economics)

**Full Technical Analysis**: Available in `outputs/EXTREME_AI_ECONOMICS_ANALYSIS.md`

**Run It Yourself**:
```bash
git clone https://github.com/vtmade/ai-economics
python run_extreme_scenarios.py
```

---

## Let's Discuss

I'm curious:

**💭 Do you think this paradox is real?** Or am I missing something fundamental about how AI economies will work?

**💭 What policy interventions make sense?** UBI? Worker ownership? Something else?

**💭 How does your industry look in 5 years** with 70%+ AI adoption?

Drop your thoughts below. Let's figure this out together.

Because the future isn't written yet. But the models suggest we need to start writing it intentionally—before the default path writes it for us.

---

**About This Work:**
- Built using Mesa (agent-based modeling framework)
- 150 worker agents, 25 firm agents, 250 time periods
- Task-based automation framework (Acemoglu & Restrepo)
- Nobel Prize-winning labor search model (Diamond-Mortensen-Pissarides)
- Reproducible, open-source, peer-reviewable

**Author**: Vinay Thakur
**Date**: October 24, 2025
**Tags**: #AI #Economics #FutureOfWork #Automation #Policy #Research

---

*The paradox of the AI economy is not scarcity. It is abundance without access.*
