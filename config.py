"""
Configuration file for AI Labor Market Simulation - Research-Based Parameters

This file contains research-backed parameters calibrated from:
- McKinsey Global Institute (2023): "The Economic Potential of Generative AI"
- Anthropic (2024): "Economic Policy Responses to AI"
- RAND Corporation (2024-2025): "Macroeconomic Implications of AI"
- Rabobank (2024): "The Economic Impact of AI: Four Scenarios"
- Epoch AI (2024-2025): "The Economic Consequences of Automating Remote Work"
- Tony Blair Institute (2024): "The Impact of AI on the Labour Market"

See docs/RESEARCH_SYNTHESIS.md and docs/RESEARCH_BASED_SCENARIOS.md for details.

Author: Vinay Thakur
Date: October 25, 2025
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
    'initial_savings_mean': 5000,
    'initial_savings_std': 2000,
    'consumption_propensity': 0.8,  # Fraction of income consumed
    'reservation_wage_factor': 0.7,  # Minimum acceptable wage as fraction of previous wage
    'job_search_cost': 50,           # Cost per period of job searching
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

# AI adoption parameters - Research-Based Scenarios
AI_CONFIG = {
    # Scenario 1: Conservative Gradual (Epoch AI 20-Year Timeline)
    # Based on: Epoch AI (2024-2025) - conservative compute scaling
    # Timeline: 20+ years, 34% job tasks remotable, economy doubles
    'conservative_gradual': {
        'adoption_rate': 0.02,              # 2% per year adoption increase
        'diffusion_speed': 0.03,            # Slow diffusion (β in logistic curve)
        'ai_max_adoption': 0.35,            # 35% ceiling (tasks that can be remote)
        'automation_rate_routine': 0.25,    # 25% of routine cognitive tasks
        'automation_rate_manual': 0.05,     # 5% of manual tasks
        'augmentation_rate_nonroutine': 0.15,  # 15% productivity boost
        'adoption_cost': 50000,
        'operating_cost_reduction': 0.10,
        'retraining_effectiveness': 0.30,   # 30% skill upgrade success
        'matching_efficiency': 0.50,
        'separation_rate': 0.02             # 2% quarterly
    },

    # Scenario 2: McKinsey Baseline (Moderate 2030 Effects)
    # Based on: McKinsey Global Institute (June 2023)
    # Key findings: 60-70% work time automatable, $2.6-4.4T annual impact,
    # 0.5-0.9pp productivity growth, 34pp increase in expertise automation
    'mckinsey_baseline': {
        'adoption_rate': 0.05,              # 5% per year - Research-backed
        'diffusion_speed': 0.08,            # Moderate diffusion
        'ai_max_adoption': 0.65,            # 65% ceiling (mid-range of 60-70%)
        'automation_rate_routine': 0.60,    # 60% of routine cognitive - McKinsey
        'automation_rate_manual': 0.15,     # 15% of manual tasks
        'augmentation_rate_nonroutine': 0.34,  # 34% boost - McKinsey expertise jump
        'adoption_cost': 35000,
        'operating_cost_reduction': 0.20,
        'retraining_effectiveness': 0.40,   # 40% with moderate policy
        'matching_efficiency': 0.50,
        'separation_rate': 0.025,           # 2.5% quarterly (elevated)
        'expected_productivity_gain': 0.007,  # 0.7pp annually (mid-range of 0.5-0.9)
        'office_support_displacement': -1600000,  # -1.6M jobs (US scale)
        'management_automation_rate': 0.49  # Up from 16% (2017) to 49% (2023)
    },

    # Scenario 3: TBI Aggressive Displacement (Rapid 2025-2030)
    # Based on: Tony Blair Institute (November 2024)
    # Key findings: +180K unemployment by 2030 (UK), peak 60K-275K/year,
    # +6% GDP by 2035, 23% workforce time savings
    'tbi_aggressive': {
        'adoption_rate': 0.10,              # 10% per year - aggressive
        'diffusion_speed': 0.15,            # Fast diffusion
        'ai_max_adoption': 0.70,            # 70% ceiling
        'automation_rate_routine': 0.70,    # 70% of routine cognitive - TBI
        'automation_rate_manual': 0.20,     # 20% of manual
        'augmentation_rate_nonroutine': 0.30,  # 30% boost
        'adoption_cost': 25000,             # Lower barriers
        'operating_cost_reduction': 0.25,
        'retraining_effectiveness': 0.25,   # 25% - insufficient policy
        'matching_efficiency': 0.35,        # REDUCED - labor market friction
        'separation_rate': 0.035,           # 3.5% quarterly - elevated
        'retraining_delay': 4,              # 4-step delay in skill upgrade
        'expected_unemployment_2030': 180000,  # +180K (UK scale)
        'peak_displacement_per_year': [60000, 275000],  # Range
        'expected_gdp_gain_2035': 0.06,     # +6% by 2035
        'workforce_time_savings': 0.23      # 23% time savings
    },

    # Scenario 4: Anthropic Comprehensive Policy Response
    # Based on: Anthropic (2024) - 9-category graduated policy framework
    # Key findings: $10K/year per trainee, $700M AAA baseline,
    # 3-stage response (workforce dev → fiscal → redistribution)
    'anthropic_policy': {
        # Same AI adoption as McKinsey baseline
        'adoption_rate': 0.05,
        'diffusion_speed': 0.08,
        'ai_max_adoption': 0.65,
        'automation_rate_routine': 0.60,
        'automation_rate_manual': 0.15,
        'augmentation_rate_nonroutine': 0.34,
        'adoption_cost': 35000,
        'operating_cost_reduction': 0.20,

        # Comprehensive policy response - KEY DIFFERENTIATOR
        'retraining_enabled': True,
        'retraining_cost_per_worker': 10000,  # $10K annually - Anthropic estimate
        'retraining_effectiveness': 0.60,   # 60% success with proper funding
        'retraining_coverage': 0.80,        # 80% of displaced workers reached
        'training_grant_amount': 10000,     # Direct grants to workers

        # Phase 1: Workforce Development (Steps 1-50)
        'workforce_development_phase': True,

        # Phase 2: Fiscal Support (Steps 51-100)
        'ui_benefit_replacement_rate': 0.70,  # 70% wage replacement (vs 50% baseline)
        'ui_duration': 26,                  # Extended (26 steps ≈ 2.6 years)
        'automation_adjustment_assistance': True,
        'aaa_budget': 700000000,            # $700M annually baseline
        'aaa_coverage': 0.90,               # 90% of automation-displaced

        # Phase 3: Wealth Redistribution (if unemployment > 15%)
        'wealth_tax_threshold': 0.15,
        'wealth_tax_rate': 0.02,            # 2% annual on business wealth
        'vat_rate': 0.05,                   # 5% value-added tax
        'sovereign_wealth_fund': True,

        # Tax incentives
        'human_capital_tax_credit': 0.20,   # 20% credit for training investment
        'effective_corporate_tax_rate': 0.25,  # Up from 0.21

        # Labor market improvements from policy
        'matching_efficiency': 0.60,        # IMPROVED with AAA programs
        'separation_rate': 0.020,           # 2.0% - kept low by policy
        'retraining_delay': 2               # Faster retraining (2 steps)
    },

    # Scenario 5: RAND Empirical Evidence (Data-Calibrated)
    # Based on: RAND Corporation (2024-2025)
    # Key findings: +$7K per capita GDP by 2035, 0.57 correlation (AI adoption & unemployment),
    # 22-25 year-olds most affected, software/customer service/clerical primary
    'rand_empirical': {
        'adoption_rate': 0.05,              # Moderate
        'diffusion_speed': 0.08,
        'ai_max_adoption': 0.60,
        'automation_rate_routine': 0.55,    # 55% moderate
        'automation_rate_manual': 0.12,
        'augmentation_rate_nonroutine': 0.30,
        'adoption_cost': 35000,
        'operating_cost_reduction': 0.18,
        'retraining_effectiveness': 0.35,   # Modest policy
        'matching_efficiency': 0.45,        # Moderate friction
        'separation_rate': 0.025,

        # RAND-specific calibration targets
        'target_correlation_ai_unemployment': 0.57,  # Empirical correlation
        'target_gdp_per_capita_gain_2035': 7000,  # +$7,000 per capita
        'target_productivity_gain': 0.006,  # 0.6pp annually

        # Occupational exposure (for validation)
        'occupational_exposure': {
            'software_dev': 0.75,
            'customer_service': 0.70,
            'clerical': 0.65,
            'manufacturing': 0.25,
            'healthcare': 0.20
        },

        # Age demographic effects
        'age_22_25_displacement_multiplier': 1.80,  # 80% higher than average
        'age_group_shares': {
            '22-25': 0.12,
            '26-35': 0.25,
            '36-50': 0.40,
            '51-65': 0.23
        }
    }
}

# Task-based AI framework - Updated with McKinsey findings
# McKinsey (2023): Management automation 16% → 49%, 34pp expertise automation jump
TASK_CONFIG = {
    'task_types': ['routine_cognitive', 'routine_manual', 'nonroutine_cognitive', 'nonroutine_manual'],

    # Updated task distributions reflecting research on knowledge work
    'task_distribution': {
        'low': {
            'routine_manual': 0.6,
            'routine_cognitive': 0.2,
            'nonroutine_manual': 0.15,
            'nonroutine_cognitive': 0.05
        },
        'medium': {
            'routine_manual': 0.2,
            'routine_cognitive': 0.5,    # INCREASED - office support heavily routine
            'nonroutine_manual': 0.15,
            'nonroutine_cognitive': 0.15
        },
        'high': {
            # High-skill workers (managers, professionals) - McKinsey paradigm shift
            'routine_manual': 0.05,
            'routine_cognitive': 0.35,   # INCREASED from 0.15 - management tasks
            'nonroutine_manual': 0.10,
            'nonroutine_cognitive': 0.50 # Management + expertise
        }
    },

    # Research-backed automation susceptibility
    # McKinsey: 60-70% of work time automatable
    # TBI: Routine cognitive tasks most affected
    'automation_susceptibility': {
        'routine_manual': 0.80,         # Highly automatable (robots, automation)
        'routine_cognitive': 0.70,      # Highly automatable (60-70% - McKinsey)
        'nonroutine_manual': 0.25,      # Less automatable (complex manual work)
        'nonroutine_cognitive': 0.30    # INCREASED from 0.2 - management now 49% vs 16%
    },

    # McKinsey 34 percentage point jump in expertise automation
    'augmentation_potential': {
        'routine_manual': 0.1,          # Low augmentation potential
        'routine_cognitive': 0.3,       # Medium augmentation
        'nonroutine_manual': 0.2,       # Low-medium augmentation
        'nonroutine_cognitive': 0.7     # High augmentation (expertise jump)
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

# Government policy parameters - Anthropic Framework
# Based on Anthropic (2024): 9-category graduated policy response
GOVERNMENT_CONFIG = {
    'ubi': {
        'amount': 0,                    # Universal basic income per period (not in base scenarios)
        'tax_rate': 0.0                 # Income tax rate to fund UBI
    },

    # Phase 1: Workforce Development (All scenarios)
    # Anthropic: $10,000/year per trainee workforce training grants
    'retraining': {
        'enabled': False,               # Scenario-specific
        'cost_per_worker': 10000,       # $10K annually - Anthropic research-backed
        'duration': 10,                 # Periods required for retraining
        'success_rate': 0.7,            # Probability of successful skill upgrade
        'skill_improvement': 0.3,       # Skill increase upon completion
        'subsidy_rate': 1.0,            # Fraction of cost covered by government
        'coverage_rate': 0.80,          # 80% of displaced workers can access (Anthropic)
        'training_grant': 10000         # Direct grants to workers in training
    },

    # Phase 2: Fiscal Support (Moderate disruption scenarios)
    # Anthropic: TAA-style programs, ~$700M annually baseline
    'unemployment_insurance': {
        'replacement_rate': 0.5,        # Fraction of previous wage (baseline)
        'replacement_rate_enhanced': 0.70,  # Enhanced for Anthropic scenario
        'duration': 20,                 # Maximum periods of benefits (baseline)
        'duration_extended': 26,        # Extended for automation-displaced (2.6 years)
        'tax_rate': 0.02                # Tax rate to fund UI
    },

    'automation_adjustment_assistance': {
        'enabled': False,               # Scenario-specific (Anthropic)
        'budget_baseline': 700000000,   # $700M annually - Anthropic estimate
        'coverage_rate': 0.90,          # 90% of automation-displaced workers
        'additional_benefits': 0.20,    # 20% bonus for automation-related displacement
        'job_search_assistance': True,
        'relocation_assistance': True
    },

    # Phase 3: Wealth Redistribution (Severe disruption)
    # Anthropic: Triggered when displacement severe
    'wealth_redistribution': {
        'enabled': False,               # Triggered if unemployment > threshold
        'unemployment_threshold': 0.15, # Enable if unemployment > 15%
        'wealth_tax_rate': 0.02,        # 2% annual on business wealth
        'vat_rate': 0.05,               # 5% value-added tax
        'sovereign_wealth_fund': False, # Capture AI returns
        'swf_dividend_per_capita': 0    # Annual dividend from SWF
    },

    # Tax incentives for human capital investment (All scenarios)
    'tax_policy': {
        'human_capital_tax_credit': 0.20,  # 20% credit for training investment
        'corporate_tax_rate': 0.21,        # Baseline
        'corporate_tax_rate_reformed': 0.25,  # Anthropic: close profit-shifting
        'profit_shifting_closed': False    # Scenario-specific
    }
}

# Sectoral heterogeneity - Research-based exposure levels
# Based on McKinsey, TBI findings on differential sectoral impacts
SECTOR_CONFIG = {
    'enabled': False,  # Enable for sectoral differentiation
    'sectors': {
        'admin_secretarial': {
            'ai_exposure': 0.85,           # TBI: Highest automation exposure
            'share_of_employment': 0.15,
            'productivity_baseline': 1.0
        },
        'customer_service': {
            'ai_exposure': 0.80,           # McKinsey, RAND: High exposure
            'share_of_employment': 0.12,
            'productivity_baseline': 0.95
        },
        'banking_finance': {
            'ai_exposure': 0.75,           # TBI: Data-rich sectors
            'share_of_employment': 0.08,
            'productivity_baseline': 1.2
        },
        'software_dev': {
            'ai_exposure': 0.75,           # RAND: Surprisingly high
            'share_of_employment': 0.05,
            'productivity_baseline': 1.5
        },
        'professional_services': {
            'ai_exposure': 0.45,           # McKinsey: Management 49%
            'share_of_employment': 0.20,
            'productivity_baseline': 1.3
        },
        'healthcare': {
            'ai_exposure': 0.20,           # RAND, McKinsey: Low automation
            'share_of_employment': 0.15,
            'productivity_baseline': 1.1
        },
        'construction': {
            'ai_exposure': 0.15,           # TBI: Complex manual labor
            'share_of_employment': 0.10,
            'productivity_baseline': 0.9
        },
        'other': {
            'ai_exposure': 0.40,           # Average
            'share_of_employment': 0.15,
            'productivity_baseline': 1.0
        }
    }
}

# Demographic heterogeneity - Age-based effects
# Based on RAND (2024-2025): 22-25 year-olds most affected
DEMOGRAPHIC_CONFIG = {
    'enabled': False,  # Enable for age-differentiated effects
    'age_groups': {
        '22-25': {
            'share_of_workforce': 0.12,
            'displacement_multiplier': 1.80,  # 80% higher than average - RAND
            'reskilling_effectiveness': 1.20,  # Young workers reskill better
            'occupations': ['customer_service', 'clerical', 'software_dev']
        },
        '26-35': {
            'share_of_workforce': 0.25,
            'displacement_multiplier': 1.20,
            'reskilling_effectiveness': 1.10,
            'occupations': ['software_dev', 'professional_services', 'customer_service']
        },
        '36-50': {
            'share_of_workforce': 0.40,
            'displacement_multiplier': 1.00,  # Baseline
            'reskilling_effectiveness': 0.90,
            'occupations': ['professional_services', 'management', 'healthcare']
        },
        '51-65': {
            'share_of_workforce': 0.23,
            'displacement_multiplier': 0.80,   # Lower displacement
            'reskilling_effectiveness': 0.60,  # Harder to reskill
            'occupations': ['management', 'professional_services', 'healthcare']
        }
    }
}

# Validation targets from research
# Used to calibrate and validate simulation results
VALIDATION_TARGETS = {
    'mckinsey_baseline': {
        'productivity_growth_annual': [0.005, 0.009],  # 0.5-0.9pp range
        'work_time_automatable': [0.60, 0.70],         # 60-70%
        'office_support_displacement': -1600000,        # -1.6M jobs
        'management_automation_rate': 0.49,             # 49% (up from 16%)
        'economic_value_annual': [2.6e12, 4.4e12]      # $2.6-4.4 trillion
    },
    'tbi_aggressive': {
        'unemployment_increase_2030': 180000,           # +180K (UK)
        'peak_displacement_annual': [60000, 275000],    # Range per year
        'gdp_gain_2035': 0.06,                         # +6%
        'workforce_time_savings': 0.23,                # 23%
        'jobs_displaced_2050': [1000000, 3000000]      # 1-3M range
    },
    'rand_empirical': {
        'gdp_per_capita_gain_2035': 7000,              # +$7,000
        'ai_unemployment_correlation': 0.57,            # Empirical correlation
        'age_22_25_most_affected': True,
        'occupations_high_exposure': ['software_dev', 'customer_service', 'clerical']
    },
    'anthropic_policy': {
        'training_cost_per_worker': 10000,             # $10K/year
        'aaa_budget_baseline': 700000000,              # $700M annually
        'policy_coverage_rate': 0.80,                  # 80% of displaced
        'unemployment_limit': 0.15                     # Keep below 15% threshold
    },
    'epoch_ai_conservative': {
        'automation_timeline_years': 20,               # 20-year median
        'tasks_remotable_share': 0.34,                 # 34% of job tasks
        'occupations_fully_remote': [0.13, 0.18],      # 13-18% range
        'economy_multiplier': 2.0                      # Economy doubles (conservative)
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
