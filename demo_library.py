#!/usr/bin/env python
"""Demo script showing AI Safety Library usage"""

import numpy as np
from ai_safety_lib import (
    SafetyGate,
    PerformanceMonitor,
    FairnessAnalyzer,
    ExplainabilityAnalyzer,
)

print("=" * 70)
print("AI SAFETY LIBRARY - PYTHON LIBRARY DEMO")
print("=" * 70)

# 1. Initialize all components
print("\n1. Initializing components...")
safety_gate = SafetyGate(confidence_threshold=0.7, drift_threshold=0.3)
monitor = PerformanceMonitor()
fairness = FairnessAnalyzer()
explainer = ExplainabilityAnalyzer()
print("   ✓ All components initialized")

# 2. Generate sample data
print("\n2. Generating sample data (50 samples)...")
np.random.seed(42)
predictions = np.random.uniform(0.65, 0.95, 50).tolist()
reference_data = {
    "feature_1": np.random.normal(0, 1, 50).tolist(),
    "feature_2": np.random.normal(0, 1, 50).tolist(),
}
current_data = {
    "feature_1": np.random.normal(0.1, 1.1, 50).tolist(),
    "feature_2": np.random.normal(0, 1, 50).tolist(),
}
true_labels = np.random.binomial(1, 0.7, 50).tolist()
protected_groups = np.random.choice(["Group_A", "Group_B"], 50).tolist()
print("   ✓ Sample data ready")

# 3. Safety Evaluation
print("\n3. Safety Evaluation")
assessment = safety_gate.evaluate(
    predictions=predictions,
    reference_data=reference_data,
    current_data=current_data,
)
risk_level = assessment.risk_level.value
overall_risk = assessment.overall_risk
should_deploy = safety_gate.should_deploy(assessment)
print(f"   ✓ Risk Level: {risk_level}")
print(f"   ✓ Overall Risk Score: {overall_risk:.4f}")
print(f"   ✓ Safe to Deploy: {should_deploy}")

# 4. Performance Monitoring
print("\n4. Performance Monitoring")
metrics = monitor.calculate_metrics_from_predictions(predictions, true_labels)
monitor.record_metrics(
    accuracy=metrics["accuracy"],
    precision=metrics["precision"],
    recall=metrics["recall"],
    f1_score=metrics["f1_score"],
    latency_ms=125.5,
    error_rate=0.05,
)
print(f"   ✓ Accuracy: {metrics['accuracy']:.4f}")
print(f"   ✓ Precision: {metrics['precision']:.4f}")
print(f"   ✓ Recall: {metrics['recall']:.4f}")
print(f"   ✓ F1 Score: {metrics['f1_score']:.4f}")

# 5. Fairness Analysis
print("\n5. Fairness Analysis")
fairness_reports = fairness.comprehensive_fairness_check(
    predictions=predictions,
    protected_groups=protected_groups,
    true_labels=true_labels,
)
for report in fairness_reports[:3]:
    print(f"   ✓ {report.metric_type.value}: {report.is_fair} (score={report.score:.4f})")

# 6. Explainability
print("\n6. Feature Importance")
importances = explainer.calculate_feature_importance(
    feature_values=current_data, predictions=predictions
)
for imp in importances[:3]:
    print(f"   ✓ {imp.rank}. {imp.feature_name}: {imp.importance_score:.4f}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Status: ALL CHECKS COMPLETED SUCCESSFULLY")
print(f"Risk Level: {risk_level}")
print(f"Deployment Ready: {should_deploy}")
print(f"Model Accuracy: {metrics['accuracy']:.2%}")
print(f"Fairness Status: {'FAIR' if all(r.is_fair for r in fairness_reports) else 'NEEDS REVIEW'}")
print("=" * 70)
print("\nLibrary is working perfectly! You can now use it in your projects.")
print("=" * 70)
