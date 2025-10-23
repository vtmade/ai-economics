"""
Scenario Runner

Runs individual scenarios and manages simulation execution.
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

        self.scenarios = {
            'baseline': self._get_baseline_config,
            'low_adoption': self._get_low_adoption_config,
            'high_adoption': self._get_high_adoption_config,
            'retraining': self._get_retraining_config,
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

    def _get_baseline_config(self) -> Dict:
        """Baseline scenario: No AI adoption."""
        return {
            'scenario_description': 'Baseline scenario with no AI adoption (control)',
            'ai_adoption': False
        }

    def _get_low_adoption_config(self) -> Dict:
        """Low AI adoption scenario."""
        return {
            'scenario_description': 'Conservative AI diffusion with low adoption rate',
            'ai_adoption': True,
            'adoption_rate': 0.3,
            'diffusion_speed': 0.02
        }

    def _get_high_adoption_config(self) -> Dict:
        """High AI adoption scenario."""
        return {
            'scenario_description': 'Rapid AI diffusion with high adoption rate',
            'ai_adoption': True,
            'adoption_rate': 0.8,
            'diffusion_speed': 0.08
        }

    def _get_retraining_config(self) -> Dict:
        """AI adoption with government retraining programs."""
        return {
            'scenario_description': 'Low AI adoption with active government retraining programs',
            'ai_adoption': True,
            'adoption_rate': 0.3,
            'diffusion_speed': 0.02,
            'retraining_enabled': True
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

    parser = argparse.ArgumentParser(description='Run AI Labor Market Simulation')
    parser.add_argument('scenario', choices=['baseline', 'low_adoption', 'high_adoption',
                                            'retraining', 'custom'],
                       help='Scenario to run')
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
