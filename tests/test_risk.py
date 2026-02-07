"""Tests for risk assessment module."""

import pytest
from ai_safety_lib.risk import RiskAssessor
from ai_safety_lib.types import SafetyMetric, SafetyLevel


class TestRiskAssessor:
    """Test suite for RiskAssessor class."""
    
    def test_initialization(self):
        """Test RiskAssessor initialization."""
        assessor = RiskAssessor()
        assert assessor.weights is not None
        assert "confidence" in assessor.weights
    
    def test_calculate_risk_score_safe(self):
        """Test risk score calculation for safe metrics."""
        assessor = RiskAssessor()
        metrics = {
            "confidence": SafetyMetric("confidence", 0.8, 0.7, SafetyLevel.SAFE),
            "drift": SafetyMetric("drift", 0.1, 0.3, SafetyLevel.SAFE),
        }
        score = assessor.calculate_risk_score(metrics)
        assert 0.0 <= score <= 1.0
        assert score < 0.3  # Should be low risk
    
    def test_calculate_risk_score_critical(self):
        """Test risk score calculation for critical metrics."""
        assessor = RiskAssessor()
        metrics = {
            "confidence": SafetyMetric("confidence", 0.3, 0.7, SafetyLevel.CRITICAL),
            "drift": SafetyMetric("drift", 0.5, 0.3, SafetyLevel.CRITICAL),
        }
        score = assessor.calculate_risk_score(metrics)
        assert score >= 0.7  # Should be high risk
    
    def test_assess_risk(self):
        """Test comprehensive risk assessment."""
        assessor = RiskAssessor()
        metrics = {
            "confidence": SafetyMetric("confidence", 0.6, 0.7, SafetyLevel.WARNING),
            "drift": SafetyMetric("drift", 0.2, 0.3, SafetyLevel.SAFE),
        }
        assessment = assessor.assess_risk(metrics)
        
        assert assessment.overall_risk >= 0.0
        assert assessment.overall_risk <= 1.0
        assert assessment.risk_level in [SafetyLevel.SAFE, SafetyLevel.WARNING, SafetyLevel.CRITICAL]
        assert isinstance(assessment.component_risks, dict)
        assert isinstance(assessment.recommendations, list)
    
    def test_recommendations_generation(self):
        """Test that recommendations are generated for critical metrics."""
        assessor = RiskAssessor()
        metrics = {
            "confidence": SafetyMetric("confidence", 0.3, 0.7, SafetyLevel.CRITICAL),
        }
        assessment = assessor.assess_risk(metrics)
        assert len(assessment.recommendations) > 0
        assert any("CRITICAL" in rec for rec in assessment.recommendations)
