"""Tests for safety gate module."""

import pytest
from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.types import SafetyLevel


class TestSafetyGate:
    """Test suite for SafetyGate class."""
    
    def test_initialization(self):
        """Test SafetyGate initialization."""
        gate = SafetyGate(
            confidence_threshold=0.75,
            drift_threshold=0.25,
            allow_warning=True
        )
        assert gate.confidence_monitor.confidence_threshold == 0.75
        assert gate.drift_detector.drift_threshold == 0.25
        assert gate.allow_warning is True
    
    def test_evaluate(self, sample_predictions, sample_reference_data, sample_current_data):
        """Test safety evaluation."""
        gate = SafetyGate()
        assessment = gate.evaluate(
            predictions=sample_predictions,
            reference_data=sample_reference_data,
            current_data=sample_current_data,
            dataset_name="test"
        )
        
        assert assessment.overall_risk >= 0.0
        assert assessment.overall_risk <= 1.0
        assert assessment.risk_level in [SafetyLevel.SAFE, SafetyLevel.WARNING, SafetyLevel.CRITICAL]
    
    def test_should_deploy_safe(self, sample_predictions, sample_reference_data):
        """Test deployment decision for safe models."""
        gate = SafetyGate(confidence_threshold=0.5, drift_threshold=0.5)
        assessment = gate.evaluate(
            predictions=sample_predictions,
            reference_data=sample_reference_data,
            current_data=sample_reference_data,  # No drift
            dataset_name="test"
        )
        assert gate.should_deploy(assessment) is True
    
    def test_should_deploy_critical(self):
        """Test deployment decision for critical models."""
        gate = SafetyGate()
        low_predictions = [0.2, 0.25, 0.3] * 10
        ref_data = {"f1": [0.0] * 30}
        curr_data = {"f1": [10.0] * 30}  # Extreme drift
        
        assessment = gate.evaluate(
            predictions=low_predictions,
            reference_data=ref_data,
            current_data=curr_data,
            dataset_name="test"
        )
        assert gate.should_deploy(assessment) is False
    
    def test_should_deploy_warning_allowed(self, sample_predictions, sample_reference_data, sample_current_data):
        """Test deployment with warning level when allowed."""
        gate = SafetyGate(allow_warning=True)
        assessment = gate.evaluate(
            predictions=sample_predictions,
            reference_data=sample_reference_data,
            current_data=sample_current_data,
            dataset_name="test"
        )
        
        # Should deploy even if warning (if warning level)
        if assessment.risk_level == SafetyLevel.WARNING:
            assert gate.should_deploy(assessment) is True
    
    def test_audit_log(self, sample_predictions, sample_reference_data, sample_current_data):
        """Test that evaluations are logged."""
        gate = SafetyGate()
        initial_log_count = len(gate.get_audit_log())
        
        gate.evaluate(
            predictions=sample_predictions,
            reference_data=sample_reference_data,
            current_data=sample_current_data,
            dataset_name="test"
        )
        
        assert len(gate.get_audit_log()) == initial_log_count + 1
        log_entry = gate.get_audit_log()[-1]
        assert "overall_risk" in log_entry
        assert "risk_level" in log_entry
