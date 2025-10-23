"""
Labor Market Implementation

Implements matching between workers and firms with:
- Search and matching frictions
- Wage negotiations
- Vacancy posting and job search
"""

import numpy as np
from typing import List, Tuple, Dict


class LaborMarket:
    """
    Labor market with search and matching frictions.

    Implements a simplified version of the Diamond-Mortensen-Pissarides
    search and matching model.
    """

    def __init__(self, model, config: Dict):
        """
        Initialize labor market.

        Args:
            model: Mesa model instance
            config: Market configuration
        """
        self.model = model
        self.config = config

        self.matching_efficiency = config.get('matching_efficiency', 0.5)
        self.search_friction = config.get('search_friction', 0.2)
        self.wage_stickiness = config.get('wage_stickiness', 0.3)

        # Market statistics
        self.unemployment_rate = 0
        self.vacancy_rate = 0
        self.job_finding_rate = 0
        self.average_wage = 0
        self.wage_by_skill = {'low': 0, 'medium': 0, 'high': 0}

        # History
        self.unemployment_history = []
        self.vacancy_history = []
        self.wage_history = []

    def match_workers_and_firms(self):
        """
        Match unemployed workers with firms that have vacancies.

        Uses a random matching process with matching efficiency parameter.
        """
        # Get unemployed workers
        unemployed = [agent for agent in self.model.schedule.agents
                     if hasattr(agent, 'employed') and not agent.employed
                     and not agent.in_retraining]

        # Get firms with vacancies
        firms_with_vacancies = [(agent, agent.get_vacancies())
                               for agent in self.model.schedule.agents
                               if hasattr(agent, 'get_vacancies') and agent.get_vacancies() > 0]

        if len(unemployed) == 0 or len(firms_with_vacancies) == 0:
            return

        # Create vacancy list
        vacancies = []
        for firm, num_vacancies in firms_with_vacancies:
            for _ in range(num_vacancies):
                vacancies.append(firm)

        # Shuffle for random matching
        np.random.shuffle(unemployed)
        np.random.shuffle(vacancies)

        # Match workers to vacancies
        matches_attempted = 0
        matches_made = 0

        for i, worker in enumerate(unemployed):
            if i >= len(vacancies):
                break

            firm = vacancies[i]
            matches_attempted += 1

            # Matching occurs with probability matching_efficiency
            if np.random.random() < self.matching_efficiency:
                # Wage negotiation
                wage = self._negotiate_wage(worker, firm)

                # Worker accepts if wage >= reservation wage
                if worker.receive_job_offer(firm, wage):
                    firm.hire_worker(worker)
                    matches_made += 1

        # Calculate job finding rate
        if len(unemployed) > 0:
            self.job_finding_rate = matches_made / len(unemployed)

    def _negotiate_wage(self, worker, firm) -> float:
        """
        Negotiate wage between worker and firm.

        Uses a simple bargaining model where wage is between
        worker's reservation wage and firm's willingness to pay.

        Args:
            worker: Worker agent
            firm: Firm agent

        Returns:
            float: Negotiated wage
        """
        # Worker's reservation wage
        reservation_wage = worker.reservation_wage

        # Firm's maximum willingness to pay (based on marginal product)
        price = self.model.goods_market.get_price() if hasattr(self.model, 'goods_market') else 100

        # Marginal product of labor
        if firm.production > 0 and len(firm.workers) > 0:
            mpl = firm.labor_share * firm.production / len(firm.workers)
            max_wage = mpl * price * 0.8  # Firm keeps some surplus
        else:
            max_wage = firm.wage_offered

        # Nash bargaining with equal bargaining power
        if max_wage > reservation_wage:
            wage = (reservation_wage + max_wage) / 2
        else:
            wage = firm.wage_offered

        # Some wage stickiness - adjust slowly toward market clearing
        wage = firm.wage_offered * self.wage_stickiness + wage * (1 - self.wage_stickiness)

        return wage

    def calculate_statistics(self):
        """Calculate labor market statistics."""
        # Get all workers and firms
        workers = [agent for agent in self.model.schedule.agents
                  if hasattr(agent, 'employed')]
        firms = [agent for agent in self.model.schedule.agents
                if hasattr(agent, 'workers')]

        if len(workers) == 0:
            return

        # Unemployment rate
        unemployed = sum(1 for w in workers if not w.employed)
        self.unemployment_rate = unemployed / len(workers)

        # Vacancy rate
        total_vacancies = sum(f.get_vacancies() for f in firms)
        total_jobs = sum(len(f.workers) for f in firms) + total_vacancies
        if total_jobs > 0:
            self.vacancy_rate = total_vacancies / total_jobs

        # Average wage
        employed_workers = [w for w in workers if w.employed]
        if len(employed_workers) > 0:
            self.average_wage = sum(w.wage for w in employed_workers) / len(employed_workers)

            # Wage by skill level
            for skill in ['low', 'medium', 'high']:
                skill_workers = [w for w in employed_workers if w.skill_level == skill]
                if len(skill_workers) > 0:
                    self.wage_by_skill[skill] = sum(w.wage for w in skill_workers) / len(skill_workers)

        # Record history
        self.unemployment_history.append(self.unemployment_rate)
        self.vacancy_history.append(self.vacancy_rate)
        self.wage_history.append(self.average_wage)

    def get_beveridge_curve_data(self) -> Tuple[List[float], List[float]]:
        """
        Get data for Beveridge curve (unemployment vs vacancies).

        Returns:
            Tuple of unemployment rates and vacancy rates
        """
        return self.unemployment_history, self.vacancy_history

    def get_statistics(self) -> Dict:
        """
        Get current labor market statistics.

        Returns:
            Dict: Labor market statistics
        """
        return {
            'unemployment_rate': self.unemployment_rate,
            'vacancy_rate': self.vacancy_rate,
            'job_finding_rate': self.job_finding_rate,
            'average_wage': self.average_wage,
            'wage_by_skill': self.wage_by_skill.copy()
        }
