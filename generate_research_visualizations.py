"""
Generate Research-Based Visualizations

Creates publication-quality visualizations for research-backed scenarios.

Author: Vinay Thakur
Date: October 25, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

# Load data
data_dir = 'outputs/data'
scenarios = {
    'Conservative Gradual\n(Epoch AI)': pd.read_csv(f'{data_dir}/conservative_gradual_timeseries.csv', index_col=0),
    'McKinsey Baseline\n(Moderate 2030)': pd.read_csv(f'{data_dir}/mckinsey_baseline_timeseries.csv', index_col=0),
    'TBI Aggressive\n(Rapid Displacement)': pd.read_csv(f'{data_dir}/tbi_aggressive_timeseries.csv', index_col=0),
    'Anthropic Policy\n(Comprehensive)': pd.read_csv(f'{data_dir}/anthropic_policy_timeseries.csv', index_col=0)
}

# Color scheme
colors = {
    'Conservative Gradual\n(Epoch AI)': '#2E86AB',  # Blue
    'McKinsey Baseline\n(Moderate 2030)': '#A23B72',  # Purple
    'TBI Aggressive\n(Rapid Displacement)': '#F18F01',  # Orange
    'Anthropic Policy\n(Comprehensive)': '#06A77D'  # Green
}

os.makedirs('outputs/figures', exist_ok=True)

# 1. Multi-panel comparison
fig, axes = plt.subplots(3, 2, figsize=(16, 12))
fig.suptitle('Research-Based AI Labor Market Scenarios: Comprehensive Comparison',
             fontsize=16, fontweight='bold', y=0.995)

# Unemployment Rate
ax = axes[0, 0]
for name, df in scenarios.items():
    ax.plot(df.index, df['Unemployment Rate'] * 100, label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step (1 step ≈ 0.1 years)')
ax.set_ylabel('Unemployment Rate (%)')
ax.set_title('Unemployment Rate Over Time')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# Average Wage
ax = axes[0, 1]
for name, df in scenarios.items():
    ax.plot(df.index, df['Average Wage'], label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step')
ax.set_ylabel('Average Wage ($)')
ax.set_title('Average Wage Trajectory')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# GDP
ax = axes[1, 0]
for name, df in scenarios.items():
    ax.plot(df.index, df['GDP'], label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step')
ax.set_ylabel('GDP')
ax.set_title('GDP Growth')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# AI Adoption Rate
ax = axes[1, 1]
for name, df in scenarios.items():
    ax.plot(df.index, df['AI Adoption Rate'] * 100, label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step')
ax.set_ylabel('AI Adoption Rate (%)')
ax.set_title('AI Technology Adoption')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# Gini Coefficient
ax = axes[2, 0]
for name, df in scenarios.items():
    ax.plot(df.index, df['Gini Coefficient'], label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step')
ax.set_ylabel('Gini Coefficient')
ax.set_title('Income Inequality (Gini)')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# Labor Share
ax = axes[2, 1]
for name, df in scenarios.items():
    ax.plot(df.index, df['Labor Share'] * 100, label=name,
            color=colors[name], linewidth=2.5, alpha=0.9)
ax.set_xlabel('Time Step')
ax.set_ylabel('Labor Share (%)')
ax.set_title('Labor Share of Income')
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/figures/research_scenarios_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created: research_scenarios_comparison.png")
plt.close()

# 2. Wage by skill level
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Wage Dynamics by Skill Level - Research-Based Scenarios',
             fontsize=16, fontweight='bold')

skill_levels = ['Low Skill Wage', 'Medium Skill Wage', 'High Skill Wage']
skill_colors = ['#E63946', '#F77F00', '#06A77D']

for idx, (name, df) in enumerate(scenarios.items()):
    ax = axes[idx // 2, idx % 2]
    for skill, color in zip(skill_levels, skill_colors):
        if skill in df.columns:
            ax.plot(df.index, df[skill], label=skill, color=color, linewidth=2.5, alpha=0.8)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Wage ($)')
    ax.set_title(name)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/figures/wage_by_skill_research.png', dpi=300, bbox_inches='tight')
print("✓ Created: wage_by_skill_research.png")
plt.close()

# 3. Final outcomes comparison (bar chart)
comparison_df = pd.read_csv('outputs/data/scenario_comparison.csv')

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Final Outcomes: Research-Based Scenario Comparison',
             fontsize=16, fontweight='bold')

metrics = [
    ('Unemployment Rate (%)', 'Unemployment\nRate (%)'),
    ('Average Wage ($)', 'Average\nWage ($)'),
    ('Gini Coefficient', 'Gini\nCoefficient'),
    ('GDP', 'GDP'),
    ('Labor Share (%)', 'Labor Share\n(%)'),
    ('Wage Inequality Ratio', 'Wage\nInequality')
]

for idx, (col, label) in enumerate(metrics):
    ax = axes[idx // 3, idx % 3]
    scenario_names = [s.split('\n')[0] for s in comparison_df['Scenario']]
    bars = ax.bar(range(len(scenario_names)), comparison_df[col],
                   color=[colors[k] for k in scenarios.keys()], alpha=0.8, edgecolor='black')
    ax.set_ylabel(label)
    ax.set_title(label)
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=45, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('outputs/figures/final_outcomes_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created: final_outcomes_comparison.png")
plt.close()

# 4. Impact relative to baseline (bar chart)
impacts_df = pd.read_csv('outputs/data/scenario_impacts.csv')

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Impacts Relative to Conservative Gradual Baseline',
             fontsize=16, fontweight='bold')

impact_metrics = [
    ('Δ Unemployment (pp)', 'Unemployment\nChange (pp)'),
    ('Δ Wage (%)', 'Wage\nChange (%)'),
    ('Δ Gini', 'Gini\nChange'),
    ('Δ GDP (%)', 'GDP\nChange (%)'),
    ('Δ Labor Share (pp)', 'Labor Share\nChange (pp)'),
    ('Δ Wage Inequality', 'Wage Inequality\nChange')
]

for idx, (col, label) in enumerate(impact_metrics):
    ax = axes[idx // 3, idx % 3]
    scenario_names = [s.split('\n')[0] for s in impacts_df['Scenario']]

    # Color bars based on positive/negative
    bar_colors = ['#06A77D' if x >= 0 else '#E63946' for x in impacts_df[col]]

    bars = ax.bar(range(len(scenario_names)), impacts_df[col],
                   color=bar_colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel(label)
    ax.set_title(label)
    ax.set_xticks(range(len(scenario_names)))
    ax.set_xticklabels(scenario_names, rotation=45, ha='right', fontsize=9)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        va = 'bottom' if height >= 0 else 'top'
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:+.1f}',
                ha='center', va=va, fontsize=9)

plt.tight_layout()
plt.savefig('outputs/figures/impacts_relative_to_baseline.png', dpi=300, bbox_inches='tight')
print("✓ Created: impacts_relative_to_baseline.png")
plt.close()

print("\n" + "="*60)
print("All visualizations generated successfully!")
print("="*60)
print("\nGenerated files:")
print("  - outputs/figures/research_scenarios_comparison.png")
print("  - outputs/figures/wage_by_skill_research.png")
print("  - outputs/figures/final_outcomes_comparison.png")
print("  - outputs/figures/impacts_relative_to_baseline.png")
