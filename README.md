# AI Safety Library

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, production-ready Python library for AI safety monitoring, risk assessment, fairness evaluation, and explainability analysis.

## Features

### Core Safety Modules
- **Confidence Monitoring**: Track and assess model prediction confidence with uncertainty quantification
- **Drift Detection**: Monitor data distribution shifts using statistical metrics
- **Risk Assessment**: Multi-dimensional risk scoring with component-level analysis
- **Safety Gates**: Automated deployment control based on configurable safety thresholds
- **Audit Logging**: Complete audit trail of all safety evaluations

### Advanced Capabilities
- **Explainability**: Feature importance calculation and SHAP-like analysis
- **Fairness Analysis**: Demographic parity, equal opportunity, and disparate impact metrics
- **Performance Monitoring**: Real-time metrics tracking with automated alerting
- **REST API**: Production-ready FastAPI server with full OpenAPI documentation
- **Configuration Management**: YAML/JSON config support with environment variables
- **Docker Support**: Ready-to-deploy containerized applications

## Installation

### Basic Installation
```bash
pip install ai-safety-lib
```

### With API Server
```bash
pip install ai-safety-lib[api]
```

### Development Installation
```bash
pip install ai-safety-lib[dev]
```

### Full Installation (All Features)
```bash
pip install ai-safety-lib[all]
```

### From Source
```bash
git clone https://github.com/MUKILAN0608/ai_safety_lib.git
cd ai_safety_lib
pip install -e ".[all]"
```

## Quick Start

### Basic Usage

```python
from ai_safety_lib.safety_gate import SafetyGate
import numpy as np

# Initialize safety gate
safety_gate = SafetyGate(
    confidence_threshold=0.7,
    drift_threshold=0.3,
    allow_warning=False
)

# Prepare your data
predictions = [0.85, 0.92, 0.78, 0.88, ...]
reference_data = {
    "feature_1": [...],
    "feature_2": [...]
}
current_data = {
    "feature_1": [...],
    "feature_2": [...]
}

# Evaluate safety
assessment = safety_gate.evaluate(
    predictions=predictions,
    reference_data=reference_data,
    current_data=current_data
)

# Make deployment decision
if safety_gate.should_deploy(assessment):
    print("Safe to deploy!")
else:
    print(f"Deployment blocked. Risk level: {assessment.risk_level}")
```

### Comprehensive Example

```python
from ai_safety_lib import (
    SafetyGate, PerformanceMonitor, 
    FairnessAnalyzer, ExplainabilityAnalyzer
)

# Initialize all components
safety_gate = SafetyGate()
monitor = PerformanceMonitor(alert_callback=lambda x: print(f"Alert: {x.message}"))
fairness = FairnessAnalyzer()
explainer = ExplainabilityAnalyzer()

# 1. Safety Evaluation
assessment = safety_gate.evaluate(predictions, reference_data, current_data)

# 2. Performance Monitoring
monitor.record_metrics(
    accuracy=0.85,
    latency_ms=125.5,
    error_rate=0.03
)

# 3. Fairness Analysis
fairness_reports = fairness.comprehensive_fairness_check(
    predictions=predictions,
    protected_groups=groups,
    true_labels=labels
)

# 4. Explainability
feature_importance = explainer.calculate_feature_importance(
    feature_values=current_data,
    predictions=predictions
)
```

## API Server

### Start the Server

```bash
# Development mode
python api_server.py

# Production mode with uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4

# Using Docker
docker-compose up
```

### API Endpoints

- **POST** `/evaluate` - Safety evaluation
- **POST** `/metrics` - Record performance metrics
- **GET** `/metrics/summary` - Get metrics summary
- **GET** `/alerts` - Retrieve alerts
- **POST** `/fairness/analyze` - Fairness analysis
- **POST** `/explain` - Generate explanations
- **GET** `/audit-log` - Get audit trail

### Interactive Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Call

```python
import requests

response = requests.post(
    "http://localhost:8000/evaluate",
    json={
        "predictions": [0.8, 0.9, 0.85],
        "reference_data": {"feature_1": [1.0, 2.0, 1.5]},
        "current_data": {"feature_1": [1.1, 2.1, 1.6]}
    }
)

result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Should Deploy: {result['should_deploy']}")
```

## Module Overview

### Safety Modules

| Module | Description |
|--------|-------------|
| `confidence.py` | Model confidence and uncertainty monitoring |
| `drift.py` | Data drift detection using statistical methods |
| `risk.py` | Multi-dimensional risk assessment and scoring |
| `safety_gate.py` | Deployment safety gates and orchestration |

### Advanced Modules

| Module | Description |
|--------|-------------|
| `explainability.py` | Feature importance and SHAP-like explanations |
| `fairness.py` | Bias detection and fairness metrics |
| `monitoring.py` | Real-time performance monitoring with alerts |
| `config.py` | Configuration management system |

## Configuration

### Using Configuration Files

```yaml
# config.yaml
safety:
  confidence_threshold: 0.7
  drift_threshold: 0.3
  allow_warning: false
  fairness_threshold: 0.8

monitoring:
  enable_alerts: true
  alert_thresholds:
    accuracy: 0.75
    error_rate: 0.1
    latency_ms: 500.0
```

```python
from ai_safety_lib.config import ConfigManager

config_manager = ConfigManager()
config = config_manager.load_from_file("config.yaml")

# Use config with safety gate
safety_gate = SafetyGate(
    confidence_threshold=config.safety.confidence_threshold,
    drift_threshold=config.safety.drift_threshold
)
```

### Environment Variables

```bash
export SAFETY_CONFIDENCE_THRESHOLD=0.75
export SAFETY_DRIFT_THRESHOLD=0.25
export MONITORING_ENABLE_ALERTS=true
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t ai-safety-api .

# Run container
docker run -p 8000:8000 ai-safety-api
```

### Docker Compose (with Monitoring)

```bash
docker-compose up
```

Includes:
- AI Safety API (port 8000)
- Prometheus (port 9090)
- Grafana (port 3000)

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=ai_safety_lib --cov-report=html

# Run specific test file
pytest tests/test_safety_gate.py -v
```

## Examples

Comprehensive examples are available in the `examples/` directory:

- `comprehensive_example.py` - Full feature demonstration
- `config_example.py` - Configuration management
- `api_example.py` - API server usage

Run any example:
```bash
python examples/comprehensive_example.py
```

## Documentation

- **[API Documentation](docs/API.md)** - Complete REST API reference
- **[Contributing Guide](CONTRIBUTING.md)** - Development guidelines
- **[Changelog](CHANGELOG.md)** - Version history

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/MUKILAN0608/ai_safety_lib.git
cd ai_safety_lib

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black ai_safety_lib tests examples
isort ai_safety_lib tests examples

# Lint
flake8 ai_safety_lib
mypy ai_safety_lib
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by best practices in MLOps and responsible AI
- Built with modern Python tooling and frameworks
- Designed for production deployment scenarios

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/MUKILAN0608/ai_safety_lib/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MUKILAN0608/ai_safety_lib/discussions)

## 🗺️ Roadmap

- [ ] Integration with popular ML frameworks (scikit-learn, PyTorch, TensorFlow)
- [ ] Advanced drift detection algorithms (Kolmogorov-Smirnov, PSI)
- [ ] Model performance degradation prediction
- [ ] Automated retraining recommendations
- [ ] Dashboard UI for visualization
- [ ] Cloud provider integrations (AWS, Azure, GCP)

---

**Made for safer AI systems**
