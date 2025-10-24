"""
Configuration file for AI Labor Market Simulation

This file contains all default parameters for the simulation.
Users can override these by passing custom parameters to scenarios.
"""

# Simulation parameters
DEFAULT_NUM_WORKERS = 100
DEFAULT_NUM_FIRMS = 20
DEFAULT_STEPS = 200
RANDOM_SEED = 42

# Worker parameters
WORKER_CONFIG = {
    'initial_skills': {
        'low': 0.3,      # Proportion of low-skilled workers
        'medium': 0.5,   # Proportion of medium-skilled workers
        'high': 0.2      # Proportion of high-skilled workers
    },
    'skill_levels': {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.9
    },
    'initial_savings_mean': 10000,
    'initial_savings_std': 3000,
    'consumption_propensity': 0.75,  # Fraction of income consumed (reduced to avoid debt spiral)
    'reservation_wage_factor': 0.5,  # Minimum acceptable wage (more flexible)
    'job_search_cost': 20,           # Cost per period of job searching (reduced)
    'learning_rate': 0.01,           # Skill improvement rate when employed
    'skill_depreciation': 0.005      # Skill decay rate when unemployed
}

# Firm parameters
FIRM_CONFIG = {
    'initial_capital_mean': 100000,
    'initial_capital_std': 30000,
    'production_function': 'cobb_douglas',
    'capital_share': 0.3,            # Alpha in Cobb-Douglas
    'labor_share': 0.7,              # 1 - alpha
    'depreciation_rate': 0.05,       # Capital depreciation per period
    'markup': 0.2,                   # Markup over marginal cost
    'investment_rate': 0.15,         # Fraction of profits invested
    'max_vacancies': 5,              # Maximum job openings per firm
    'wage_adjustment_speed': 0.1     # Speed of wage adjustment to market conditions
}

# AI adoption parameters
AI_CONFIG = {
    'baseline': {
        'adoption_rate': 0.0,
        'automation_intensity': 0.0,
        'augmentation_intensity': 0.0
    },
    'low_adoption': {
        'adoption_rate': 0.3,           # 30% of firms eventually adopt
        'diffusion_speed': 0.02,        # Slow diffusion
        'automation_intensity': 0.3,    # Low automation effect
        'augmentation_intensity': 0.2,  # Low augmentation effect
        'adoption_cost': 50000,         # High fixed cost
        'operating_cost_reduction': 0.1 # 10% reduction in labor costs
    },
    'high_adoption': {
        'adoption_rate': 0.8,           # 80% of firms eventually adopt
        'diffusion_speed': 0.08,        # Fast diffusion
        'automation_intensity': 0.5,    # High automation effect
        'augmentation_intensity': 0.4,  # High augmentation effect
        'adoption_cost': 30000,         # Lower fixed cost
        'operating_cost_reduction': 0.25 # 25% reduction in labor costs
    },
    'extreme_displacement': {
        'adoption_rate': 0.95,          # 95% of firms adopt (near universal)
        'diffusion_speed': 0.15,        # Very fast diffusion
        'automation_intensity': 0.85,   # Extreme automation - 85% of routine tasks
        'augmentation_intensity': 0.6,  # High augmentation for survivors
        'adoption_cost': 10000,         # Very low cost (AI commoditized)
        'operating_cost_reduction': 0.65 # 65% reduction in labor costs
    },
    'technological_singularity': {
        'adoption_rate': 0.98,          # Near-universal adoption
        'diffusion_speed': 0.20,        # Explosive diffusion
        'automation_intensity': 0.95,   # 95% of jobs automated
        'augmentation_intensity': 0.8,  # Massive augmentation for elite
        'adoption_cost': 5000,          # Trivial cost
        'operating_cost_reduction': 0.80 # 80% reduction in labor needs
    }
}

# Task-based AI framework
TASK_CONFIG = {
    'task_types': ['routine_cognitive', 'routine_manual', 'nonroutine_cognitive', 'nonroutine_manual'],
    'task_distribution': {
        'low': {
            'routine_manual': 0.6,
            'routine_cognitive': 0.2,
            'nonroutine_manual': 0.15,
            'nonroutine_cognitive': 0.05
        },
        'medium': {
            'routine_manual': 0.2,
            'routine_cognitive': 0.4,
            'nonroutine_manual': 0.2,
            'nonroutine_cognitive': 0.2
        },
        'high': {
            'routine_manual': 0.05,
            'routine_cognitive': 0.15,
            'nonroutine_manual': 0.2,
            'nonroutine_cognitive': 0.6
        }
    },
    'automation_susceptibility': {
        'routine_manual': 0.95,         # Near-total automation potential
        'routine_cognitive': 0.90,      # Near-total automation (AI excels here)
        'nonroutine_manual': 0.60,      # Moderate automation (robotics improving)
        'nonroutine_cognitive': 0.40    # Lower but still significant (creative AI)
    },
    'augmentation_potential': {
        'routine_manual': 0.1,          # Low augmentation potential
        'routine_cognitive': 0.3,       # Medium augmentation potential
        'nonroutine_manual': 0.2,       # Low-medium augmentation
        'nonroutine_cognitive': 0.7     # High augmentation potential
    }
}

# Market parameters
MARKET_CONFIG = {
    'labor': {
        'matching_efficiency': 0.5,     # Probability of successful match
        'search_friction': 0.2,         # Search costs and delays
        'wage_stickiness': 0.3          # Resistance to wage changes
    },
    'goods': {
        'price_adjustment_speed': 0.15,
        'demand_elasticity': 1.2,
        'initial_price': 100
    }
}

# Government policy parameters
GOVERNMENT_CONFIG = {
    'ubi': {
        'amount': 0,                    # Universal basic income per period
        'tax_rate': 0.0                 # Income tax rate to fund UBI
    },
    'retraining': {
        'enabled': False,
        'cost_per_worker': 2000,        # Cost of retraining program
        'duration': 10,                 # Periods required for retraining
        'success_rate': 0.7,            # Probability of successful skill upgrade
        'skill_improvement': 0.3,       # Skill increase upon completion
        'subsidy_rate': 1.0             # Fraction of cost covered by government
    },
    'unemployment_insurance': {
        'replacement_rate': 0.5,        # Fraction of previous wage
        'duration': 20,                 # Maximum periods of benefits
        'tax_rate': 0.02                # Tax rate to fund UI
    }
}

# Visualization parameters
VIZ_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 300,
    'style': 'seaborn-v0_8-darkgrid',
    'color_palette': 'Set2',
    'font_size': 11,
    'save_format': ['png', 'pdf']
}

# Report parameters
REPORT_CONFIG = {
    'include_methodology': True,
    'include_sensitivity_analysis': True,
    'include_statistical_tests': True,
    'output_formats': ['html', 'pdf'],
    'sections': [
        'executive_summary',
        'model_overview',
        'scenario_description',
        'key_findings',
        'time_series_analysis',
        'distribution_analysis',
        'policy_recommendations',
        'technical_appendix'
    ]
}

# Metrics to track
METRICS = [
    'unemployment_rate',
    'mean_wage',
    'median_wage',
    'gini_coefficient',
    'gdp',
    'labor_share',
    'productivity',
    'ai_adoption_rate',
    'skill_distribution',
    'wage_by_skill',
    'firm_profits',
    'consumer_welfare'
]
