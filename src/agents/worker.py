"""
Worker Agent Implementation

Models individual workers with:
- Heterogeneous skills (low, medium, high)
- Consumption and savings behavior
- Job search and labor supply decisions
- Skill accumulation and depreciation
- Responses to AI-driven labor market changes
"""

import numpy as np
from mesa import Agent
from typing import Optional, Dict


class Worker(Agent):
    """
    Worker agent that makes labor supply and consumption decisions.

    Attributes:
        skill_level (str): One of 'low', 'medium', 'high'
        skill_value (float): Numerical skill level (0-1 scale)
        employed (bool): Employment status
        employer (Firm): Current employer (if employed)
        wage (float): Current wage
        savings (float): Accumulated savings
        consumption (float): Current period consumption
        reservation_wage (float): Minimum acceptable wage
        task_composition (Dict): Distribution of tasks performed
        in_retraining (bool): Whether currently in retraining program
        retraining_progress (int): Progress in retraining program
    """

    def __init__(self, unique_id: int, model, skill_level: str,
                 initial_skill: float, initial_savings: float, config: Dict):
        """
        Initialize a worker agent.

        Args:
            unique_id: Unique identifier for the agent
            model: Mesa model instance
            skill_level: Skill category ('low', 'medium', 'high')
            initial_skill: Initial skill value (0-1)
            initial_savings: Initial savings amount
            config: Configuration dictionary with worker parameters
        """
        super().__init__(unique_id, model)

        # Skill attributes
        self.skill_level = skill_level
        self.skill_value = initial_skill
        self.initial_skill = initial_skill

        # Employment attributes
        self.employed = False
        self.employer = None
        self.wage = 0
        self.wage_history = []
        self.unemployment_duration = 0

        # Financial attributes
        self.savings = initial_savings
        self.consumption = 0
        self.income = 0

        # Job search attributes
        self.reservation_wage = initial_skill * config.get('reservation_wage_factor', 0.7) * 1000
        self.job_offers = []

        # Task composition (for AI impact analysis)
        self.task_composition = self._initialize_tasks(skill_level,
                                                       model.task_config['task_distribution'])

        # Retraining attributes
        self.in_retraining = False
        self.retraining_progress = 0
        self.retraining_duration = 0

        # Configuration
        self.config = config
        self.consumption_propensity = config.get('consumption_propensity', 0.8)
        self.learning_rate = config.get('learning_rate', 0.01)
        self.skill_depreciation = config.get('skill_depreciation', 0.005)
        self.job_search_cost = config.get('job_search_cost', 50)

        # History for analysis
        self.employment_history = []
        self.income_history = []
        self.skill_history = []

    def _initialize_tasks(self, skill_level: str, task_dist: Dict) -> Dict[str, float]:
        """Initialize task composition based on skill level."""
        return task_dist[skill_level].copy()

    def step(self):
        """Execute one step of worker behavior."""
        # Record current state
        self.employment_history.append(self.employed)
        self.income_history.append(self.income)
        self.skill_history.append(self.skill_value)

        # Update based on employment status
        if self.employed:
            self._work()
        else:
            self._search_for_job()
            self.unemployment_duration += 1

        # Handle retraining
        if self.in_retraining:
            self._progress_retraining()

        # Make consumption decision
        self._consume()

        # Update skills
        self._update_skills()

    def _work(self):
        """Perform work and receive wage."""
        if self.employer is None:
            self.employed = False
            return

        # Receive wage
        self.income = self.wage
        self.savings += self.wage
        self.wage_history.append(self.wage)

        # Update reservation wage based on current wage
        self.reservation_wage = self.wage * self.config.get('reservation_wage_factor', 0.7)

        # Reset unemployment counter
        self.unemployment_duration = 0

    def _search_for_job(self):
        """Search for employment opportunities."""
        # Pay search cost
        search_cost = self.job_search_cost
        self.savings -= search_cost
        self.income = 0

        # Get unemployment benefits if available
        if hasattr(self.model, 'government'):
            ui_payment = self.model.government.get_unemployment_benefit(self)
            self.savings += ui_payment
            self.income += ui_payment

        # Consider retraining if unemployed for a while
        if (self.unemployment_duration > 5 and
            not self.in_retraining and
            hasattr(self.model, 'government')):
            if self.model.government.offer_retraining(self):
                self.in_retraining = True
                self.retraining_duration = self.model.government.config['retraining']['duration']

        # Adjust reservation wage if unemployed for long period
        if self.unemployment_duration > 10:
            self.reservation_wage *= 0.95  # Become less selective

    def _consume(self):
        """Make consumption decision based on permanent income hypothesis."""
        # Calculate consumption based on savings and income
        if self.savings > 0:
            # Consume a fraction of income plus some savings if needed
            target_consumption = self.income * self.consumption_propensity
            if target_consumption > self.savings:
                target_consumption = self.savings * 0.9  # Don't exhaust all savings

            self.consumption = max(target_consumption, 0)
            self.savings -= self.consumption
        else:
            self.consumption = 0
            # Negative savings represent debt
            self.savings *= 1.05  # Interest on debt

    def _update_skills(self):
        """Update skill level based on employment and learning."""
        if self.employed and not self.in_retraining:
            # Learning by doing - skill improvement when employed
            self.skill_value += self.learning_rate * (1 - self.skill_value)
            self.skill_value = min(self.skill_value, 1.0)
        elif not self.employed and not self.in_retraining:
            # Skill depreciation when unemployed
            self.skill_value -= self.skill_depreciation
            self.skill_value = max(self.skill_value, 0.1)

    def _progress_retraining(self):
        """Progress through retraining program."""
        self.retraining_progress += 1

        if self.retraining_progress >= self.retraining_duration:
            # Complete retraining
            gov_config = self.model.government.config['retraining']
            success = np.random.random() < gov_config['success_rate']

            if success:
                # Skill improvement
                self.skill_value += gov_config['skill_improvement']
                self.skill_value = min(self.skill_value, 1.0)

                # Potentially upgrade skill level
                if self.skill_level == 'low' and self.skill_value > 0.5:
                    self.skill_level = 'medium'
                    self.task_composition = self._initialize_tasks(
                        'medium', self.model.task_config['task_distribution']
                    )
                elif self.skill_level == 'medium' and self.skill_value > 0.8:
                    self.skill_level = 'high'
                    self.task_composition = self._initialize_tasks(
                        'high', self.model.task_config['task_distribution']
                    )

            # Reset retraining status
            self.in_retraining = False
            self.retraining_progress = 0
            self.retraining_duration = 0

    def receive_job_offer(self, firm, wage: float):
        """
        Receive and evaluate a job offer.

        Args:
            firm: Firm making the offer
            wage: Offered wage

        Returns:
            bool: Whether offer is accepted
        """
        # Don't accept offers if in retraining
        if self.in_retraining:
            return False

        # Accept if wage exceeds reservation wage
        if wage >= self.reservation_wage:
            # Quit current job if employed
            if self.employed and self.employer is not None:
                self.quit_job()

            # Accept new job
            self.employed = True
            self.employer = firm
            self.wage = wage
            return True

        return False

    def quit_job(self):
        """Quit current job."""
        if self.employer is not None:
            self.employer.fire_worker(self)

        self.employed = False
        self.employer = None
        self.wage = 0

    def get_fired(self):
        """Handle being fired by employer."""
        self.employed = False
        self.employer = None
        self.wage = 0
        self.unemployment_duration = 0

    def calculate_productivity(self, ai_adoption: bool = False) -> float:
        """
        Calculate worker productivity, potentially augmented by AI.

        Args:
            ai_adoption: Whether firm has adopted AI

        Returns:
            float: Worker productivity
        """
        base_productivity = self.skill_value

        if ai_adoption:
            # Calculate AI augmentation effect based on task composition
            augmentation = 0
            for task_type, task_share in self.task_composition.items():
                aug_potential = self.model.task_config['augmentation_potential'][task_type]
                augmentation += task_share * aug_potential

            # AI augments productivity
            ai_config = self.model.ai_config.get('augmentation_intensity', 0.3)
            base_productivity *= (1 + ai_config * augmentation)

        return base_productivity

    def automation_risk(self) -> float:
        """
        Calculate risk of automation based on task composition.

        Returns:
            float: Automation risk (0-1)
        """
        risk = 0
        for task_type, task_share in self.task_composition.items():
            auto_susceptibility = self.model.task_config['automation_susceptibility'][task_type]
            risk += task_share * auto_susceptibility

        return risk

    def get_welfare(self) -> float:
        """
        Calculate worker welfare (utility function).

        Returns:
            float: Welfare measure
        """
        # Simple log utility from consumption
        if self.consumption > 0:
            consumption_utility = np.log(self.consumption + 1)
        else:
            consumption_utility = 0

        # Disutility from unemployment
        employment_utility = 10 if self.employed else 0

        # Savings provide security
        savings_utility = np.log(max(self.savings, 1)) * 0.5

        return consumption_utility + employment_utility + savings_utility
