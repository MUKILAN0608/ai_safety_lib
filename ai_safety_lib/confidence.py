"""Confidence monitoring and uncertainty quantification module."""

from typing import List, Tuple, Dict, Any
import numpy as np
from .types import ModelConfidence, SafetyMetric, SafetyLevel


class ConfidenceMonitor:
    """Monitor and track model confidence metrics."""
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize confidence monitor.
        
        Args:
            confidence_threshold: Threshold for acceptable confidence level
        """
        self.confidence_threshold = confidence_threshold
    
    def calculate_confidence(self, predictions: List[float]) -> float:
        """Calculate mean confidence from predictions."""
        if not predictions:
            return 0.0
        return float(np.mean(predictions))
    
    def calculate_uncertainty(self, predictions: List[float]) -> List[float]:
        """Calculate uncertainty for predictions."""
        return [1.0 - p for p in predictions]
    
    def assess_confidence(self, predictions: List[float]) -> SafetyMetric:
        """Assess confidence level and return safety metric."""
        mean_conf = self.calculate_confidence(predictions)
        
        if mean_conf < self.confidence_threshold * 0.5:
            level = SafetyLevel.CRITICAL
        elif mean_conf < self.confidence_threshold:
            level = SafetyLevel.WARNING
        else:
            level = SafetyLevel.SAFE
        
        return SafetyMetric(
            name="model_confidence",
            value=mean_conf,
            threshold=self.confidence_threshold,
            level=level
        )
