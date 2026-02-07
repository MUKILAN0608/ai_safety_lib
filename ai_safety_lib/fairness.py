"""Fairness and bias detection module."""

from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass
from enum import Enum


class FairnessMetric(Enum):
    """Types of fairness metrics."""

    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    EQUALIZED_ODDS = "equalized_odds"
    DISPARATE_IMPACT = "disparate_impact"


@dataclass
class BiasReport:
    """Bias analysis report."""

    protected_attribute: str
    metric_type: FairnessMetric
    score: float
    is_fair: bool
    group_metrics: Dict[str, float]
    threshold: float


class FairnessAnalyzer:
    """Analyze model predictions for fairness and bias."""

    def __init__(self, fairness_threshold: float = 0.8):
        """
        Initialize fairness analyzer.

        Args:
            fairness_threshold: Threshold for fairness (0.8 = 80% rule)
        """
        self.fairness_threshold = fairness_threshold

    def calculate_demographic_parity(
        self,
        predictions: List[float],
        protected_groups: List[str],
        threshold: float = 0.5,
    ) -> BiasReport:
        """
        Calculate demographic parity (equal positive rate across groups).

        Args:
            predictions: Model predictions (probabilities)
            protected_groups: Group labels for each prediction
            threshold: Threshold for positive classification

        Returns:
            BiasReport with demographic parity analysis
        """
        # Convert predictions to binary
        binary_preds = [1 if p >= threshold else 0 for p in predictions]

        # Calculate positive rates per group
        unique_groups = list(set(protected_groups))
        group_positive_rates = {}

        for group in unique_groups:
            group_preds = [binary_preds[i] for i, g in enumerate(protected_groups) if g == group]
            if group_preds:
                positive_rate = sum(group_preds) / len(group_preds)
                group_positive_rates[group] = positive_rate

        # Calculate disparity
        if len(group_positive_rates) < 2:
            disparity_score = 1.0
        else:
            rates = list(group_positive_rates.values())
            min_rate = min(rates)
            max_rate = max(rates)
            disparity_score = min_rate / max_rate if max_rate > 0 else 1.0

        return BiasReport(
            protected_attribute="group",
            metric_type=FairnessMetric.DEMOGRAPHIC_PARITY,
            score=disparity_score,
            is_fair=disparity_score >= self.fairness_threshold,
            group_metrics=group_positive_rates,
            threshold=self.fairness_threshold,
        )

    def calculate_equal_opportunity(
        self,
        predictions: List[float],
        protected_groups: List[str],
        true_labels: List[int],
        threshold: float = 0.5,
    ) -> BiasReport:
        """
        Calculate equal opportunity (equal TPR across groups).

        Args:
            predictions: Model predictions (probabilities)
            protected_groups: Group labels
            true_labels: True labels (0 or 1)
            threshold: Classification threshold

        Returns:
            BiasReport with equal opportunity analysis
        """
        binary_preds = [1 if p >= threshold else 0 for p in predictions]

        unique_groups = list(set(protected_groups))
        group_tpr = {}

        for group in unique_groups:
            group_indices = [i for i, g in enumerate(protected_groups) if g == group]

            # True positives and actual positives for this group
            tp = sum(1 for i in group_indices if true_labels[i] == 1 and binary_preds[i] == 1)
            actual_positive = sum(1 for i in group_indices if true_labels[i] == 1)

            tpr = tp / actual_positive if actual_positive > 0 else 0.0
            group_tpr[group] = tpr

        # Calculate disparity
        if len(group_tpr) < 2:
            disparity_score = 1.0
        else:
            tprs = list(group_tpr.values())
            min_tpr = min(tprs)
            max_tpr = max(tprs)
            disparity_score = min_tpr / max_tpr if max_tpr > 0 else 1.0

        return BiasReport(
            protected_attribute="group",
            metric_type=FairnessMetric.EQUAL_OPPORTUNITY,
            score=disparity_score,
            is_fair=disparity_score >= self.fairness_threshold,
            group_metrics=group_tpr,
            threshold=self.fairness_threshold,
        )

    def calculate_disparate_impact(
        self,
        predictions: List[float],
        protected_groups: List[str],
        privileged_group: str,
        threshold: float = 0.5,
    ) -> BiasReport:
        """
        Calculate disparate impact ratio.

        Args:
            predictions: Model predictions
            protected_groups: Group labels
            privileged_group: Name of the privileged group
            threshold: Classification threshold

        Returns:
            BiasReport with disparate impact analysis
        """
        binary_preds = [1 if p >= threshold else 0 for p in predictions]

        # Calculate selection rates
        unique_groups = list(set(protected_groups))
        selection_rates = {}

        for group in unique_groups:
            group_preds = [binary_preds[i] for i, g in enumerate(protected_groups) if g == group]
            if group_preds:
                selection_rates[group] = sum(group_preds) / len(group_preds)

        # Calculate disparate impact ratio
        privileged_rate = selection_rates.get(privileged_group, 1.0)

        impact_ratios = {}
        for group, rate in selection_rates.items():
            if group != privileged_group:
                impact_ratios[group] = rate / privileged_rate if privileged_rate > 0 else 1.0

        # Overall score is the minimum ratio
        min_ratio = min(impact_ratios.values()) if impact_ratios else 1.0

        return BiasReport(
            protected_attribute="group",
            metric_type=FairnessMetric.DISPARATE_IMPACT,
            score=min_ratio,
            is_fair=min_ratio >= self.fairness_threshold,
            group_metrics=selection_rates,
            threshold=self.fairness_threshold,
        )

    def comprehensive_fairness_check(
        self,
        predictions: List[float],
        protected_groups: List[str],
        true_labels: Optional[List[int]] = None,
        privileged_group: Optional[str] = None,
    ) -> List[BiasReport]:
        """
        Run comprehensive fairness analysis.

        Args:
            predictions: Model predictions
            protected_groups: Group labels
            true_labels: True labels (optional, for equal opportunity)
            privileged_group: Privileged group name (optional, for disparate impact)

        Returns:
            List of BiasReport objects
        """
        reports = []

        # Always check demographic parity
        reports.append(self.calculate_demographic_parity(predictions, protected_groups))

        # Check equal opportunity if labels provided
        if true_labels is not None:
            reports.append(
                self.calculate_equal_opportunity(predictions, protected_groups, true_labels)
            )

        # Check disparate impact if privileged group specified
        if privileged_group is not None:
            reports.append(
                self.calculate_disparate_impact(predictions, protected_groups, privileged_group)
            )

        return reports
