"""Explainability and interpretability module."""

from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class FeatureImportance:
    """Feature importance result."""

    feature_name: str
    importance_score: float
    rank: int


@dataclass
class ExplanationResult:
    """Explanation result for a prediction."""

    prediction_index: int
    predicted_value: float
    feature_contributions: Dict[str, float]
    top_features: List[FeatureImportance]


class ExplainabilityAnalyzer:
    """Analyze and explain model predictions."""

    def __init__(self, feature_names: Optional[List[str]] = None):
        """
        Initialize explainability analyzer.

        Args:
            feature_names: Names of features in the model
        """
        self.feature_names = feature_names or []

    def calculate_feature_importance(
        self, feature_values: Dict[str, List[float]], predictions: List[float]
    ) -> List[FeatureImportance]:
        """
        Calculate feature importance using correlation analysis.

        Args:
            feature_values: Dictionary of feature names to their values
            predictions: Model predictions

        Returns:
            List of FeatureImportance objects
        """
        importances = []

        for feature_name, values in feature_values.items():
            if len(values) != len(predictions):
                continue

            # Calculate correlation as a simple importance measure
            correlation = np.corrcoef(values, predictions)[0, 1]
            importance_score = abs(correlation) if not np.isnan(correlation) else 0.0

            importances.append({"feature_name": feature_name, "importance_score": importance_score})

        # Sort by importance
        importances.sort(key=lambda x: x["importance_score"], reverse=True)

        # Create FeatureImportance objects with ranks
        return [
            FeatureImportance(
                feature_name=imp["feature_name"],
                importance_score=imp["importance_score"],
                rank=idx + 1,
            )
            for idx, imp in enumerate(importances)
        ]

    def explain_prediction(
        self,
        prediction_index: int,
        prediction_value: float,
        feature_values: Dict[str, float],
        feature_importances: List[FeatureImportance],
        top_k: int = 5,
    ) -> ExplanationResult:
        """
        Explain a single prediction.

        Args:
            prediction_index: Index of the prediction
            prediction_value: Predicted value
            feature_values: Feature values for this prediction
            feature_importances: Pre-calculated feature importances
            top_k: Number of top features to include

        Returns:
            ExplanationResult with explanation details
        """
        # Calculate feature contributions (weighted by importance and value)
        contributions = {}
        for feat_imp in feature_importances:
            feat_name = feat_imp.feature_name
            if feat_name in feature_values:
                contribution = feat_imp.importance_score * feature_values[feat_name]
                contributions[feat_name] = contribution

        # Get top features
        top_features = feature_importances[:top_k]

        return ExplanationResult(
            prediction_index=prediction_index,
            predicted_value=prediction_value,
            feature_contributions=contributions,
            top_features=top_features,
        )

    def generate_explanation_report(
        self, explanation: ExplanationResult, verbose: bool = True
    ) -> str:
        """Generate human-readable explanation report."""
        report = []
        report.append(f"Explanation for Prediction #{explanation.prediction_index}")
        report.append(f"Predicted Value: {explanation.predicted_value:.4f}")
        report.append("\nTop Contributing Features:")

        for feat in explanation.top_features:
            contrib = explanation.feature_contributions.get(feat.feature_name, 0.0)
            report.append(
                f"  {feat.rank}. {feat.feature_name}: "
                f"importance={feat.importance_score:.4f}, "
                f"contribution={contrib:.4f}"
            )

        if verbose and len(explanation.feature_contributions) > len(explanation.top_features):
            report.append(
                f"\n... and {len(explanation.feature_contributions) - len(explanation.top_features)} more features"
            )

        return "\n".join(report)


class SHAPAnalyzer:
    """Simplified SHAP-like analysis for model explanations."""

    def __init__(self):
        """Initialize SHAP analyzer."""
        self.baseline_values: Dict[str, float] = {}

    def set_baseline(self, feature_values: Dict[str, List[float]]) -> None:
        """Set baseline (average) values for features."""
        for feature_name, values in feature_values.items():
            self.baseline_values[feature_name] = float(np.mean(values))

    def calculate_shap_values(
        self,
        feature_values: Dict[str, float],
        prediction: float,
        baseline_prediction: float = 0.5,
    ) -> Dict[str, float]:
        """
        Calculate SHAP-like values (simplified).

        Args:
            feature_values: Current feature values
            prediction: Current prediction
            baseline_prediction: Baseline prediction value

        Returns:
            Dictionary of SHAP values per feature
        """
        shap_values = {}
        total_diff = prediction - baseline_prediction

        # Simple attribution: distribute the difference proportionally
        feature_diffs = []
        for feat_name, value in feature_values.items():
            baseline = self.baseline_values.get(feat_name, 0.0)
            diff = abs(value - baseline)
            feature_diffs.append((feat_name, diff))

        total_feature_diff = sum(diff for _, diff in feature_diffs) or 1.0

        for feat_name, diff in feature_diffs:
            shap_values[feat_name] = total_diff * (diff / total_feature_diff)

        return shap_values
