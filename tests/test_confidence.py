"""Tests for confidence monitoring module."""

import pytest
from ai_safety_lib.confidence import ConfidenceMonitor
from ai_safety_lib.types import SafetyLevel


class TestConfidenceMonitor:
    """Test suite for ConfidenceMonitor class."""

    def test_initialization(self):
        """Test ConfidenceMonitor initialization."""
        monitor = ConfidenceMonitor(confidence_threshold=0.8)
        assert monitor.confidence_threshold == 0.8

    def test_calculate_confidence(self, sample_predictions):
        """Test confidence calculation."""
        monitor = ConfidenceMonitor()
        confidence = monitor.calculate_confidence(sample_predictions)
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Our fixture should have reasonably high confidence

    def test_calculate_uncertainty(self, sample_predictions):
        """Test uncertainty calculation."""
        monitor = ConfidenceMonitor()
        uncertainties = monitor.calculate_uncertainty(sample_predictions)
        assert len(uncertainties) == len(sample_predictions)
        assert all(0.0 <= u <= 1.0 for u in uncertainties)

    def test_assess_confidence_safe(self, sample_predictions):
        """Test that high confidence predictions are marked as SAFE."""
        monitor = ConfidenceMonitor(confidence_threshold=0.6)
        metric = monitor.assess_confidence(sample_predictions)
        assert metric.level == SafetyLevel.SAFE
        assert metric.name == "model_confidence"

    def test_assess_confidence_warning(self, low_confidence_predictions):
        """Test that medium confidence predictions are marked WARNING."""
        monitor = ConfidenceMonitor(confidence_threshold=0.8)
        metric = monitor.assess_confidence(low_confidence_predictions)
        assert metric.level == SafetyLevel.WARNING

    def test_assess_confidence_critical(self):
        """Test that very low confidence predictions are marked CRITICAL."""
        monitor = ConfidenceMonitor(confidence_threshold=0.7)
        very_low_predictions = [0.2, 0.25, 0.3, 0.28]
        metric = monitor.assess_confidence(very_low_predictions)
        assert metric.level == SafetyLevel.CRITICAL

    def test_empty_predictions(self):
        """Test handling of empty predictions list."""
        monitor = ConfidenceMonitor()
        confidence = monitor.calculate_confidence([])
        assert confidence == 0.0
