"""
AI Impact Modeling

Task-based framework for modeling AI's effects on labor markets:
- Automation (labor displacement)
- Augmentation (productivity enhancement)
- Skill-biased technical change
- Gradual diffusion
"""

import numpy as np
from typing import Dict, Tuple


class AIImpactModel:
    """
    Models the impact of AI on tasks, workers, and firms.

    Based on task-based framework from Acemoglu & Restrepo (2018).
    """

    def __init__(self, config: Dict):
        """
        Initialize AI impact model.

        Args:
            config: AI configuration including automation and augmentation parameters
        """
        self.config = config
        self.task_config = config.get('task_config', {})

        # AI parameters
        self.automation_intensity = config.get('automation_intensity', 0.3)
        self.augmentation_intensity = config.get('augmentation_intensity', 0.2)
        self.diffusion_speed = config.get('diffusion_speed', 0.05)
        self.adoption_rate = config.get('adoption_rate', 0.5)

    def calculate_task_automation(self, task_type: str) -> float:
        """
        Calculate degree of automation for a task type.

        Args:
            task_type: Type of task (routine_cognitive, etc.)

        Returns:
            float: Automation level (0-1)
        """
        susceptibility = self.task_config.get('automation_susceptibility', {}).get(task_type, 0)
        return susceptibility * self.automation_intensity

    def calculate_task_augmentation(self, task_type: str) -> float:
        """
        Calculate degree of augmentation for a task type.

        Args:
            task_type: Type of task

        Returns:
            float: Augmentation level (0-1)
        """
        potential = self.task_config.get('augmentation_potential', {}).get(task_type, 0)
        return potential * self.augmentation_intensity

    def calculate_worker_displacement_risk(self, worker) -> float:
        """
        Calculate probability that worker is displaced by automation.

        Args:
            worker: Worker agent

        Returns:
            float: Displacement risk (0-1)
        """
        displacement_risk = 0

        for task_type, task_share in worker.task_composition.items():
            automation = self.calculate_task_automation(task_type)
            displacement_risk += task_share * automation

        return displacement_risk

    def calculate_worker_productivity_gain(self, worker) -> float:
        """
        Calculate productivity gain from AI augmentation.

        Args:
            worker: Worker agent

        Returns:
            float: Productivity multiplier (e.g., 1.2 = 20% gain)
        """
        productivity_gain = 0

        for task_type, task_share in worker.task_composition.items():
            augmentation = self.calculate_task_augmentation(task_type)
            productivity_gain += task_share * augmentation

        return 1 + productivity_gain

    def calculate_labor_share_change(self, baseline_labor_share: float,
                                    ai_adoption_rate: float) -> float:
        """
        Calculate change in labor share of income due to AI.

        Args:
            baseline_labor_share: Labor share before AI
            ai_adoption_rate: Fraction of economy with AI

        Returns:
            float: New labor share
        """
        # Automation reduces labor share
        automation_effect = -self.automation_intensity * 0.1 * ai_adoption_rate

        # Augmentation can increase or decrease labor share
        # (depends on whether it's labor-augmenting or capital-augmenting)
        augmentation_effect = self.augmentation_intensity * 0.05 * ai_adoption_rate

        return baseline_labor_share + automation_effect + augmentation_effect

    def get_diffusion_rate(self, time_step: int) -> float:
        """
        Calculate AI adoption rate at given time using logistic diffusion curve.

        Args:
            time_step: Current simulation step

        Returns:
            float: Adoption rate at this time (0-1)
        """
        # Logistic function: L / (1 + exp(-k(t - t0)))
        midpoint = 50  # Time when adoption reaches 50% of maximum
        adoption = self.adoption_rate / (1 + np.exp(-self.diffusion_speed * (time_step - midpoint)))

        return adoption

    def calculate_skill_bias(self) -> Dict[str, float]:
        """
        Calculate skill-biased nature of AI technology.

        Returns:
            Dict: Impact by skill level (positive = benefits, negative = harms)
        """
        # AI tends to be:
        # - Highly automating for routine tasks (hurts low-medium skill)
        # - Highly augmenting for cognitive tasks (helps high skill)

        return {
            'low': -self.automation_intensity * 0.4,      # Negative impact
            'medium': -self.automation_intensity * 0.2,   # Small negative impact
            'high': self.augmentation_intensity * 0.3     # Positive impact
        }

    def estimate_employment_effect(self, baseline_employment: int,
                                   ai_adoption_rate: float) -> Tuple[int, Dict]:
        """
        Estimate aggregate employment effect of AI.

        Args:
            baseline_employment: Employment before AI
            ai_adoption_rate: Current AI adoption rate

        Returns:
            Tuple of (new employment level, breakdown by skill)
        """
        # Displacement effect
        displacement = self.automation_intensity * ai_adoption_rate * baseline_employment

        # Productivity effect creates new jobs
        productivity_boost = self.augmentation_intensity * ai_adoption_rate
        job_creation = productivity_boost * baseline_employment * 0.5

        # Net effect
        net_employment_change = job_creation - displacement
        new_employment = int(baseline_employment + net_employment_change)

        # Breakdown by skill
        skill_bias = self.calculate_skill_bias()
        breakdown = {
            'low': baseline_employment * 0.3 * (1 + skill_bias['low'] * ai_adoption_rate),
            'medium': baseline_employment * 0.5 * (1 + skill_bias['medium'] * ai_adoption_rate),
            'high': baseline_employment * 0.2 * (1 + skill_bias['high'] * ai_adoption_rate)
        }

        return new_employment, breakdown

    def calculate_wage_polarization(self, wage_distribution: Dict[str, float],
                                   ai_adoption_rate: float) -> Dict[str, float]:
        """
        Calculate wage changes due to AI-induced polarization.

        Args:
            wage_distribution: Current wages by skill
            ai_adoption_rate: Current AI adoption rate

        Returns:
            Dict: New wages by skill level
        """
        skill_bias = self.calculate_skill_bias()

        new_wages = {}
        for skill, base_wage in wage_distribution.items():
            # Wage changes based on skill bias
            wage_change = skill_bias[skill] * ai_adoption_rate
            new_wages[skill] = base_wage * (1 + wage_change)

        return new_wages


class TechnologyDiffusion:
    """
    Models gradual diffusion of AI technology across firms.
    """

    def __init__(self, adoption_rate: float, diffusion_speed: float):
        """
        Initialize diffusion model.

        Args:
            adoption_rate: Maximum adoption rate
            diffusion_speed: Speed of diffusion
        """
        self.adoption_rate = adoption_rate
        self.diffusion_speed = diffusion_speed

    def get_adoption_probability(self, time_step: int, firm_characteristics: Dict) -> float:
        """
        Calculate adoption probability for a firm.

        Args:
            time_step: Current time
            firm_characteristics: Firm attributes (size, profitability, etc.)

        Returns:
            float: Adoption probability
        """
        # Base probability from diffusion curve
        base_prob = self.adoption_rate / (1 + np.exp(-self.diffusion_speed * (time_step - 50)))

        # Adjust for firm characteristics
        size_factor = 1 + np.log(firm_characteristics.get('capital', 1000)) / 20
        profit_factor = 1 if firm_characteristics.get('profits', 0) > 0 else 0.5

        return base_prob * size_factor * profit_factor
