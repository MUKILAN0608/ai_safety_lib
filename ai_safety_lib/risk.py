"""Risk assessment and scoring module."""

from typing import List, Dict, Any
from dataclasses import dataclass
from .types import SafetyMetric, SafetyLevel


@dataclass
class RiskAssessment:
    """Risk assessment result."""

    overall_risk: float
    risk_level: SafetyLevel
    component_risks: Dict[str, float]
    recommendations: List[str]


class RiskAssessor:
    """Assess and score model risks."""

    def __init__(self):
        """Initialize risk assessor."""
        self.weights = {
            "confidence": 0.4,
            "drift": 0.3,
            "performance": 0.2,
            "fairness": 0.1,
        }

    def calculate_risk_score(self, metrics: Dict[str, SafetyMetric]) -> float:
        """Calculate weighted risk score from multiple metrics."""
        risk_score = 0.0

        for metric_name, metric in metrics.items():
            weight = self.weights.get(metric_name, 0.1)

            # Convert safety level to risk (higher level = higher risk)
            if metric.level == SafetyLevel.SAFE:
                metric_risk = 0.0
            elif metric.level == SafetyLevel.WARNING:
                metric_risk = 0.5
            else:  # CRITICAL
                metric_risk = 1.0

            risk_score += weight * metric_risk

        return min(risk_score, 1.0)

    def assess_risk(self, metrics: Dict[str, SafetyMetric]) -> RiskAssessment:
        """Perform comprehensive risk assessment."""
        overall_risk = self.calculate_risk_score(metrics)

        if overall_risk < 0.3:
            level = SafetyLevel.SAFE
        elif overall_risk < 0.7:
            level = SafetyLevel.WARNING
        else:
            level = SafetyLevel.CRITICAL

        component_risks = {
            name: (
                1.0
                if metric.level == SafetyLevel.CRITICAL
                else 0.5 if metric.level == SafetyLevel.WARNING else 0.0
            )
            for name, metric in metrics.items()
        }

        recommendations = self._generate_recommendations(metrics, level)

        return RiskAssessment(
            overall_risk=overall_risk,
            risk_level=level,
            component_risks=component_risks,
            recommendations=recommendations,
        )

    def _generate_recommendations(
        self, metrics: Dict[str, SafetyMetric], risk_level: SafetyLevel
    ) -> List[str]:
        """Generate recommendations based on risk assessment."""
        recommendations = []

        for metric_name, metric in metrics.items():
            if metric.level == SafetyLevel.CRITICAL:
                recommendations.append(f"CRITICAL: Investigate {metric_name} immediately")
            elif metric.level == SafetyLevel.WARNING:
                recommendations.append(f"Review {metric_name} metrics")

        if risk_level == SafetyLevel.CRITICAL:
            recommendations.append("Consider retraining or adjusting model parameters")

        return recommendations
