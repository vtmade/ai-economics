"""
Scenario Runner - Research-Based Scenarios

Runs individual scenarios based on 2023-2025 research findings:
- McKinsey Global Institute (2023)
- Anthropic (2024)
- RAND Corporation (2024-2025)
- Tony Blair Institute (2024)
- Epoch AI (2024-2025)

See docs/RESEARCH_SYNTHESIS.md and docs/RESEARCH_BASED_SCENARIOS.md for details.

Author: Vinay Thakur
Date: October 25, 2025
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.model import LaborMarketModel
import config


class ScenarioRunner:
    """
    Manages execution of individual simulation scenarios.
    """

    def __init__(self, random_seed=None):
        """
        Initialize scenario runner.

        Args:
            random_seed: Random seed for reproducibility
        """
        self.random_seed = random_seed or config.RANDOM_SEED
        np.random.seed(self.random_seed)

        # Research-based scenarios
        self.scenarios = {
            'conservative_gradual': self._get_conservative_gradual_config,
            'mckinsey_baseline': self._get_mckinsey_baseline_config,
            'tbi_aggressive': self._get_tbi_aggressive_config,
            'anthropic_policy': self._get_anthropic_policy_config,
            'rand_empirical': self._get_rand_empirical_config,
            'custom': self._get_custom_config
        }

    def run_scenario(self, scenario_name: str, steps: int = None,
                    num_workers: int = None, num_firms: int = None,
                    custom_params: Dict = None) -> Dict:
        """
        Run a single scenario.

        Args:
            scenario_name: Name of scenario ('baseline', 'low_adoption', etc.)
            steps: Number of simulation steps
            num_workers: Number of worker agents
            num_firms: Number of firm agents
            custom_params: Custom parameters for scenario

        Returns:
            Dict containing model and results
        """
        print(f"\n{'='*60}")
        print(f"Running Scenario: {scenario_name.upper()}")
        print(f"{'='*60}")

        # Get scenario configuration
        if scenario_name in self.scenarios:
            scenario_config = self.scenarios[scenario_name]()
        else:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        # Apply custom parameters
        if custom_params:
            scenario_config.update(custom_params)

        # Create model
        model = LaborMarketModel(
            scenario_name=scenario_name,
            num_workers=num_workers,
            num_firms=num_firms,
            custom_config=scenario_config
        )

        # Run simulation
        steps = steps or config.DEFAULT_STEPS
        print(f"Running {steps} time steps...")

        for step in range(steps):
            model.step()

            # Progress indicator
            if (step + 1) % 50 == 0:
                print(f"  Step {step + 1}/{steps} - "
                      f"Unemployment: {model.labor_market.unemployment_rate:.2%}, "
                      f"AI Adoption: {model._calculate_ai_adoption_rate():.2%}")

        print(f"\nScenario complete!")

        # Get results
        results_df = model.get_results()
        summary_stats = model.get_summary_statistics()

        return {
            'model': model,
            'results': results_df,
            'summary': summary_stats,
            'scenario_name': scenario_name,
            'config': scenario_config
        }

    def _get_conservative_gradual_config(self) -> Dict:
        """
        Scenario 1: Conservative Gradual (Epoch AI 20-Year Timeline)

        Based on Epoch AI (2024-2025) conservative compute scaling assumptions.
        - Full automation timeline: 20+ years (median estimate)
        - 34% of job tasks remotable
        - Economy doubles within 20 years (conservative)
        """
        return {
            'scenario_description': 'Conservative gradual adoption - Epoch AI 20-year timeline',
            'ai_adoption': True,
            **config.AI_CONFIG['conservative_gradual']
        }

    def _get_mckinsey_baseline_config(self) -> Dict:
        """
        Scenario 2: McKinsey Baseline (Moderate 2030 Effects)

        Based on McKinsey Global Institute (June 2023).
        - 60-70% work time automatable
        - $2.6-4.4T annual economic impact
        - 0.5-0.9pp productivity growth through 2030
        - 34pp increase in expertise automation
        """
        return {
            'scenario_description': 'McKinsey baseline - Moderate 2030 effects',
            'ai_adoption': True,
            **config.AI_CONFIG['mckinsey_baseline']
        }

    def _get_tbi_aggressive_config(self) -> Dict:
        """
        Scenario 3: TBI Aggressive Displacement (Rapid 2025-2030)

        Based on Tony Blair Institute (November 2024).
        - +180K unemployment by 2030 (UK)
        - Peak displacement: 60K-275K jobs/year
        - +6% GDP by 2035
        - 23% workforce time savings
        """
        return {
            'scenario_description': 'TBI aggressive - Rapid displacement 2025-2030',
            'ai_adoption': True,
            **config.AI_CONFIG['tbi_aggressive']
        }

    def _get_anthropic_policy_config(self) -> Dict:
        """
        Scenario 4: Anthropic Comprehensive Policy Response

        Based on Anthropic (2024) 9-category graduated policy framework.
        - $10K/year per trainee workforce training grants
        - ~$700M annually for Automation Adjustment Assistance
        - 3-stage response: workforce dev → fiscal support → wealth redistribution
        - Users increasingly delegate full tasks (faster displacement)
        """
        return {
            'scenario_description': 'Anthropic comprehensive policy - Graduated response',
            'ai_adoption': True,
            **config.AI_CONFIG['anthropic_policy']
        }

    def _get_rand_empirical_config(self) -> Dict:
        """
        Scenario 5: RAND Empirical Evidence (Data-Calibrated)

        Based on RAND Corporation (2024-2025) empirical findings.
        - +$7K per capita GDP by 2035
        - 0.57 correlation between AI adoption and unemployment
        - 22-25 year-olds most affected
        - Software dev, customer service, clerical primary occupations
        """
        return {
            'scenario_description': 'RAND empirical - Data-calibrated projection',
            'ai_adoption': True,
            **config.AI_CONFIG['rand_empirical']
        }

    def _get_custom_config(self) -> Dict:
        """Custom scenario with user-defined parameters."""
        return {
            'scenario_description': 'Custom scenario with user-defined parameters'
        }

    def save_results(self, results: Dict, output_dir: str = 'outputs/data'):
        """
        Save scenario results to disk.

        Args:
            results: Results dictionary from run_scenario
            output_dir: Directory to save results
        """
        os.makedirs(output_dir, exist_ok=True)

        scenario_name = results['scenario_name']

        # Save time series data
        results['results'].to_csv(
            os.path.join(output_dir, f'{scenario_name}_timeseries.csv'),
            index=True
        )

        # Save summary statistics
        summary_df = pd.DataFrame([results['summary']])
        summary_df.to_csv(
            os.path.join(output_dir, f'{scenario_name}_summary.csv'),
            index=False
        )

        print(f"\nResults saved to {output_dir}")


def main():
    """Run a single scenario from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Run AI Labor Market Simulation - Research-Based Scenarios')
    parser.add_argument('scenario',
                       choices=['conservative_gradual', 'mckinsey_baseline', 'tbi_aggressive',
                               'anthropic_policy', 'rand_empirical', 'custom'],
                       help='Research-based scenario to run')
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

    # Run scenario
    runner = ScenarioRunner(random_seed=args.seed)
    results = runner.run_scenario(
        scenario_name=args.scenario,
        steps=args.steps,
        num_workers=args.workers,
        num_firms=args.firms
    )

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")
    for key, value in results['summary'].items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v:.4f}")
        else:
            print(f"{key}: {value:.4f}")

    # Save if requested
    if args.save:
        runner.save_results(results)


if __name__ == '__main__':
    main()
