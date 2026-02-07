# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-07

### Added
- **Explainability Module**: Feature importance calculation and SHAP-like analysis
- **Fairness Module**: Demographic parity, equal opportunity, and disparate impact metrics
- **Monitoring Module**: Real-time performance monitoring with alerts
- **Configuration Management**: YAML/JSON config support with environment variables
- **FastAPI Server**: Production-ready REST API for all safety features
- **Comprehensive Test Suite**: >80% code coverage with pytest
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Docker Support**: Production Dockerfile and docker-compose with monitoring
- **Examples**: Comprehensive examples for all major features
- **API Endpoints**: 
  - `/evaluate` - Safety evaluation
  - `/metrics` - Performance metrics recording
  - `/fairness/analyze` - Fairness analysis
  - `/explain` - Explainability analysis
  - `/alerts` - Alert management
  - `/audit-log` - Audit trail

### Changed
- Updated package version to 0.2.0
- Enhanced `setup.py` with additional classifiers and entry points
- Improved documentation with comprehensive examples
- Extended `requirements.txt` with API dependencies

### Fixed
- Type hints across all modules
- Error handling in API endpoints
- Configuration validation

## [0.1.0] - 2026-02-07

### Added
- Initial release
- Core safety modules:
  - Confidence monitoring
  - Drift detection
  - Risk assessment
  - Safety gate orchestration
- Basic utility functions
- README documentation
- Setup configuration
- Demo script

[0.2.0]: https://github.com/MUKILAN0608/ai_safety_lib/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/MUKILAN0608/ai_safety_lib/releases/tag/v0.1.0
