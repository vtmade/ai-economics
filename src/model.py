"""
Main Simulation Model

Integrates all components:
- Worker and Firm agents
- Labor and goods markets
- Government policies
- AI impact modeling
- Data collection
"""

import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from src.agents.worker import Worker
from src.agents.firm import Firm
from src.agents.government import Government
from src.markets.labor_market import LaborMarket
from src.markets.goods_market import GoodsMarket
from src.ai_models.ai_impact import AIImpactModel

import config


class LaborMarketModel(Model):
    """
    Agent-based model of labor markets with AI adoption.

    Simulates the economic effects of AI technology on employment,
    wages, inequality, and productivity.
    """

    def __init__(self, scenario_name='baseline', num_workers=None, num_firms=None,
                 custom_config=None):
        """
        Initialize the model.

        Args:
            scenario_name: Name of scenario to run
            num_workers: Number of worker agents (default from config)
            num_firms: Number of firm agents (default from config)
            custom_config: Custom configuration overrides
        """
        super().__init__()

        self.scenario_name = scenario_name
        self.num_workers = num_workers or config.DEFAULT_NUM_WORKERS
        self.num_firms = num_firms or config.DEFAULT_NUM_FIRMS

        # Load configuration
        self.worker_config = config.WORKER_CONFIG.copy()
        self.firm_config = config.FIRM_CONFIG.copy()
        self.ai_config = config.AI_CONFIG.copy()
        self.task_config = config.TASK_CONFIG.copy()
        self.market_config = config.MARKET_CONFIG.copy()
        self.government_config = config.GOVERNMENT_CONFIG.copy()

        # Apply custom configuration
        if custom_config:
            self._apply_custom_config(custom_config)

        # Apply scenario-specific settings
        self._apply_scenario_config(scenario_name)

        # Initialize scheduler
        self.schedule = RandomActivation(self)

        # Create markets
        self.labor_market = LaborMarket(self, self.market_config['labor'])
        self.goods_market = GoodsMarket(self, self.market_config['goods'])

        # Create AI impact model
        ai_scenario_config = self.ai_config.get(scenario_name, self.ai_config['baseline'])
        ai_scenario_config['task_config'] = self.task_config
        self.ai_impact = AIImpactModel(ai_scenario_config)

        # Create agents
        self._create_workers()
        self._create_firms()

        # Create government (if policies are active)
        if self._government_needed():
            self.government = Government(self.next_id(), self, self.government_config)
            self.schedule.add(self.government)

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={
                'Unemployment Rate': lambda m: m.labor_market.unemployment_rate,
                'Average Wage': lambda m: m.labor_market.average_wage,
                'Low Skill Wage': lambda m: m.labor_market.wage_by_skill.get('low', 0),
                'Medium Skill Wage': lambda m: m.labor_market.wage_by_skill.get('medium', 0),
                'High Skill Wage': lambda m: m.labor_market.wage_by_skill.get('high', 0),
                'GDP': lambda m: m.goods_market.calculate_gdp(),
                'Price Level': lambda m: m.goods_market.price,
                'AI Adoption Rate': self._calculate_ai_adoption_rate,
                'Gini Coefficient': self._calculate_gini,
                'Labor Share': self._calculate_labor_share,
                'Average Productivity': self._calculate_avg_productivity,
                'Total Employment': self._count_employed,
                'Average Firm Profit': self._calculate_avg_profit,
                'Low Skill Employment Rate': lambda m: self._skill_employment_rate('low'),
                'Medium Skill Employment Rate': lambda m: self._skill_employment_rate('medium'),
                'High Skill Employment Rate': lambda m: self._skill_employment_rate('high')
            }
        )

        self.running = True

    def _apply_custom_config(self, custom_config):
        """Apply custom configuration parameters."""
        for key, value in custom_config.items():
            if hasattr(config, key):
                setattr(self, key.lower(), value)

    def _apply_scenario_config(self, scenario_name):
        """Apply scenario-specific configuration."""
        if scenario_name == 'retraining':
            # Enable retraining programs
            self.government_config['retraining']['enabled'] = True
            # Use low adoption AI parameters
            self.scenario_ai_config = 'low_adoption'
        elif scenario_name == 'custom':
            # Custom scenarios use provided parameters
            pass

    def _government_needed(self) -> bool:
        """Check if government agent is needed for this scenario."""
        return (self.government_config['ubi']['amount'] > 0 or
                self.government_config['retraining']['enabled'] or
                self.scenario_name == 'retraining')

    def _create_workers(self):
        """Create worker agents with heterogeneous skills."""
        skill_dist = self.worker_config['initial_skills']
        skill_levels = self.worker_config['skill_levels']

        for i in range(self.num_workers):
            # Assign skill level
            rand = np.random.random()
            if rand < skill_dist['low']:
                skill_level = 'low'
                skill_value = skill_levels['low'] + np.random.normal(0, 0.05)
            elif rand < skill_dist['low'] + skill_dist['medium']:
                skill_level = 'medium'
                skill_value = skill_levels['medium'] + np.random.normal(0, 0.05)
            else:
                skill_level = 'high'
                skill_value = skill_levels['high'] + np.random.normal(0, 0.05)

            skill_value = np.clip(skill_value, 0.1, 1.0)

            # Initial savings
            savings = max(0, np.random.normal(
                self.worker_config['initial_savings_mean'],
                self.worker_config['initial_savings_std']
            ))

            # Create worker
            worker = Worker(self.next_id(), self, skill_level, skill_value, savings,
                          self.worker_config)
            self.schedule.add(worker)

    def _create_firms(self):
        """Create firm agents with heterogeneous capital."""
        for i in range(self.num_firms):
            # Initial capital
            capital = max(10000, np.random.normal(
                self.firm_config['initial_capital_mean'],
                self.firm_config['initial_capital_std']
            ))

            # Create firm
            firm = Firm(self.next_id(), self, capital, self.firm_config)
            self.schedule.add(firm)

    def step(self):
        """Execute one step of the model."""
        # 1. Agents make decisions
        self.schedule.step()

        # 2. Labor market matching
        self.labor_market.match_workers_and_firms()
        self.labor_market.calculate_statistics()

        # 3. Goods market clearing
        self.goods_market.clear_market()

        # 4. Collect data
        self.datacollector.collect(self)

    def run_model(self, steps=None):
        """
        Run the model for a specified number of steps.

        Args:
            steps: Number of steps to run (default from config)
        """
        steps = steps or config.DEFAULT_STEPS

        for _ in range(steps):
            self.step()

    # Data collection methods

    def _calculate_ai_adoption_rate(self):
        """Calculate fraction of firms that have adopted AI."""
        firms = [agent for agent in self.schedule.agents if isinstance(agent, Firm)]
        if len(firms) == 0:
            return 0
        adopted = sum(1 for f in firms if f.ai_adopted)
        return adopted / len(firms)

    def _calculate_gini(self):
        """Calculate Gini coefficient of income inequality."""
        workers = [agent for agent in self.schedule.agents if isinstance(agent, Worker)]
        if len(workers) == 0:
            return 0

        incomes = sorted([w.income for w in workers])
        n = len(incomes)

        if sum(incomes) == 0:
            return 0

        # Calculate Gini coefficient
        numerator = sum((i + 1) * income for i, income in enumerate(incomes))
        denominator = n * sum(incomes)

        return (2 * numerator) / denominator - (n + 1) / n

    def _calculate_labor_share(self):
        """Calculate labor share of income."""
        firms = [agent for agent in self.schedule.agents if isinstance(agent, Firm)]
        if len(firms) == 0:
            return 0

        total_revenue = sum(f.revenue for f in firms)
        total_wages = sum(f.wage_bill for f in firms)

        if total_revenue == 0:
            return 0

        return total_wages / total_revenue

    def _calculate_avg_productivity(self):
        """Calculate average worker productivity."""
        workers = [agent for agent in self.schedule.agents if isinstance(agent, Worker)]
        if len(workers) == 0:
            return 0

        total_productivity = sum(w.skill_value for w in workers)
        return total_productivity / len(workers)

    def _count_employed(self):
        """Count number of employed workers."""
        workers = [agent for agent in self.schedule.agents if isinstance(agent, Worker)]
        return sum(1 for w in workers if w.employed)

    def _calculate_avg_profit(self):
        """Calculate average firm profit."""
        firms = [agent for agent in self.schedule.agents if isinstance(agent, Firm)]
        if len(firms) == 0:
            return 0
        return sum(f.profits for f in firms) / len(firms)

    def _skill_employment_rate(self, skill_level):
        """Calculate employment rate for specific skill level."""
        workers = [agent for agent in self.schedule.agents
                  if isinstance(agent, Worker) and agent.skill_level == skill_level]
        if len(workers) == 0:
            return 0
        employed = sum(1 for w in workers if w.employed)
        return employed / len(workers)

    def get_results(self):
        """
        Get model results as a pandas DataFrame.

        Returns:
            DataFrame with all collected metrics
        """
        return self.datacollector.get_model_vars_dataframe()

    def get_summary_statistics(self):
        """
        Get summary statistics from the model run.

        Returns:
            Dict with key economic indicators
        """
        df = self.get_results()

        if len(df) == 0:
            return {}

        # Calculate statistics over last 50 periods (steady state)
        steady_state = df.tail(50)

        return {
            'avg_unemployment_rate': steady_state['Unemployment Rate'].mean(),
            'avg_wage': steady_state['Average Wage'].mean(),
            'final_gini': steady_state['Gini Coefficient'].iloc[-1],
            'final_ai_adoption': steady_state['AI Adoption Rate'].iloc[-1],
            'avg_gdp': steady_state['GDP'].mean(),
            'labor_share': steady_state['Labor Share'].mean(),
            'wage_inequality': (steady_state['High Skill Wage'].mean() /
                              steady_state['Low Skill Wage'].mean() if
                              steady_state['Low Skill Wage'].mean() > 0 else 0),
            'employment_by_skill': {
                'low': steady_state['Low Skill Employment Rate'].mean(),
                'medium': steady_state['Medium Skill Employment Rate'].mean(),
                'high': steady_state['High Skill Employment Rate'].mean()
            }
        }
