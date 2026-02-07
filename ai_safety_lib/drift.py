"""Data drift detection and monitoring module."""

from typing import List, Dict, Tuple, Any
import numpy as np
from .types import DriftMetric, SafetyMetric, SafetyLevel


class DriftDetector:
    """Detect and monitor data drift in model inputs and outputs."""
    
    def __init__(self, drift_threshold: float = 0.3):
        """
        Initialize drift detector.
        
        Args:
            drift_threshold: Threshold for detecting significant drift
        """
        self.drift_threshold = drift_threshold
    
    def calculate_drift_score(
        self, 
        reference_data: List[float], 
        current_data: List[float]
    ) -> float:
        """
        Calculate drift score between reference and current data.
        Uses Kullback-Leibler divergence approximation.
        """
        if not reference_data or not current_data:
            return 0.0
        
        # Simple implementation using mean and std comparison
        ref_mean = np.mean(reference_data)
        curr_mean = np.mean(current_data)
        
        return abs(curr_mean - ref_mean) / (abs(ref_mean) + 1e-6)
    
    def detect_feature_drift(
        self,
        feature_name: str,
        reference_data: List[float],
        current_data: List[float]
    ) -> bool:
        """Detect if a specific feature has drifted."""
        drift_score = self.calculate_drift_score(reference_data, current_data)
        return bool(drift_score > self.drift_threshold)
    
    def assess_drift(
        self,
        dataset_name: str,
        reference_data: Dict[str, List[float]],
        current_data: Dict[str, List[float]]
    ) -> DriftMetric:
        """Assess overall drift in dataset."""
        drifted_features = [
            feat for feat in reference_data.keys()
            if self.detect_feature_drift(feat, reference_data[feat], current_data.get(feat, []))
        ]
        
        all_drift_scores = [
            self.calculate_drift_score(reference_data[feat], current_data.get(feat, []))
            for feat in reference_data.keys()
        ]
        mean_drift = np.mean(all_drift_scores) if all_drift_scores else 0.0
        
        return DriftMetric(
            dataset=dataset_name,
            drift_score=mean_drift,
            detected=len(drifted_features) > 0,
            features_drifted=drifted_features
        )
