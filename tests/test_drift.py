"""Tests for drift detection module."""

import pytest
import numpy as np
from ai_safety_lib.drift import DriftDetector


class TestDriftDetector:
    """Test suite for DriftDetector class."""

    def test_initialization(self):
        """Test DriftDetector initialization."""
        detector = DriftDetector(drift_threshold=0.4)
        assert detector.drift_threshold == 0.4

    def test_calculate_drift_score(self, sample_reference_data, sample_current_data):
        """Test drift score calculation."""
        detector = DriftDetector()
        score = detector.calculate_drift_score(
            sample_reference_data["feature_1"], sample_current_data["feature_1"]
        )
        assert score >= 0.0

    def test_detect_feature_drift(self, sample_reference_data, sample_current_data):
        """Test feature drift detection."""
        detector = DriftDetector(drift_threshold=0.05)
        drifted = detector.detect_feature_drift(
            "feature_1",
            sample_reference_data["feature_1"],
            sample_current_data["feature_1"],
        )
        assert isinstance(drifted, bool)

    def test_assess_drift(self, sample_reference_data, sample_current_data):
        """Test overall drift assessment."""
        detector = DriftDetector()
        metric = detector.assess_drift("test_dataset", sample_reference_data, sample_current_data)
        assert metric.dataset == "test_dataset"
        assert metric.drift_score >= 0.0
        assert isinstance(metric.detected, bool)
        assert isinstance(metric.features_drifted, list)

    def test_no_drift_same_data(self, sample_reference_data):
        """Test that identical data shows no drift."""
        detector = DriftDetector()
        metric = detector.assess_drift("test_dataset", sample_reference_data, sample_reference_data)
        assert metric.drift_score < 0.01  # Should be very close to 0

    def test_empty_data(self):
        """Test handling of empty data."""
        detector = DriftDetector()
        score = detector.calculate_drift_score([], [])
        assert score == 0.0
