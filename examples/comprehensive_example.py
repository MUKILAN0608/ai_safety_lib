"""Example: Advanced safety monitoring with all features."""

import numpy as np
from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.monitoring import PerformanceMonitor, AlertSeverity
from ai_safety_lib.fairness import FairnessAnalyzer
from ai_safety_lib.explainability import ExplainabilityAnalyzer
from ai_safety_lib.utils import format_assessment_report


def alert_callback(alert):
    """Callback function for alerts."""
    print(f"\nALERT [{alert.severity.value.upper()}]: {alert.message}")


def main():
    """Run comprehensive safety monitoring example."""
    print("=" * 70)
    print("AI Safety Library - Comprehensive Example")
    print("=" * 70)
    
    # Initialize components
    safety_gate = SafetyGate(
        confidence_threshold=0.7,
        drift_threshold=0.3,
        allow_warning=False
    )
    
    performance_monitor = PerformanceMonitor(
        alert_thresholds={
            'accuracy': 0.75,
            'error_rate': 0.15,
            'latency_ms': 500.0
        },
        alert_callback=alert_callback
    )
    
    fairness_analyzer = FairnessAnalyzer(fairness_threshold=0.8)
    explainability_analyzer = ExplainabilityAnalyzer()
    
    # Generate synthetic data
    np.random.seed(42)
    
    # Model predictions
    predictions = np.random.uniform(0.65, 0.95, 100).tolist()
    
    # Reference and current data
    reference_data = {
        "age": np.random.normal(35, 10, 100).tolist(),
        "income": np.random.normal(50000, 15000, 100).tolist(),
        "credit_score": np.random.normal(700, 50, 100).tolist(),
    }
    
    current_data = {
        "age": np.random.normal(36, 11, 100).tolist(),
        "income": np.random.normal(51000, 15500, 100).tolist(),
        "credit_score": np.random.normal(695, 52, 100).tolist(),
    }
    
    # True labels (for fairness and performance metrics)
    true_labels = np.random.binomial(1, 0.7, 100).tolist()
    
    # Protected groups (for fairness analysis)
    protected_groups = np.random.choice(['Group_A', 'Group_B'], 100).tolist()
    
    print("\n1. Safety Evaluation")
    print("-" * 70)
    assessment = safety_gate.evaluate(
        predictions=predictions,
        reference_data=reference_data,
        current_data=current_data,
        dataset_name="credit_scoring"
    )
    
    report = format_assessment_report(vars(assessment), verbose=True)
    print(report)
    
    deploy_decision = "✅ APPROVED" if safety_gate.should_deploy(assessment) else "❌ BLOCKED"
    print(f"\nDeployment Decision: {deploy_decision}")
    
    print("\n2. Performance Monitoring")
    print("-" * 70)
    
    # Calculate and record metrics
    metrics = performance_monitor.calculate_metrics_from_predictions(
        predictions, true_labels
    )
    
    performance_monitor.record_metrics(
        accuracy=metrics['accuracy'],
        precision=metrics['precision'],
        recall=metrics['recall'],
        f1_score=metrics['f1_score'],
        latency_ms=np.random.uniform(100, 300),
        error_rate=0.05
    )
    
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1 Score: {metrics['f1_score']:.3f}")
    
    # Get metrics summary
    summary = performance_monitor.get_metrics_summary(last_n=5)
    if summary:
        print("\nMetrics Summary (Last 5 records):")
        for metric_name, stats in summary.items():
            print(f"  {metric_name}: mean={stats['mean']:.3f}, std={stats['std']:.3f}")
    
    print("\n3. Fairness Analysis")
    print("-" * 70)
    
    fairness_reports = fairness_analyzer.comprehensive_fairness_check(
        predictions=predictions,
        protected_groups=protected_groups,
        true_labels=true_labels,
        privileged_group='Group_A'
    )
    
    for report in fairness_reports:
        status = "✅ FAIR" if report.is_fair else "⚠️ BIASED"
        print(f"\n{report.metric_type.value.upper()}: {status}")
        print(f"  Score: {report.score:.3f} (threshold: {report.threshold})")
        print(f"  Group Metrics: {report.group_metrics}")
    
    print("\n4. Explainability Analysis")
    print("-" * 70)
    
    # Calculate feature importance
    feature_importances = explainability_analyzer.calculate_feature_importance(
        feature_values=current_data,
        predictions=predictions
    )
    
    print("\nFeature Importances:")
    for feat in feature_importances:
        print(f"  {feat.rank}. {feat.feature_name}: {feat.importance_score:.4f}")
    
    # Explain a specific prediction
    sample_idx = 0
    sample_features = {k: v[sample_idx] for k, v in current_data.items()}
    
    explanation = explainability_analyzer.explain_prediction(
        prediction_index=sample_idx,
        prediction_value=predictions[sample_idx],
        feature_values=sample_features,
        feature_importances=feature_importances,
        top_k=3
    )
    
    print(f"\n{explainability_analyzer.generate_explanation_report(explanation)}")
    
    print("\n5. Alert Summary")
    print("-" * 70)
    
    recent_alerts = performance_monitor.get_recent_alerts(limit=5)
    if recent_alerts:
        print(f"Recent Alerts: {len(recent_alerts)}")
        for alert in recent_alerts:
            print(f"  [{alert.severity.value}] {alert.message}")
    else:
        print("No alerts triggered ✅")
    
    print("\n" + "=" * 70)
    print("Comprehensive safety analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
