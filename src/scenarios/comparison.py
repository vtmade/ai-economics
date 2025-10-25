"""
Scenario Comparison - Research-Based Scenarios

Runs and compares research-based scenarios from 2023-2025 AI labor market studies.

Author: Vinay Thakur
Date: October 25, 2025
"""

import numpy as np
import pandas as pd
from typing import Dict, List
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.scenarios.runner import ScenarioRunner


class ScenarioComparison:
    """
    Compares results across multiple scenarios.
    """

    def __init__(self, random_seed=42):
        """
        Initialize scenario comparison.

        Args:
            random_seed: Random seed for reproducibility
        """
        self.runner = ScenarioRunner(random_seed)
        # Research-based scenarios for comparison
        self.scenarios_to_run = [
            'conservative_gradual',    # Epoch AI: 20-year timeline
            'mckinsey_baseline',        # McKinsey: Moderate 2030 effects
            'tbi_aggressive',           # TBI: Rapid displacement
            'anthropic_policy'          # Anthropic: Comprehensive policy response
            # 'rand_empirical'          # Optional: RAND data-calibrated
        ]
        self.results = {}

    def run_all_scenarios(self, steps: int = 200, num_workers: int = 100,
                         num_firms: int = 20) -> Dict:
        """
        Run all comparison scenarios.

        Args:
            steps: Number of simulation steps
            num_workers: Number of worker agents
            num_firms: Number of firm agents

        Returns:
            Dict of scenario results
        """
        print(f"\n{'#'*60}")
        print("RUNNING MULTI-SCENARIO COMPARISON")
        print(f"{'#'*60}\n")

        for scenario_name in self.scenarios_to_run:
            results = self.runner.run_scenario(
                scenario_name=scenario_name,
                steps=steps,
                num_workers=num_workers,
                num_firms=num_firms
            )
            self.results[scenario_name] = results

        print(f"\n{'#'*60}")
        print("ALL SCENARIOS COMPLETE")
        print(f"{'#'*60}\n")

        return self.results

    def create_comparison_table(self) -> pd.DataFrame:
        """
        Create comparison table of key metrics across scenarios.

        Returns:
            DataFrame with comparison statistics
        """
        if not self.results:
            raise ValueError("No results available. Run scenarios first.")

        comparison_data = []

        for scenario_name, result in self.results.items():
            summary = result['summary']

            row = {
                'Scenario': scenario_name.replace('_', ' ').title(),
                'Unemployment Rate (%)': summary['avg_unemployment_rate'] * 100,
                'Average Wage ($)': summary['avg_wage'],
                'Gini Coefficient': summary['final_gini'],
                'AI Adoption Rate (%)': summary['final_ai_adoption'] * 100,
                'GDP': summary['avg_gdp'],
                'Labor Share (%)': summary['labor_share'] * 100,
                'Wage Inequality Ratio': summary['wage_inequality'],
                'Low Skill Employment (%)': summary['employment_by_skill']['low'] * 100,
                'High Skill Employment (%)': summary['employment_by_skill']['high'] * 100
            }

            comparison_data.append(row)

        return pd.DataFrame(comparison_data)

    def calculate_impacts(self, baseline_name: str = 'conservative_gradual') -> pd.DataFrame:
        """
        Calculate impacts relative to baseline scenario.

        Args:
            baseline_name: Name of baseline scenario (default: conservative_gradual - Epoch AI)

        Returns:
            DataFrame with percentage changes relative to baseline
        """
        if baseline_name not in self.results:
            raise ValueError(f"Baseline scenario '{baseline_name}' not found")

        baseline_summary = self.results[baseline_name]['summary']
        impact_data = []

        for scenario_name, result in self.results.items():
            if scenario_name == baseline_name:
                continue

            summary = result['summary']

            # Calculate percentage changes
            row = {
                'Scenario': scenario_name.replace('_', ' ').title(),
                'Δ Unemployment (pp)': (summary['avg_unemployment_rate'] -
                                       baseline_summary['avg_unemployment_rate']) * 100,
                'Δ Wage (%)': ((summary['avg_wage'] / baseline_summary['avg_wage']) - 1) * 100
                              if baseline_summary['avg_wage'] > 0 else 0,
                'Δ Gini': summary['final_gini'] - baseline_summary['final_gini'],
                'Δ GDP (%)': ((summary['avg_gdp'] / baseline_summary['avg_gdp']) - 1) * 100
                            if baseline_summary['avg_gdp'] > 0 else 0,
                'Δ Labor Share (pp)': (summary['labor_share'] -
                                      baseline_summary['labor_share']) * 100,
                'Δ Wage Inequality': summary['wage_inequality'] - baseline_summary['wage_inequality']
            }

            impact_data.append(row)

        return pd.DataFrame(impact_data)

    def save_comparison(self, output_dir: str = 'outputs/data'):
        """
        Save comparison results.

        Args:
            output_dir: Directory to save results
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save comparison table
        comparison_table = self.create_comparison_table()
        comparison_table.to_csv(
            os.path.join(output_dir, 'scenario_comparison.csv'),
            index=False
        )

        # Save impact analysis
        impact_table = self.calculate_impacts()
        impact_table.to_csv(
            os.path.join(output_dir, 'scenario_impacts.csv'),
            index=False
        )

        # Save all time series data
        for scenario_name, result in self.results.items():
            result['results'].to_csv(
                os.path.join(output_dir, f'{scenario_name}_timeseries.csv'),
                index=True
            )

        print(f"\nComparison results saved to {output_dir}")

    def print_comparison_summary(self):
        """Print formatted comparison summary to console."""
        print(f"\n{'='*80}")
        print("SCENARIO COMPARISON SUMMARY")
        print(f"{'='*80}\n")

        # Comparison table
        comparison_table = self.create_comparison_table()
        print(comparison_table.to_string(index=False))

        print(f"\n{'='*80}")
        print("IMPACTS RELATIVE TO BASELINE")
        print(f"{'='*80}\n")

        # Impact table
        impact_table = self.calculate_impacts()
        print(impact_table.to_string(index=False))

        print(f"\n{'='*80}\n")


def main():
    """Run scenario comparison from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Compare AI Labor Market Scenarios')
    parser.add_argument('--steps', type=int, default=200,
                       help='Number of simulation steps')
    parser.add_argument('--workers', type=int, default=100,
                       help='Number of workers')
    parser.add_argument('--firms', type=int, default=20,
                       help='Number of firms')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    parser.add_argument('--save', action='store_true',
                       help='Save results to disk')

    args = parser.parse_args()

    # Run comparison
    comparison = ScenarioComparison(random_seed=args.seed)
    comparison.run_all_scenarios(
        steps=args.steps,
        num_workers=args.workers,
        num_firms=args.firms
    )

    # Print summary
    comparison.print_comparison_summary()

    # Save if requested
    if args.save:
        comparison.save_comparison()


if __name__ == '__main__':
    main()
