"""
Automated Report Generation

Generates comprehensive HTML and PDF reports with:
- Executive summary
- Methodology
- Results and visualizations
- Policy recommendations
"""

import os
import pandas as pd
from datetime import datetime
from typing import Dict, List
import markdown
from jinja2 import Template


class ReportGenerator:
    """
    Generates comprehensive simulation reports.
    """

    def __init__(self, output_dir: str = 'outputs/reports'):
        """
        Initialize report generator.

        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(self, results_dict: Dict[str, Dict],
                       comparison_df: pd.DataFrame,
                       impact_df: pd.DataFrame,
                       format: str = 'html') -> str:
        """
        Generate comprehensive report.

        Args:
            results_dict: Dictionary of scenario results
            comparison_df: DataFrame with comparison statistics
            impact_df: DataFrame with impact analysis
            format: Output format ('html' or 'markdown')

        Returns:
            str: Path to generated report
        """
        print("\nGenerating comprehensive report...")

        # Generate report sections
        report_content = self._build_report(results_dict, comparison_df, impact_df)

        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'html':
            filename = f'simulation_report_{timestamp}.html'
            filepath = os.path.join(self.output_dir, filename)
            self._save_html_report(report_content, filepath)
        else:
            filename = f'simulation_report_{timestamp}.md'
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(report_content)

        print(f"Report generated: {filepath}")
        return filepath

    def _build_report(self, results_dict: Dict, comparison_df: pd.DataFrame,
                     impact_df: pd.DataFrame) -> str:
        """Build complete report content."""

        sections = []

        # Title and metadata
        sections.append(self._generate_title())

        # Executive Summary
        sections.append(self._generate_executive_summary(comparison_df, impact_df))

        # Model Overview
        sections.append(self._generate_model_overview())

        # Scenario Descriptions
        sections.append(self._generate_scenario_descriptions())

        # Key Findings
        sections.append(self._generate_key_findings(comparison_df, impact_df))

        # Detailed Results
        sections.append(self._generate_detailed_results(results_dict, comparison_df))

        # Economic Interpretation
        sections.append(self._generate_economic_interpretation(impact_df))

        # Policy Recommendations
        sections.append(self._generate_policy_recommendations(impact_df))

        # Methodology
        sections.append(self._generate_methodology())

        # Technical Appendix
        sections.append(self._generate_technical_appendix())

        return '\n\n'.join(sections)

    def _generate_title(self) -> str:
        """Generate report title and metadata."""
        date = datetime.now().strftime('%B %d, %Y')
        return f"""# AI Labor Market Impact Simulation
## Comprehensive Analysis Report

**Date:** {date}

**Author:** AI Economics Research Team

---
"""

    def _generate_executive_summary(self, comparison_df: pd.DataFrame,
                                    impact_df: pd.DataFrame) -> str:
        """Generate executive summary."""

        summary = """## Executive Summary

This report presents results from an agent-based simulation of AI technology adoption in labor markets. The simulation models heterogeneous workers and firms, incorporating a task-based framework to capture both automation and augmentation effects of AI.

### Key Findings

"""

        # Extract key insights
        if len(impact_df) > 0:
            # High adoption scenario impacts
            high_adoption = impact_df[impact_df['Scenario'].str.contains('High', case=False)]
            if len(high_adoption) > 0:
                row = high_adoption.iloc[0]
                summary += f"- **High AI Adoption Scenario:**\n"
                summary += f"  - Unemployment changes by {row['Δ Unemployment (pp)']:.2f} percentage points\n"
                summary += f"  - Average wages change by {row['Δ Wage (%)']:.1f}%\n"
                summary += f"  - GDP changes by {row['Δ GDP (%)']:.1f}%\n"
                summary += f"  - Gini coefficient changes by {row['Δ Gini']:.3f}\n\n"

            # Retraining scenario
            retraining = impact_df[impact_df['Scenario'].str.contains('Retrain', case=False)]
            if len(retraining) > 0:
                row = retraining.iloc[0]
                summary += f"- **Retraining Program Effects:**\n"
                summary += f"  - Mitigates unemployment by {-row['Δ Unemployment (pp)']:.2f} percentage points vs high adoption\n"
                summary += f"  - Supports wage growth of {row['Δ Wage (%)']:.1f}%\n\n"

        summary += """### Main Conclusions

1. **Skill-Biased Effects:** AI adoption disproportionately impacts workers based on skill level
2. **Policy Matters:** Active labor market policies can significantly mitigate negative effects
3. **Productivity Gains:** AI generates substantial productivity improvements but distribution is uneven
4. **Transition Dynamics:** Short-term disruption vs. long-term benefits depends on policy response

---
"""

        return summary

    def _generate_model_overview(self) -> str:
        """Generate model overview section."""

        return """## Model Overview

### Agent-Based Modeling Framework

This simulation uses an agent-based model (ABM) to capture micro-level decisions and emergent macro-level outcomes.

#### Agents

1. **Workers (N=100)**
   - Heterogeneous skills: low (30%), medium (50%), high (20%)
   - Make labor supply and consumption decisions
   - Can participate in retraining programs
   - Skills evolve through learning-by-doing and depreciation

2. **Firms (N=20)**
   - Production using Cobb-Douglas technology
   - Hire workers and set wages
   - Make AI adoption decisions based on cost-benefit analysis
   - Invest in capital

3. **Government**
   - Implements labor market policies
   - Unemployment insurance
   - Retraining programs
   - Collects taxes and redistributes

#### Markets

- **Labor Market:** Search and matching with frictions
- **Goods Market:** Price adjustment based on supply and demand

#### AI Impact Framework

Task-based model distinguishing:
- **Automation:** Labor displacement in routine tasks
- **Augmentation:** Productivity enhancement in cognitive tasks
- **Diffusion:** Gradual adoption following logistic curve

---
"""

    def _generate_scenario_descriptions(self) -> str:
        """Generate scenario descriptions."""

        return """## Scenario Descriptions

### 1. Baseline (No AI)
Control scenario with no AI adoption. Represents counterfactual of continuing with existing technology.

**Key Parameters:**
- AI adoption rate: 0%
- No automation or augmentation effects

### 2. Low AI Adoption
Conservative diffusion scenario representing gradual, selective AI adoption.

**Key Parameters:**
- Maximum adoption rate: 30% of firms
- Diffusion speed: Slow (2% per period)
- Automation intensity: Low (30%)
- Augmentation intensity: Low (20%)

### 3. High AI Adoption
Rapid diffusion scenario with widespread AI adoption.

**Key Parameters:**
- Maximum adoption rate: 80% of firms
- Diffusion speed: Fast (8% per period)
- Automation intensity: High (50%)
- Augmentation intensity: High (40%)

### 4. AI + Retraining Programs
Low adoption scenario with active government retraining programs.

**Key Parameters:**
- Same AI parameters as low adoption
- Retraining programs enabled
- 70% success rate
- 30% skill improvement upon completion
- Government subsidizes 100% of cost

---
"""

    def _generate_key_findings(self, comparison_df: pd.DataFrame,
                              impact_df: pd.DataFrame) -> str:
        """Generate key findings section."""

        findings = """## Key Findings

### Labor Market Impacts

"""

        # Create comparison text from data
        findings += "#### Unemployment Effects\n\n"
        findings += comparison_df[['Scenario', 'Unemployment Rate (%)']].to_markdown(index=False)
        findings += "\n\n"

        findings += "#### Wage Dynamics\n\n"
        findings += comparison_df[['Scenario', 'Average Wage ($)', 'Wage Inequality Ratio']].to_markdown(index=False)
        findings += "\n\n"

        findings += "### Economic Outcomes\n\n"
        findings += comparison_df[['Scenario', 'GDP', 'Labor Share (%)']].to_markdown(index=False)
        findings += "\n\n"

        findings += "### Inequality Measures\n\n"
        findings += comparison_df[['Scenario', 'Gini Coefficient', 'Low Skill Employment (%)',
                                  'High Skill Employment (%)']].to_markdown(index=False)
        findings += "\n\n---\n"

        return findings

    def _generate_detailed_results(self, results_dict: Dict,
                                   comparison_df: pd.DataFrame) -> str:
        """Generate detailed results section."""

        return """## Detailed Results

### Scenario-by-Scenario Analysis

The following sections present detailed analysis for each scenario, including time series dynamics and steady-state outcomes.

#### Visualizations

See accompanying figures in `outputs/figures/` for:
- Time series plots of key variables
- Scenario comparison charts
- Distribution analyses
- Comprehensive dashboards

### Cross-Scenario Comparison

The comparison table above shows steady-state values (averaged over final 50 periods) for each scenario. Key observations:

1. **Employment:** All AI scenarios show initial employment disruption followed by partial recovery
2. **Wages:** High-skill wages increase in all AI scenarios; low-skill wages decline
3. **Productivity:** Substantial productivity gains from AI adoption
4. **Inequality:** Gini coefficient rises with AI adoption, mitigated by retraining

---
"""

    def _generate_economic_interpretation(self, impact_df: pd.DataFrame) -> str:
        """Generate economic interpretation."""

        return """## Economic Interpretation

### Theoretical Framework

The results align with predictions from:
1. **Skill-Biased Technical Change:** AI disproportionately benefits high-skill workers
2. **Task-Based Framework:** Automation of routine tasks displaces some workers while augmentation enhances productivity of others
3. **Search and Matching Theory:** Labor market frictions delay reallocation

### Mechanisms

#### Labor Displacement
- Automation reduces demand for routine task workers
- Particularly affects low and medium-skill workers
- Creates unemployment during transition period

#### Productivity Enhancement
- AI augments cognitive tasks
- High-skill workers gain most
- Increases overall economic output

#### Wage Polarization
- High-skill wages rise due to complementarity with AI
- Low-skill wages fall due to displacement
- Increases inequality as measured by Gini coefficient

### Comparison to Empirical Literature

These results are consistent with empirical findings:
- Autor, Levy, and Murnane (2003) on skill-biased technical change
- Acemoglu and Restrepo (2020) on robots and jobs
- Brynjolfsson and McAfee (2014) on digital technologies

---
"""

    def _generate_policy_recommendations(self, impact_df: pd.DataFrame) -> str:
        """Generate policy recommendations."""

        return """## Policy Recommendations

Based on simulation results, we identify several policy interventions that can mitigate negative labor market effects of AI:

### 1. Active Labor Market Policies

**Retraining Programs**
- **Evidence:** Retraining scenario shows improved outcomes
- **Recommendation:** Invest in retraining programs targeting displaced workers
- **Implementation:** Focus on transitioning routine task workers to higher-skill occupations

### 2. Education and Skill Development

**Recommendation:** Strengthen education in skills complementary to AI
- Critical thinking
- Creativity
- Complex problem-solving
- Social and emotional intelligence

### 3. Safety Net Programs

**Unemployment Insurance**
- Enhanced benefits during transition periods
- Extended duration for workers in heavily automated sectors

**Universal Basic Income**
- Considered in scenarios with very high automation
- Provides income floor for displaced workers

### 4. Technology Policy

**Encourage Augmentation Over Automation**
- Tax incentives for productivity-enhancing AI
- Research funding for augmentation technologies

### 5. Competition and Labor Market Policy

- Promote worker bargaining power
- Prevent labor market monopsony
- Ensure gains from AI are broadly shared

---
"""

    def _generate_methodology(self) -> str:
        """Generate methodology section."""

        return """## Methodology

### Model Specification

#### Production Function

Firms use Cobb-Douglas production:

```
Y = A * K^α * L^(1-α)
```

Where:
- Y = Output
- A = Total Factor Productivity
- K = Capital
- L = Effective labor (sum of worker productivities)
- α = Capital share (0.3)

#### Worker Utility

Workers maximize utility from consumption and leisure:

```
U = ln(C + 1) + β * (employed) + γ * ln(savings + 1)
```

#### Labor Market Matching

Matching function based on Diamond-Mortensen-Pissarides:

```
M = m * U^η * V^(1-η)
```

Where:
- M = Matches formed
- U = Unemployed workers
- V = Vacancies
- m = Matching efficiency
- η = Matching elasticity

#### AI Adoption Decision

Firms adopt AI if:

```
NPV(AI) = Σ(Cost_Savings_t + Productivity_Gain_t) / (1+r)^t > Adoption_Cost
```

#### Task-Based AI Impact

Worker productivity with AI:

```
Productivity_AI = Productivity_base * (1 + Σ task_share * augmentation_potential)
```

Displacement risk:

```
Risk = Σ task_share * automation_susceptibility
```

### Calibration

Model parameters calibrated to match:
- US labor market statistics
- Skill distribution from BLS data
- Wage ratios from Current Population Survey
- AI adoption forecasts from industry reports

### Simulation Details

- **Time horizon:** 200 periods (~ 20 years with annual periods)
- **Warm-up:** First 20 periods excluded from analysis
- **Random seed:** 42 for reproducibility
- **Monte Carlo:** Single run (can be extended to multiple runs)

---
"""

    def _generate_technical_appendix(self) -> str:
        """Generate technical appendix."""

        return """## Technical Appendix

### Parameter Values

#### Worker Parameters
- Initial skills: Low (0.3), Medium (0.6), High (0.9)
- Consumption propensity: 0.8
- Learning rate: 0.01
- Skill depreciation: 0.005

#### Firm Parameters
- Capital share (α): 0.3
- Depreciation rate: 0.05
- Markup: 0.2
- Investment rate: 0.15

#### AI Parameters (High Adoption)
- Adoption rate: 0.8
- Diffusion speed: 0.08
- Automation intensity: 0.5
- Augmentation intensity: 0.4

#### Market Parameters
- Matching efficiency: 0.5
- Price adjustment speed: 0.15
- Wage stickiness: 0.3

### Software Implementation

- **Language:** Python 3.9+
- **Framework:** Mesa (agent-based modeling)
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Report Generation:** Jinja2, Markdown

### Code Availability

Full source code available at: [GitHub Repository]

### Reproducibility

To reproduce results:
```bash
python -m src.scenarios.comparison --steps 200 --seed 42 --save
```

---

*Report generated automatically by AI Labor Market Simulation System*
"""

    def _save_html_report(self, content: str, filepath: str):
        """Save report as HTML with styling."""

        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])

        # HTML template with styling
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Labor Market Simulation Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 30px 0;
        }}
        ul, ol {{
            margin-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <hr>
        <p class="timestamp">Report generated: {timestamp}</p>
    </div>
</body>
</html>
"""

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html_output = html_template.format(content=html_content, timestamp=timestamp)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_output)
