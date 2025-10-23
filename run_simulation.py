#!/usr/bin/env python3
"""
Main Entry Point for AI Labor Market Simulation

This script provides a command-line interface for running simulations,
comparing scenarios, and generating reports.

Usage:
    python run_simulation.py --help
    python run_simulation.py --scenario baseline --steps 200
    python run_simulation.py --compare-all --visualize --report
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.scenarios.runner import ScenarioRunner
from src.scenarios.comparison import ScenarioComparison
from src.visualization.plots import SimulationVisualizer
from src.reports.report_generator import ReportGenerator
import config


def main():
    parser = argparse.ArgumentParser(
        description='AI Labor Market Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single scenario
  python run_simulation.py --scenario baseline --steps 200

  # Compare all scenarios
  python run_simulation.py --compare-all

  # Run with visualization and report
  python run_simulation.py --compare-all --visualize --report

  # Custom scenario
  python run_simulation.py --scenario custom --workers 200 --firms 40

  # Save results to disk
  python run_simulation.py --scenario high_adoption --save
        """
    )

    # Scenario selection
    parser.add_argument('--scenario', choices=['baseline', 'low_adoption',
                                              'high_adoption', 'retraining', 'custom'],
                       help='Scenario to run')
    parser.add_argument('--compare-all', action='store_true',
                       help='Compare all predefined scenarios')

    # Simulation parameters
    parser.add_argument('--steps', type=int, default=200,
                       help='Number of simulation steps (default: 200)')
    parser.add_argument('--workers', type=int, default=100,
                       help='Number of worker agents (default: 100)')
    parser.add_argument('--firms', type=int, default=20,
                       help='Number of firm agents (default: 20)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')

    # Output options
    parser.add_argument('--save', action='store_true',
                       help='Save results to disk')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualizations')
    parser.add_argument('--report', action='store_true',
                       help='Generate comprehensive HTML report')
    parser.add_argument('--output-dir', default='outputs',
                       help='Output directory (default: outputs)')

    # Display options
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress output')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed output')

    args = parser.parse_args()

    # Validate arguments
    if not args.scenario and not args.compare_all:
        parser.error('Must specify either --scenario or --compare-all')

    # Set up output directories
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(f'{args.output_dir}/data', exist_ok=True)
    os.makedirs(f'{args.output_dir}/figures', exist_ok=True)
    os.makedirs(f'{args.output_dir}/reports', exist_ok=True)

    print("="*70)
    print(" AI LABOR MARKET ECONOMICS SIMULATION")
    print("="*70)
    print()

    if args.compare_all:
        # Run all scenarios comparison
        print("Running multi-scenario comparison...")
        print()

        comparison = ScenarioComparison(random_seed=args.seed)
        results_dict = comparison.run_all_scenarios(
            steps=args.steps,
            num_workers=args.workers,
            num_firms=args.firms
        )

        # Print summary
        comparison.print_comparison_summary()

        # Save results
        if args.save:
            comparison.save_comparison(output_dir=f'{args.output_dir}/data')
            print(f"\n✓ Results saved to {args.output_dir}/data/")

        # Generate visualizations
        if args.visualize:
            print("\nGenerating visualizations...")
            viz = SimulationVisualizer(output_dir=f'{args.output_dir}/figures')
            viz.create_all_visualizations(results_dict)
            print(f"✓ Visualizations saved to {args.output_dir}/figures/")

        # Generate report
        if args.report:
            print("\nGenerating comprehensive report...")
            comparison_table = comparison.create_comparison_table()
            impact_table = comparison.calculate_impacts()

            report_gen = ReportGenerator(output_dir=f'{args.output_dir}/reports')
            report_path = report_gen.generate_report(
                results_dict=results_dict,
                comparison_df=comparison_table,
                impact_df=impact_table,
                format='html'
            )
            print(f"✓ Report saved to {report_path}")

    else:
        # Run single scenario
        print(f"Running scenario: {args.scenario}")
        print(f"Parameters: {args.workers} workers, {args.firms} firms, {args.steps} steps")
        print()

        runner = ScenarioRunner(random_seed=args.seed)
        results = runner.run_scenario(
            scenario_name=args.scenario,
            steps=args.steps,
            num_workers=args.workers,
            num_firms=args.firms
        )

        # Print summary
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        for key, value in results['summary'].items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v:.4f}")
            else:
                print(f"{key}: {value:.4f}")

        # Save results
        if args.save:
            runner.save_results(results, output_dir=f'{args.output_dir}/data')
            print(f"\n✓ Results saved to {args.output_dir}/data/")

        # Generate visualizations
        if args.visualize:
            print("\nGenerating visualizations...")
            viz = SimulationVisualizer(output_dir=f'{args.output_dir}/figures')
            viz.plot_dashboard(results, save_name=f'dashboard_{args.scenario}.png')
            print(f"✓ Dashboard saved to {args.output_dir}/figures/")

    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
