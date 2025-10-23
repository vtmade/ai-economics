"""
Government Agent Implementation

Models government policy interventions:
- Universal Basic Income (UBI)
- Retraining programs
- Unemployment insurance
- Tax collection
"""

import numpy as np
from mesa import Agent
from typing import Dict, Optional


class Government(Agent):
    """
    Government agent that implements labor market policies.

    Attributes:
        ubi_amount (float): Universal basic income per worker
        tax_revenue (float): Total tax revenue collected
        program_spending (float): Total spending on programs
        budget_balance (float): Surplus or deficit
    """

    def __init__(self, unique_id: int, model, config: Dict):
        """
        Initialize government agent.

        Args:
            unique_id: Unique identifier
            model: Mesa model instance
            config: Configuration dictionary with policy parameters
        """
        super().__init__(model)
        self.unique_id = unique_id

        self.config = config

        # UBI settings
        self.ubi_enabled = config['ubi']['amount'] > 0
        self.ubi_amount = config['ubi']['amount']
        self.ubi_tax_rate = config['ubi']['tax_rate']

        # Retraining settings
        self.retraining_enabled = config['retraining']['enabled']
        self.retraining_cost = config['retraining']['cost_per_worker']
        self.retraining_subsidy = config['retraining']['subsidy_rate']

        # Unemployment insurance
        self.ui_replacement_rate = config['unemployment_insurance']['replacement_rate']
        self.ui_duration = config['unemployment_insurance']['duration']
        self.ui_tax_rate = config['unemployment_insurance']['tax_rate']

        # Budget tracking
        self.tax_revenue = 0
        self.ubi_spending = 0
        self.retraining_spending = 0
        self.ui_spending = 0
        self.budget_balance = 0

        # History
        self.tax_revenue_history = []
        self.spending_history = []
        self.budget_history = []

    def step(self):
        """Execute government operations for the period."""
        # Collect taxes
        self._collect_taxes()

        # Pay out UBI
        if self.ubi_enabled:
            self._distribute_ubi()

        # Pay unemployment insurance
        self._pay_unemployment_insurance()

        # Calculate budget balance
        total_spending = self.ubi_spending + self.retraining_spending + self.ui_spending
        self.budget_balance = self.tax_revenue - total_spending

        # Record history
        self.tax_revenue_history.append(self.tax_revenue)
        self.spending_history.append(total_spending)
        self.budget_history.append(self.budget_balance)

        # Reset for next period
        self.tax_revenue = 0
        self.ubi_spending = 0
        self.retraining_spending = 0
        self.ui_spending = 0

    def _collect_taxes(self):
        """Collect taxes from workers and firms."""
        # Income tax from workers
        income_tax_rate = self.ubi_tax_rate + self.ui_tax_rate

        for worker in self.model.schedule.agents:
            if hasattr(worker, 'income') and worker.income > 0:
                tax = worker.income * income_tax_rate
                worker.savings -= tax
                self.tax_revenue += tax

        # Corporate tax from firms
        corporate_tax_rate = 0.15  # Fixed corporate tax rate

        for firm in self.model.schedule.agents:
            if hasattr(firm, 'profits') and firm.profits > 0:
                tax = firm.profits * corporate_tax_rate
                firm.capital -= tax
                self.tax_revenue += tax

    def _distribute_ubi(self):
        """Distribute universal basic income to all workers."""
        for worker in self.model.schedule.agents:
            if hasattr(worker, 'savings'):
                worker.savings += self.ubi_amount
                worker.income += self.ubi_amount
                self.ubi_spending += self.ubi_amount

    def _pay_unemployment_insurance(self):
        """Pay unemployment insurance to eligible workers."""
        for worker in self.model.schedule.agents:
            if hasattr(worker, 'employed'):
                benefit = self.get_unemployment_benefit(worker)
                if benefit > 0:
                    self.ui_spending += benefit

    def get_unemployment_benefit(self, worker) -> float:
        """
        Calculate unemployment insurance benefit for a worker.

        Args:
            worker: Worker agent

        Returns:
            float: UI benefit amount
        """
        # Check eligibility
        if worker.employed or worker.unemployment_duration > self.ui_duration:
            return 0

        # Calculate benefit based on previous wage
        if len(worker.wage_history) > 0:
            previous_wage = worker.wage_history[-1]
            benefit = previous_wage * self.ui_replacement_rate
            return benefit

        return 0

    def offer_retraining(self, worker) -> bool:
        """
        Offer retraining program to eligible worker.

        Args:
            worker: Worker agent

        Returns:
            bool: Whether worker is enrolled
        """
        if not self.retraining_enabled:
            return False

        # Check if worker is eligible (unemployed, low-medium skill)
        if not worker.employed and worker.skill_level in ['low', 'medium']:
            # Worker pays portion of cost
            worker_cost = self.retraining_cost * (1 - self.retraining_subsidy)

            # Check if worker can afford it
            if worker.savings >= worker_cost or self.retraining_subsidy == 1.0:
                worker.savings -= worker_cost
                self.retraining_spending += self.retraining_cost
                return True

        return False

    def get_tax_rate(self) -> float:
        """Get total tax rate."""
        return self.ubi_tax_rate + self.ui_tax_rate

    def get_budget_summary(self) -> Dict:
        """
        Get summary of government budget.

        Returns:
            Dict: Budget statistics
        """
        return {
            'tax_revenue': self.tax_revenue,
            'ubi_spending': self.ubi_spending,
            'retraining_spending': self.retraining_spending,
            'ui_spending': self.ui_spending,
            'total_spending': self.ubi_spending + self.retraining_spending + self.ui_spending,
            'budget_balance': self.budget_balance
        }
