# AI Labor Market Economics Simulator

An educational agent-based model for understanding AI's impact on labor markets, with comprehensive tutorials, scenarios, and automated reporting.

## Overview

This simulation models the economic effects of AI adoption on labor markets, featuring:
- Heterogeneous worker and firm agents
- Task-based AI impact framework (automation vs. augmentation)
- Multiple comparison scenarios
- Publication-quality visualizations
- Automated comprehensive reports
- Interactive educational tutorials

## Key Features

### Economic Model
- **Worker Agents**: Heterogeneous skills, consumption behavior, job search strategies
- **Firm Agents**: Production functions, hiring decisions, AI adoption choices
- **Markets**: Labor matching and goods markets with realistic pricing
- **Government**: Optional policy interventions (UBI, retraining programs)

### AI Impact Modeling
- Task-based framework distinguishing automation from augmentation
- Gradual technology diffusion curves
- Firm-level adoption decisions based on cost-benefit analysis
- Differential effects across skill levels

### Scenarios
1. **Baseline**: No AI adoption (control scenario)
2. **Low AI Adoption**: Conservative diffusion rate
3. **High AI Adoption**: Rapid diffusion rate
4. **AI + Retraining**: High adoption with government retraining programs
5. **Custom**: User-configurable parameters

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-economics

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Run a Basic Simulation

```python
from src.scenarios.runner import ScenarioRunner

# Run baseline scenario
runner = ScenarioRunner()
results = runner.run_scenario('baseline', steps=200)
runner.generate_report(results, output_dir='outputs/reports')
```

### Interactive Tutorial

```bash
jupyter notebook notebooks/tutorial.ipynb
```

## Project Structure

```
ai-economics/
├── src/
│   ├── agents/          # Worker, Firm, Government agents
│   ├── markets/         # Labor and goods markets
│   ├── ai_models/       # AI adoption and impact models
│   ├── scenarios/       # Scenario definitions and runner
│   ├── visualization/   # Plotting and charting utilities
│   └── reports/         # Automated report generation
├── notebooks/           # Interactive Jupyter tutorials
├── docs/               # Documentation and methodology
├── outputs/            # Generated figures and reports
├── tests/              # Unit and integration tests
└── config/             # Configuration files
```

## Documentation

- [Methodology Guide](docs/methodology.md): Detailed explanation of all model assumptions
- [Economic Glossary](docs/glossary.md): Definitions of economic terms
- [Study Guide](docs/study_guide.md): Guided experiments and exercises
- [API Reference](docs/api_reference.md): Code documentation

## Usage Examples

### Compare Multiple Scenarios

```python
from src.scenarios.comparison import ScenarioComparison

comparison = ScenarioComparison()
results = comparison.run_all_scenarios(steps=200)
comparison.create_comparison_report(results)
```

### Custom Scenario

```python
from src.scenarios.custom import CustomScenario

scenario = CustomScenario(
    ai_adoption_rate=0.7,
    automation_intensity=0.6,
    augmentation_intensity=0.4,
    retraining_effectiveness=0.5
)
results = scenario.run(steps=200)
```

## Educational Features

This simulator is designed for learning economics:

1. **Interactive Tutorial**: Step-by-step Jupyter notebook with exercises
2. **Guided Experiments**: Pre-designed experiments to explore key concepts
3. **Comprehensive Documentation**: Theory explained alongside code
4. **Economic Glossary**: Key terms defined with examples
5. **Automated Reports**: Professional reports with explanations of results

## Output Examples

The simulator generates:
- Time series plots of employment, wages, productivity
- Distribution plots showing inequality measures
- Comparison charts across scenarios
- Comprehensive PDF/HTML reports with interpretation
- Raw data exports for further analysis

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this simulator in research or teaching, please cite:

```bibtex
@software{ai_labor_market_sim,
  title = {AI Labor Market Economics Simulator},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/yourusername/ai-economics}
}
```

## References

- Acemoglu, D., & Restrepo, P. (2018). The race between man and machine
- Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change
- Agrawal, A., Gans, J., & Goldfarb, A. (2019). The Economics of Artificial Intelligence

## Contact

For questions or feedback, please open an issue on GitHub.
