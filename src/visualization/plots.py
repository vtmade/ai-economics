"""
Visualization Module

Creates publication-quality plots for analysis and reports.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10


class SimulationVisualizer:
    """
    Creates various plots for simulation analysis.
    """

    def __init__(self, output_dir: str = 'outputs/figures'):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save figures
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Color palette
        self.colors = sns.color_palette("Set2", 8)
        self.scenario_colors = {
            'baseline': self.colors[0],
            'low_adoption': self.colors[1],
            'high_adoption': self.colors[2],
            'retraining': self.colors[3],
            'custom': self.colors[4]
        }

    def plot_time_series(self, results: Dict, metrics: List[str],
                        title: str = None, save_name: str = None):
        """
        Plot time series of key metrics.

        Args:
            results: Results dictionary from scenario run
            metrics: List of metrics to plot
            title: Plot title
            save_name: Filename to save plot
        """
        df = results['results']
        scenario_name = results['scenario_name']

        n_metrics = len(metrics)
        fig, axes = plt.subplots(n_metrics, 1, figsize=(12, 4 * n_metrics))

        if n_metrics == 1:
            axes = [axes]

        for ax, metric in zip(axes, metrics):
            if metric in df.columns:
                ax.plot(df.index, df[metric], color=self.scenario_colors.get(scenario_name),
                       linewidth=2, label=metric)
                ax.set_xlabel('Time Step')
                ax.set_ylabel(metric)
                ax.set_title(f'{metric} Over Time')
                ax.grid(True, alpha=0.3)
                ax.legend()

        if title:
            fig.suptitle(title, fontsize=16, y=1.001)

        plt.tight_layout()

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig

    def plot_comparison(self, results_dict: Dict[str, Dict],
                       metric: str, title: str = None, save_name: str = None):
        """
        Compare a metric across multiple scenarios.

        Args:
            results_dict: Dictionary of scenario results
            metric: Metric to compare
            title: Plot title
            save_name: Filename to save plot
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        for scenario_name, results in results_dict.items():
            df = results['results']
            if metric in df.columns:
                ax.plot(df.index, df[metric],
                       color=self.scenario_colors.get(scenario_name),
                       linewidth=2, label=scenario_name.replace('_', ' ').title())

        ax.set_xlabel('Time Step', fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        ax.set_title(title or f'{metric} Comparison Across Scenarios', fontsize=14)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig

    def plot_dashboard(self, results: Dict, save_name: str = None):
        """
        Create a dashboard with multiple key metrics.

        Args:
            results: Results dictionary from scenario run
            save_name: Filename to save plot
        """
        df = results['results']
        scenario_name = results['scenario_name'].replace('_', ' ').title()

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. Unemployment Rate
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(df.index, df['Unemployment Rate'] * 100, color=self.colors[0], linewidth=2)
        ax1.set_title('Unemployment Rate', fontweight='bold')
        ax1.set_ylabel('Percent (%)')
        ax1.grid(True, alpha=0.3)

        # 2. Average Wage
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(df.index, df['Average Wage'], color=self.colors[1], linewidth=2)
        ax2.set_title('Average Wage', fontweight='bold')
        ax2.set_ylabel('Dollars ($)')
        ax2.grid(True, alpha=0.3)

        # 3. GDP
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.plot(df.index, df['GDP'], color=self.colors[2], linewidth=2)
        ax3.set_title('GDP', fontweight='bold')
        ax3.set_ylabel('Output')
        ax3.grid(True, alpha=0.3)

        # 4. Wages by Skill Level
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(df.index, df['Low Skill Wage'], label='Low Skill', linewidth=2)
        ax4.plot(df.index, df['Medium Skill Wage'], label='Medium Skill', linewidth=2)
        ax4.plot(df.index, df['High Skill Wage'], label='High Skill', linewidth=2)
        ax4.set_title('Wages by Skill Level', fontweight='bold')
        ax4.set_ylabel('Wage ($)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # 5. Gini Coefficient
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.plot(df.index, df['Gini Coefficient'], color=self.colors[3], linewidth=2)
        ax5.set_title('Income Inequality (Gini)', fontweight='bold')
        ax5.set_ylabel('Gini Coefficient')
        ax5.grid(True, alpha=0.3)

        # 6. AI Adoption Rate
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.plot(df.index, df['AI Adoption Rate'] * 100, color=self.colors[4], linewidth=2)
        ax6.set_title('AI Adoption Rate', fontweight='bold')
        ax6.set_ylabel('Percent (%)')
        ax6.grid(True, alpha=0.3)

        # 7. Employment by Skill
        ax7 = fig.add_subplot(gs[2, 0])
        ax7.plot(df.index, df['Low Skill Employment Rate'] * 100,
                label='Low Skill', linewidth=2)
        ax7.plot(df.index, df['Medium Skill Employment Rate'] * 100,
                label='Medium Skill', linewidth=2)
        ax7.plot(df.index, df['High Skill Employment Rate'] * 100,
                label='High Skill', linewidth=2)
        ax7.set_title('Employment Rate by Skill', fontweight='bold')
        ax7.set_xlabel('Time Step')
        ax7.set_ylabel('Percent (%)')
        ax7.legend()
        ax7.grid(True, alpha=0.3)

        # 8. Labor Share
        ax8 = fig.add_subplot(gs[2, 1])
        ax8.plot(df.index, df['Labor Share'] * 100, color=self.colors[5], linewidth=2)
        ax8.set_title('Labor Share of Income', fontweight='bold')
        ax8.set_xlabel('Time Step')
        ax8.set_ylabel('Percent (%)')
        ax8.grid(True, alpha=0.3)

        # 9. Average Productivity
        ax9 = fig.add_subplot(gs[2, 2])
        ax9.plot(df.index, df['Average Productivity'], color=self.colors[6], linewidth=2)
        ax9.set_title('Average Worker Productivity', fontweight='bold')
        ax9.set_xlabel('Time Step')
        ax9.set_ylabel('Productivity')
        ax9.grid(True, alpha=0.3)

        fig.suptitle(f'Simulation Dashboard: {scenario_name}',
                    fontsize=18, fontweight='bold', y=0.995)

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig

    def plot_comparison_bars(self, comparison_df: pd.DataFrame,
                            metrics: List[str], save_name: str = None):
        """
        Create bar charts comparing metrics across scenarios.

        Args:
            comparison_df: DataFrame with comparison statistics
            metrics: List of metrics to plot
            save_name: Filename to save plot
        """
        n_metrics = len(metrics)
        fig, axes = plt.subplots(1, n_metrics, figsize=(6 * n_metrics, 6))

        if n_metrics == 1:
            axes = [axes]

        for ax, metric in zip(axes, metrics):
            if metric in comparison_df.columns:
                scenarios = comparison_df['Scenario']
                values = comparison_df[metric]

                bars = ax.bar(range(len(scenarios)), values,
                             color=[self.scenario_colors.get(s.lower().replace(' ', '_'), self.colors[0])
                                   for s in scenarios])

                ax.set_xticks(range(len(scenarios)))
                ax.set_xticklabels(scenarios, rotation=45, ha='right')
                ax.set_ylabel(metric)
                ax.set_title(metric, fontweight='bold')
                ax.grid(True, axis='y', alpha=0.3)

                # Add value labels on bars
                for i, (bar, val) in enumerate(zip(bars, values)):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                           f'{val:.2f}',
                           ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig

    def plot_distribution(self, results: Dict, variable: str = 'wage',
                         save_name: str = None):
        """
        Plot distribution of a variable across agents.

        Args:
            results: Results dictionary
            variable: Variable to plot distribution of
            save_name: Filename to save plot
        """
        model = results['model']

        # Extract data from agents
        if variable == 'wage':
            from src.agents.worker import Worker
            workers = [a for a in model.schedule.agents if isinstance(a, Worker) and a.employed]
            data = [w.wage for w in workers]
            xlabel = 'Wage ($)'
        elif variable == 'skill':
            from src.agents.worker import Worker
            workers = [a for a in model.schedule.agents if isinstance(a, Worker)]
            data = [w.skill_value for w in workers]
            xlabel = 'Skill Level'
        elif variable == 'profit':
            from src.agents.firm import Firm
            firms = [a for a in model.schedule.agents if isinstance(a, Firm)]
            data = [f.profits for f in firms]
            xlabel = 'Profit ($)'
        else:
            raise ValueError(f"Unknown variable: {variable}")

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(data, bins=30, color=self.colors[0], alpha=0.7, edgecolor='black')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(f'Distribution of {variable.title()}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        # Add statistics
        mean_val = np.mean(data)
        median_val = np.median(data)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        ax.legend()

        plt.tight_layout()

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig

    def create_all_visualizations(self, results_dict: Dict[str, Dict]):
        """
        Create all standard visualizations for scenario comparison.

        Args:
            results_dict: Dictionary of scenario results
        """
        print("\nGenerating visualizations...")

        # 1. Individual dashboards for each scenario
        for scenario_name, results in results_dict.items():
            self.plot_dashboard(results, save_name=f'dashboard_{scenario_name}.png')

        # 2. Comparison plots for key metrics
        key_metrics = [
            'Unemployment Rate',
            'Average Wage',
            'Gini Coefficient',
            'GDP',
            'AI Adoption Rate',
            'Labor Share'
        ]

        for metric in key_metrics:
            safe_name = metric.lower().replace(' ', '_')
            self.plot_comparison(results_dict, metric,
                               title=f'{metric}: Scenario Comparison',
                               save_name=f'comparison_{safe_name}.png')

        # 3. Multi-panel comparison
        self.plot_multi_comparison(results_dict, save_name='multi_comparison.png')

        print(f"\nAll visualizations saved to {self.output_dir}/")

    def plot_multi_comparison(self, results_dict: Dict[str, Dict],
                             save_name: str = None):
        """
        Create multi-panel comparison figure.

        Args:
            results_dict: Dictionary of scenario results
            save_name: Filename to save plot
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()

        metrics = [
            ('Unemployment Rate', 'Unemployment Rate (%)'),
            ('Average Wage', 'Average Wage ($)'),
            ('Gini Coefficient', 'Gini Coefficient'),
            ('AI Adoption Rate', 'AI Adoption Rate (%)'),
            ('Labor Share', 'Labor Share (%)'),
            ('GDP', 'GDP')
        ]

        for ax, (metric, ylabel) in zip(axes, metrics):
            for scenario_name, results in results_dict.items():
                df = results['results']
                if metric in df.columns:
                    # Scale percentages
                    if '%' in ylabel and metric != 'Gini Coefficient':
                        data = df[metric] * 100
                    else:
                        data = df[metric]

                    ax.plot(df.index, data,
                           color=self.scenario_colors.get(scenario_name),
                           linewidth=2,
                           label=scenario_name.replace('_', ' ').title())

            ax.set_xlabel('Time Step')
            ax.set_ylabel(ylabel)
            ax.set_title(ylabel.replace(' (%)', '').replace(' ($)', ''), fontweight='bold')
            ax.grid(True, alpha=0.3)

            if ax == axes[0]:
                ax.legend(loc='best', framealpha=0.9)

        fig.suptitle('Multi-Scenario Comparison', fontsize=18, fontweight='bold')
        plt.tight_layout()

        if save_name:
            plt.savefig(os.path.join(self.output_dir, save_name), bbox_inches='tight')
            print(f"Saved: {save_name}")

        return fig
