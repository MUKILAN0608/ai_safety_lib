"""Pytest configuration and fixtures."""

import pytest
import numpy as np
from typing import Dict, List


@pytest.fixture
def sample_predictions():
    """Sample model predictions for testing."""
    np.random.seed(42)
    return np.random.uniform(0.5, 0.95, 100).tolist()


@pytest.fixture
def sample_reference_data():
    """Sample reference dataset for testing."""
    np.random.seed(42)
    return {
        "feature_1": np.random.normal(0, 1, 100).tolist(),
        "feature_2": np.random.normal(0, 1, 100).tolist(),
        "feature_3": np.random.uniform(0, 1, 100).tolist(),
    }


@pytest.fixture
def sample_current_data():
    """Sample current dataset (with slight drift) for testing."""
    np.random.seed(43)
    return {
        "feature_1": np.random.normal(0.1, 1.05, 100).tolist(),
        "feature_2": np.random.normal(0, 1, 100).tolist(),
        "feature_3": np.random.uniform(0.05, 1.05, 100).tolist(),
    }


@pytest.fixture
def low_confidence_predictions():
    """Low confidence predictions for testing."""
    np.random.seed(42)
    return np.random.uniform(0.3, 0.6, 100).tolist()
