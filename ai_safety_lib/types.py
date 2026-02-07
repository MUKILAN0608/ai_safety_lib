"""Type definitions and data structures for AI safety monitoring."""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class SafetyLevel(Enum):
    """Enumeration of safety levels."""
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class SafetyMetric:
    """Base class for safety metrics."""
    name: str
    value: float
    threshold: float
    level: SafetyLevel


@dataclass
class ModelConfidence:
    """Model confidence metrics."""
    predictions: List[float]
    uncertainties: List[float]
    mean_confidence: float


@dataclass
class DriftMetric:
    """Data drift detection metrics."""
    dataset: str
    drift_score: float
    detected: bool
    features_drifted: List[str]
