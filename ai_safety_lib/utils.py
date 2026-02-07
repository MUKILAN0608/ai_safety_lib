"""Utility functions for AI safety monitoring."""

from typing import List, Dict, Any, Union
import json
from pathlib import Path


def save_metrics_to_file(metrics: Dict[str, Any], filepath: Union[str, Path]) -> None:
    """Save metrics to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)


def load_metrics_from_file(filepath: Union[str, Path]) -> Dict[str, Any]:
    """Load metrics from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def normalize_predictions(predictions: List[float]) -> List[float]:
    """Normalize predictions to [0, 1] range."""
    if not predictions:
        return []
    
    min_val = min(predictions)
    max_val = max(predictions)
    
    if min_val == max_val:
        return [0.5] * len(predictions)
    
    return [(p - min_val) / (max_val - min_val) for p in predictions]


def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculate percentile of data."""
    if not data:
        return 0.0
    
    sorted_data = sorted(data)
    index = int(len(sorted_data) * percentile / 100.0)
    return sorted_data[min(index, len(sorted_data) - 1)]


def format_assessment_report(
    assessment: Dict[str, Any],
    verbose: bool = False
) -> str:
    """Format assessment results for display."""
    report = []
    report.append("=" * 50)
    report.append("SAFETY ASSESSMENT REPORT")
    report.append("=" * 50)
    
    report.append(f"\nOverall Risk Level: {assessment.get('risk_level', 'Unknown')}")
    report.append(f"Risk Score: {assessment.get('overall_risk', 0.0):.3f}")
    
    if verbose:
        component_risks = assessment.get('component_risks', {})
        report.append("\nComponent Risks:")
        for component, risk in component_risks.items():
            report.append(f"  - {component}: {risk:.3f}")
        
        recommendations = assessment.get('recommendations', [])
        if recommendations:
            report.append("\nRecommendations:")
            for rec in recommendations:
                report.append(f"  - {rec}")
    
    report.append("=" * 50)
    return "\n".join(report)
