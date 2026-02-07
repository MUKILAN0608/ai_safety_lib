# AI Safety Library

A comprehensive Python library for AI safety monitoring, risk assessment, and deployment safety gates.

## Features

- **Confidence Monitoring**: Track and assess model prediction confidence
- **Drift Detection**: Monitor data drift on input and output distributions  
- **Risk Assessment**: Comprehensive risk scoring across multiple safety dimensions
- **Safety Gates**: Control model deployment based on safety thresholds
- **Audit Logging**: Complete audit trail of all safety evaluations

## Installation

### From Source
```bash
git clone https://github.com/yourusername/ai_safety_lib.git
cd ai_safety_lib
pip install -e .
```

### From PyPI (coming soon)
```bash
pip install ai-safety-lib
```

## Quick Start

```python
from ai_safety_lib.safety_gate import SafetyGate
import numpy as np

# Initialize safety gate
safety_gate = SafetyGate(
    confidence_threshold=0.7,
    drift_threshold=0.3,
    allow_warning=False
)

# Your model predictions
predictions = [0.85, 0.92, 0.78, 0.88, ...]

# Reference and current datasets for drift detection
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

# Check deployment eligibility
if safety_gate.should_deploy(assessment):
    print("Safe to deploy!")
else:
    print(f"Deployment blocked. Risk level: {assessment.risk_level}")
```

## Module Overview

### `confidence.py`
Monitors model prediction confidence and uncertainty quantification.

**Key Classes:**
- `ConfidenceMonitor`: Assess confidence levels from predictions

### `drift.py`
Detects data drift in input and output distributions.

**Key Classes:**
- `DriftDetector`: Detect feature and dataset drift

### `risk.py`
Performs comprehensive risk assessment and scoring.

**Key Classes:**
- `RiskAssessor`: Assess overall risk from multiple metrics

### `safety_gate.py`
Main safety gate for controlling model deployment.

**Key Classes:**
- `SafetyGate`: Orchestrate all safety checks and deploy decisions

### `utils.py`
Utility functions for metric processing and reporting.

**Key Functions:**
- `format_assessment_report()`: Generate formatted safety reports
- `save_metrics_to_file()`: Persist metrics
- `normalize_predictions()`: Normalize prediction scores

## Safety Levels

- **SAFE**: Model meets all safety criteria
- **WARNING**: Model has some concerns, deployment restricted
- **CRITICAL**: Model fails safety thresholds, deployment blocked

## Configuration

### SafetyGate Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `confidence_threshold` | 0.7 | Minimum acceptable model confidence |
| `drift_threshold` | 0.3 | Maximum acceptable data drift |
| `allow_warning` | False | Allow deployment with WARNING level |

## Running the Demo

```bash
python demo.py
```

## Development

### Install Development Dependencies
```bash
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest tests/
```

### Code Quality
```bash
black ai_safety_lib/
flake8 ai_safety_lib/
mypy ai_safety_lib/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{ai_safety_lib,
  title={AI Safety Library},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/ai_safety_lib}
}
```

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note:** This is an alpha release. API and functionality may change.
