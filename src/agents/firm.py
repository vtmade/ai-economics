"""
Firm Agent Implementation

Models firms with:
- Production functions (Cobb-Douglas)
- Hiring and firing decisions
- Wage setting based on market conditions
- AI adoption decisions based on cost-benefit analysis
- Capital investment
"""

import numpy as np
from mesa import Agent
from typing import List, Dict, Optional


class Firm(Agent):
    """
    Firm agent that makes production, hiring, and investment decisions.

    Attributes:
        capital (float): Capital stock
        workers (List[Worker]): Currently employed workers
        vacancies (int): Number of job openings
        production (float): Current period output
        revenue (float): Current period revenue
        profits (float): Current period profits
        wage_offered (float): Current wage offer
        ai_adopted (bool): Whether AI has been adopted
        ai_adoption_cost (float): Fixed cost of AI adoption
    """

    def __init__(self, unique_id: int, model, initial_capital: float, config: Dict):
        """
        Initialize a firm agent.

        Args:
            unique_id: Unique identifier
            model: Mesa model instance
            initial_capital: Initial capital stock
            config: Configuration dictionary
        """
        super().__init__(model)
        self.unique_id = unique_id

        # Production attributes
        self.capital = initial_capital
        self.workers = []
        self.vacancies = 0
        self.production = 0
        self.productivity_shock = 1.0

        # Financial attributes
        self.revenue = 0
        self.profits = 0
        self.costs = 0
        self.wage_bill = 0

        # Wage setting
        self.wage_offered = self._calculate_initial_wage()

        # AI adoption
        self.ai_adopted = False
        self.ai_adoption_cost = 0
        self.ai_operating_cost = 0
        self.adoption_period = None

        # Configuration
        self.config = config
        self.capital_share = config.get('capital_share', 0.3)
        self.labor_share = config.get('labor_share', 0.7)
        self.depreciation_rate = config.get('depreciation_rate', 0.05)
        self.markup = config.get('markup', 0.2)
        self.investment_rate = config.get('investment_rate', 0.15)
        self.max_vacancies = config.get('max_vacancies', 5)
        self.wage_adjustment_speed = config.get('wage_adjustment_speed', 0.1)

        # History
        self.profit_history = []
        self.production_history = []
        self.employment_history = []
        self.wage_history = []

    def _calculate_initial_wage(self) -> float:
        """Calculate initial wage offer."""
        # Base wage on capital stock (richer firms pay more)
        return 500 + np.log(self.capital) * 50

    def step(self):
        """Execute one step of firm behavior."""
        # 1. Produce with current workforce
        self._produce()

        # 2. Sell output and calculate profits
        self._calculate_profits()

        # 3. Make AI adoption decision
        self._consider_ai_adoption()

        # 4. Make hiring/firing decisions
        self._manage_workforce()

        # 5. Adjust wages based on market conditions
        self._adjust_wages()

        # 6. Invest in capital
        self._invest()

        # 7. Depreciate capital
        self.capital *= (1 - self.depreciation_rate)

        # Record history
        self.profit_history.append(self.profits)
        self.production_history.append(self.production)
        self.employment_history.append(len(self.workers))
        self.wage_history.append(self.wage_offered)

    def _produce(self):
        """Produce output using Cobb-Douglas production function."""
        if len(self.workers) == 0:
            self.production = 0
            return

        # Calculate effective labor input
        labor_input = sum(w.calculate_productivity(self.ai_adopted) for w in self.workers)

        # Cobb-Douglas: Y = A * K^α * L^(1-α)
        tfp = self.productivity_shock  # Total factor productivity
        self.production = tfp * (self.capital ** self.capital_share) * (labor_input ** self.labor_share)

        # AI can increase TFP
        if self.ai_adopted:
            ai_productivity_boost = self.model.ai_config.get('productivity_boost', 1.1)
            self.production *= ai_productivity_boost

    def _calculate_profits(self):
        """Calculate profits from production."""
        # Get price from goods market
        price = self.model.goods_market.get_price() if hasattr(self.model, 'goods_market') else 100

        # Revenue
        self.revenue = self.production * price

        # Costs
        self.wage_bill = sum(w.wage for w in self.workers)
        capital_costs = self.capital * self.depreciation_rate * 0.1  # Maintenance

        # AI operating costs
        if self.ai_adopted:
            ai_config = self._get_ai_config()
            # AI reduces labor costs
            labor_cost_reduction = ai_config.get('operating_cost_reduction', 0.1)
            self.wage_bill *= (1 - labor_cost_reduction)
            self.ai_operating_cost = self.capital * 0.02  # AI maintenance
        else:
            self.ai_operating_cost = 0

        self.costs = self.wage_bill + capital_costs + self.ai_operating_cost

        # Profits
        self.profits = self.revenue - self.costs

    def _consider_ai_adoption(self):
        """Decide whether to adopt AI technology."""
        if self.ai_adopted:
            return

        # Get AI configuration
        ai_config = self._get_ai_config()

        # Check if we're in adoption phase
        adoption_rate = ai_config.get('adoption_rate', 0)
        diffusion_speed = ai_config.get('diffusion_speed', 0.05)

        if adoption_rate == 0:
            return  # No AI in this scenario

        # Logistic diffusion curve
        current_step = self.model.schedule.steps
        adoption_probability = adoption_rate / (1 + np.exp(-diffusion_speed * (current_step - 50)))

        # Add firm heterogeneity - larger, more profitable firms adopt first
        if self.profits > 0:
            profit_factor = 1 + np.log(self.profits + 1) / 10
            adoption_probability *= profit_factor

        # Cost-benefit analysis
        adoption_cost = ai_config.get('adoption_cost', 50000)

        if np.random.random() < adoption_probability:
            # Can afford adoption?
            if self.profits > adoption_cost * 0.5:
                # Simple NPV calculation
                expected_cost_savings = self.wage_bill * ai_config.get('operating_cost_reduction', 0.1)
                expected_productivity_gain = self.revenue * 0.1

                if (expected_cost_savings + expected_productivity_gain) > adoption_cost * 0.2:
                    self._adopt_ai(adoption_cost)

    def _adopt_ai(self, cost: float):
        """Adopt AI technology."""
        self.ai_adopted = True
        self.ai_adoption_cost = cost
        self.adoption_period = self.model.schedule.steps
        self.capital -= cost  # Pay adoption cost from capital

        # Automation may reduce workforce needs
        self._automate_tasks()

    def _automate_tasks(self):
        """Reduce workforce due to automation."""
        ai_config = self._get_ai_config()
        automation_intensity = ai_config.get('automation_intensity', 0.3)

        # Determine which workers to lay off based on automation risk
        workers_at_risk = [(w, w.automation_risk()) for w in self.workers]
        workers_at_risk.sort(key=lambda x: x[1], reverse=True)

        # Lay off workers based on automation intensity
        num_to_fire = int(len(self.workers) * automation_intensity * 0.5)

        for i in range(num_to_fire):
            if i < len(workers_at_risk):
                worker = workers_at_risk[i][0]
                self.fire_worker(worker)

    def _get_ai_config(self) -> Dict:
        """Get current AI configuration based on scenario."""
        scenario_name = getattr(self.model, 'scenario_name', 'baseline')

        if scenario_name == 'baseline':
            return self.model.ai_config.get('baseline', {})
        elif scenario_name in ['low_adoption', 'retraining']:
            return self.model.ai_config.get('low_adoption', {})
        elif scenario_name == 'high_adoption':
            return self.model.ai_config.get('high_adoption', {})
        else:
            return self.model.ai_config.get('baseline', {})

    def _manage_workforce(self):
        """Make hiring and firing decisions."""
        # Calculate desired workforce size based on marginal product
        desired_workers = self._calculate_optimal_workforce()

        current_workers = len(self.workers)

        if current_workers < desired_workers:
            # Post vacancies
            vacancies_to_post = min(desired_workers - current_workers, self.max_vacancies)
            self.vacancies = vacancies_to_post
        elif current_workers > desired_workers * 1.2:
            # Lay off workers if significantly overstaffed
            num_to_fire = int((current_workers - desired_workers) * 0.3)
            self._fire_excess_workers(num_to_fire)

    def _calculate_optimal_workforce(self) -> int:
        """Calculate profit-maximizing workforce size."""
        if self.capital <= 0:
            return 0

        # Marginal product of labor at current scale
        current_workers = max(len(self.workers), 1)

        # Price and wage
        price = self.model.goods_market.get_price() if hasattr(self.model, 'goods_market') else 100
        wage = self.wage_offered

        # MPL = (1-α) * Y / L
        if self.production > 0:
            mpl = self.labor_share * self.production / current_workers
            marginal_revenue_product = mpl * price

            # Hire if MRP > wage
            if marginal_revenue_product > wage * 1.2:
                return int(current_workers * 1.3)
            elif marginal_revenue_product < wage * 0.8:
                return int(current_workers * 0.8)

        return current_workers

    def _fire_excess_workers(self, num_to_fire: int):
        """Fire workers, targeting lowest productivity first."""
        if num_to_fire >= len(self.workers):
            num_to_fire = len(self.workers) - 1  # Keep at least one worker

        if num_to_fire <= 0:
            return

        # Sort by productivity
        workers_by_productivity = sorted(self.workers,
                                        key=lambda w: w.calculate_productivity(self.ai_adopted))

        # Fire least productive
        for i in range(num_to_fire):
            worker = workers_by_productivity[i]
            self.fire_worker(worker)

    def _adjust_wages(self):
        """Adjust wage offers based on market conditions."""
        # If we have unfilled vacancies, raise wages
        if self.vacancies > 0 and len(self.workers) < self._calculate_optimal_workforce():
            self.wage_offered *= (1 + self.wage_adjustment_speed)

        # If we're overstaffed and profits are low, lower wages
        if self.profits < 0 and len(self.workers) > self._calculate_optimal_workforce():
            self.wage_offered *= (1 - self.wage_adjustment_speed * 0.5)

        # Don't let wages fall below minimum
        self.wage_offered = max(self.wage_offered, 300)

    def _invest(self):
        """Invest profits in capital."""
        if self.profits > 0:
            investment = self.profits * self.investment_rate
            self.capital += investment

    def hire_worker(self, worker):
        """
        Hire a worker.

        Args:
            worker: Worker agent to hire
        """
        if worker not in self.workers:
            self.workers.append(worker)
            self.vacancies = max(0, self.vacancies - 1)

    def fire_worker(self, worker):
        """
        Fire a worker.

        Args:
            worker: Worker agent to fire
        """
        if worker in self.workers:
            self.workers.remove(worker)
            worker.get_fired()

    def get_vacancies(self) -> int:
        """Get number of open positions."""
        return self.vacancies

    def get_average_productivity(self) -> float:
        """Calculate average worker productivity."""
        if len(self.workers) == 0:
            return 0
        return sum(w.calculate_productivity(self.ai_adopted) for w in self.workers) / len(self.workers)
