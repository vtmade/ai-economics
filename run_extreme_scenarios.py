#!/usr/bin/env python3
"""
Run Extreme AI Economics Scenarios

This script runs extreme scenarios exploring:
1. Mass labor displacement (95% AI adoption, 85% automation)
2. Technological singularity (98% adoption, 95% automation)
3. Income concentration and consumption collapse dynamics
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.scenarios.runner import ScenarioRunner
import pandas as pd
import numpy as np

def main():
    print("="*80)
    print(" EXTREME AI ECONOMICS SIMULATION")
    print(" Studying Mass Displacement, Income Concentration, and Consumption Collapse")
    print("="*80)
    print()

    runner = ScenarioRunner(random_seed=42)

    # Scenarios to run
    scenarios = [
        'baseline',
        'high_adoption',
        'extreme_displacement',
        'technological_singularity'
    ]

    results_dict = {}

    # Run each scenario
    for scenario in scenarios:
        print(f"\n{'='*80}")
        print(f"SCENARIO: {scenario.upper().replace('_', ' ')}")
        print(f"{'='*80}\n")

        results = runner.run_scenario(
            scenario_name=scenario,
            steps=250,  # Longer simulation to see extreme effects
            num_workers=150,  # More workers to see distributional effects
            num_firms=25      # More firms
        )

        results_dict[scenario] = results

        # Print final state
        df = results['results']
        print(f"\nFINAL STATE (Period 250):")
        print(f"  Unemployment Rate: {df['Unemployment Rate'].iloc[-1]:.1%}")
        print(f"  Average Wage: ${df['Average Wage'].iloc[-1]:.2f}")
        print(f"  GDP: ${df['GDP'].iloc[-1]:.2f}")
        print(f"  Gini Coefficient: {df['Gini Coefficient'].iloc[-1]:.3f}")
        print(f"  Labor Share: {df['Labor Share'].iloc[-1]:.1%}")
        print(f"  Capital Share: {df['Capital Share'].iloc[-1]:.1%}")
        print(f"  AI Adoption: {df['AI Adoption Rate'].iloc[-1]:.1%}")
        print(f"  Top 10% Income Share: {df['Top 10% Income Share'].iloc[-1]:.1%}")
        print(f"  Total Consumption: ${df['Total Consumption'].iloc[-1]:.2f}")
        print(f"  Median Savings: ${df['Median Worker Savings'].iloc[-1]:.2f}")

    # Create comparison table
    print(f"\n\n{'='*80}")
    print("SCENARIO COMPARISON - FINAL PERIOD")
    print(f"{'='*80}\n")

    comparison_data = []
    for scenario, results in results_dict.items():
        df = results['results']
        last = df.iloc[-1]

        comparison_data.append({
            'Scenario': scenario.replace('_', ' ').title(),
            'Unemployment': f"{last['Unemployment Rate']:.1%}",
            'Avg Wage': f"${last['Average Wage']:.0f}",
            'GDP': f"${last['GDP']:.0f}",
            'Gini': f"{last['Gini Coefficient']:.3f}",
            'Labor Share': f"{last['Labor Share']:.1%}",
            'AI Adoption': f"{last['AI Adoption Rate']:.1%}",
            'Top 10% Share': f"{last['Top 10% Income Share']:.1%}",
            'Consumption': f"${last['Total Consumption']:.0f}"
        })

    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))

    # Save results
    os.makedirs('outputs/extreme_scenarios', exist_ok=True)

    for scenario, results in results_dict.items():
        results['results'].to_csv(
            f'outputs/extreme_scenarios/{scenario}_timeseries.csv'
        )

    comparison_df.to_csv('outputs/extreme_scenarios/comparison.csv', index=False)

    print(f"\n\nResults saved to outputs/extreme_scenarios/")
    print(f"{'='*80}\n")

    return results_dict

if __name__ == '__main__':
    results = main()
