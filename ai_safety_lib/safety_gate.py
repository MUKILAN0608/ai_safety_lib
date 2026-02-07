"""Safety gate module for enforcing safety decisions."""

from typing import Dict, List, Any, Optional
from .types import SafetyMetric, SafetyLevel
from .confidence import ConfidenceMonitor
from .drift import DriftDetector
from .risk import RiskAssessor, RiskAssessment


class SafetyGate:
    """Main safety gate for monitoring and controlling model deployment."""
    
    def __init__(
        self,
        confidence_threshold: float = 0.7,
        drift_threshold: float = 0.3,
        allow_warning: bool = False
    ):
        """
        Initialize safety gate.
        
        Args:
            confidence_threshold: Threshold for model confidence
            drift_threshold: Threshold for data drift
            allow_warning: Whether to allow models with warning level
        """
        self.confidence_monitor = ConfidenceMonitor(confidence_threshold)
        self.drift_detector = DriftDetector(drift_threshold)
        self.risk_assessor = RiskAssessor()
        self.allow_warning = allow_warning
        self.audit_log: List[Dict[str, Any]] = []
    
    def evaluate(
        self,
        predictions: List[float],
        reference_data: Dict[str, List[float]],
        current_data: Dict[str, List[float]],
        dataset_name: str = "default"
    ) -> RiskAssessment:
        """
        Evaluate safety of model predictions.
        
        Args:
            predictions: Model predictions
            reference_data: Reference dataset for drift detection
            current_data: Current dataset for drift detection
            dataset_name: Name of the dataset
            
        Returns:
            RiskAssessment with overall safety evaluation
        """
        # Calculate individual metrics
        confidence_metric = self.confidence_monitor.assess_confidence(predictions)
        drift_metric = self.drift_detector.assess_drift(
            dataset_name, reference_data, current_data
        )
        
        # Build metrics dictionary
        metrics = {
            "confidence": confidence_metric,
            "drift": SafetyMetric(
                name="drift",
                value=drift_metric.drift_score,
                threshold=self.drift_detector.drift_threshold,
                level=SafetyLevel.CRITICAL if drift_metric.detected else SafetyLevel.SAFE
            )
        }
        
        # Get risk assessment
        assessment = self.risk_assessor.assess_risk(metrics)
        
        # Log the evaluation
        self._log_evaluation(assessment, metrics)
        
        return assessment
    
    def should_deploy(self, assessment: RiskAssessment) -> bool:
        """
        Determine if model should be deployed based on risk assessment.
        
        Args:
            assessment: Risk assessment result
            
        Returns:
            True if model should be deployed, False otherwise
        """
        if assessment.risk_level == SafetyLevel.SAFE:
            return True
        elif assessment.risk_level == SafetyLevel.WARNING:
            return self.allow_warning
        else:
            return False
    
    def _log_evaluation(
        self,
        assessment: RiskAssessment,
        metrics: Dict[str, SafetyMetric]
    ) -> None:
        """Log the evaluation for audit purposes."""
        log_entry = {
            "overall_risk": assessment.overall_risk,
            "risk_level": assessment.risk_level.value,
            "component_risks": assessment.component_risks,
            "metrics": {
                name: {
                    "value": metric.value,
                    "level": metric.level.value
                }
                for name, metric in metrics.items()
            }
        }
        self.audit_log.append(log_entry)
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get audit log of evaluations."""
        return self.audit_log
