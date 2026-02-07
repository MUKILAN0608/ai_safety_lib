"""
GOOGLE COLAB SETUP & USAGE GUIDE
AI Safety Library

Copy and paste these cells into your Google Colab notebook
"""

# ============================================================================
# CELL 1: INSTALL THE LIBRARY
# ============================================================================
print("""
CELL 1: Installation
Copy and paste this into a Colab cell and run it:
""")

code_cell_1 = '''
# Install AI Safety Library
!pip install ai-safety-lib -q

# Verify installation
import ai_safety_lib
print(f"✅ AI Safety Library {ai_safety_lib.__version__} installed!")
'''

print(code_cell_1)

# ============================================================================
# CELL 2: BASIC IMPORTS
# ============================================================================
print("\n" + "="*70)
print("CELL 2: Import Libraries")
print("="*70)

code_cell_2 = '''
import numpy as np
import pandas as pd
from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.monitoring import PerformanceMonitor
from ai_safety_lib.fairness import FairnessAnalyzer
from ai_safety_lib.explainability import ExplainabilityAnalyzer
from ai_safety_lib.config import ConfigManager

print("✅ All imports successful!")
'''

print(code_cell_2)

# ============================================================================
# CELL 3: GENERATE SAMPLE DATA
# ============================================================================
print("\n" + "="*70)
print("CELL 3: Create Sample Data")
print("="*70)

code_cell_3 = '''
np.random.seed(42)

# Generate sample predictions
predictions = np.random.uniform(0.65, 0.95, 100).tolist()

# Reference dataset (for drift detection)
reference_data = {
    "age": np.random.normal(35, 10, 100).tolist(),
    "income": np.random.normal(50000, 15000, 100).tolist(),
    "credit_score": np.random.normal(700, 50, 100).tolist(),
}

# Current dataset (slightly drifted)
current_data = {
    "age": np.random.normal(36, 11, 100).tolist(),
    "income": np.random.normal(51000, 16000, 100).tolist(),
    "credit_score": np.random.normal(695, 52, 100).tolist(),
}

# Labels and groups (for fairness)
true_labels = np.random.binomial(1, 0.7, 100).tolist()
protected_groups = np.random.choice(['Group_A', 'Group_B'], 100).tolist()

print(f"✅ Generated sample data:")
print(f"   - Predictions: {len(predictions)} samples")
print(f"   - Reference features: {len(reference_data)} features")
print(f"   - Current features: {len(current_data)} features")
print(f"   - Groups: {set(protected_groups)}")
'''

print(code_cell_3)

# ============================================================================
# CELL 4: SAFETY EVALUATION
# ============================================================================
print("\n" + "="*70)
print("CELL 4: Safety Evaluation")
print("="*70)

code_cell_4 = '''
# Initialize safety gate
safety_gate = SafetyGate(
    confidence_threshold=0.7,
    drift_threshold=0.3,
    allow_warning=False
)

# Evaluate safety
assessment = safety_gate.evaluate(
    predictions=predictions,
    reference_data=reference_data,
    current_data=current_data,
    dataset_name="colab_test"
)

# Display results
print("="*60)
print("SAFETY EVALUATION RESULTS")
print("="*60)
print(f"Risk Level: {assessment.risk_level.value.upper()}")
print(f"Overall Risk Score: {assessment.overall_risk:.3f}")
print(f"\\nComponent Risks:")
for component, risk in assessment.component_risks.items():
    print(f"  - {component}: {risk:.3f}")
print(f"\\nShould Deploy: {'✅ YES' if safety_gate.should_deploy(assessment) else '❌ NO'}")
print(f"\\nRecommendations:")
for rec in assessment.recommendations:
    print(f"  - {rec}")
'''

print(code_cell_4)

# ============================================================================
# CELL 5: PERFORMANCE MONITORING
# ============================================================================
print("\n" + "="*70)
print("CELL 5: Performance Monitoring")
print("="*70)

code_cell_5 = '''
# Initialize monitor
monitor = PerformanceMonitor(
    alert_thresholds={
        'accuracy': 0.75,
        'error_rate': 0.10,
        'latency_ms': 500
    }
)

# Calculate metrics
metrics = monitor.calculate_metrics_from_predictions(
    predictions=predictions,
    true_labels=true_labels
)

# Record metrics
monitor.record_metrics(
    accuracy=metrics['accuracy'],
    precision=metrics['precision'],
    recall=metrics['recall'],
    f1_score=metrics['f1_score'],
    latency_ms=np.random.uniform(100, 300),
    error_rate=0.05
)

# Display results
print("="*60)
print("PERFORMANCE METRICS")
print("="*60)
print(f"Accuracy:  {metrics['accuracy']:.4f}")
print(f"Precision: {metrics['precision']:.4f}")
print(f"Recall:    {metrics['recall']:.4f}")
print(f"F1 Score:  {metrics['f1_score']:.4f}")

# Get alerts
alerts = monitor.get_recent_alerts()
if alerts:
    print(f"\\n⚠️  Alerts ({len(alerts)}):")
    for alert in alerts:
        print(f"  - [{alert.severity.value}] {alert.message}")
else:
    print("\\n✅ No alerts triggered")
'''

print(code_cell_5)

# ============================================================================
# CELL 6: FAIRNESS ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("CELL 6: Fairness Analysis")
print("="*70)

code_cell_6 = '''
# Initialize fairness analyzer
fairness = FairnessAnalyzer(fairness_threshold=0.8)

# Run comprehensive fairness check
fairness_reports = fairness.comprehensive_fairness_check(
    predictions=predictions,
    protected_groups=protected_groups,
    true_labels=true_labels,
    privileged_group='Group_A'
)

# Display results
print("="*60)
print("FAIRNESS ANALYSIS RESULTS")
print("="*60)

for report in fairness_reports:
    status = "✅ FAIR" if report.is_fair else "⚠️ BIASED"
    print(f"\\n{report.metric_type.value.upper()}: {status}")
    print(f"  Score: {report.score:.4f} (threshold: {report.threshold})")
    print(f"  Group Metrics:")
    for group, metric in report.group_metrics.items():
        print(f"    - {group}: {metric:.4f}")
'''

print(code_cell_6)

# ============================================================================
# CELL 7: EXPLAINABILITY
# ============================================================================
print("\n" + "="*70)
print("CELL 7: Feature Importance & Explainability")
print("="*70)

code_cell_7 = '''
# Initialize explainability analyzer
explainer = ExplainabilityAnalyzer()

# Calculate feature importance
importances = explainer.calculate_feature_importance(
    feature_values=current_data,
    predictions=predictions
)

# Display feature importance
print("="*60)
print("FEATURE IMPORTANCE")
print("="*60)
for importance in importances:
    bar = "█" * int(importance.importance_score * 50)
    print(f"{importance.rank}. {importance.feature_name:15} {bar} {importance.importance_score:.4f}")

# Explain a specific prediction
print("\\n" + "="*60)
print("PREDICTION EXPLANATION (Sample #0)")
print("="*60)

sample_features = {k: v[0] for k, v in current_data.items()}
explanation = explainer.explain_prediction(
    prediction_index=0,
    prediction_value=predictions[0],
    feature_values=sample_features,
    feature_importances=importances,
    top_k=3
)

print(explainer.generate_explanation_report(explanation, verbose=True))
'''

print(code_cell_7)

# ============================================================================
# CELL 8: VISUALIZATION (OPTIONAL BUT RECOMMENDED)
# ============================================================================
print("\n" + "="*70)
print("CELL 8: Visualization (Optional)")
print("="*70)

code_cell_8 = '''
import matplotlib.pyplot as plt

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Risk Score Distribution
axes[0, 0].hist(predictions, bins=20, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Prediction Distribution')
axes[0, 0].set_xlabel('Prediction Value')
axes[0, 0].set_ylabel('Count')
axes[0, 0].axvline(0.7, color='red', linestyle='--', label='Threshold')
axes[0, 0].legend()

# 2. Performance Metrics
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
metrics_values = [metrics['accuracy'], metrics['precision'], 
                  metrics['recall'], metrics['f1_score']]
colors = ['green' if v >= 0.75 else 'orange' for v in metrics_values]
axes[0, 1].bar(metrics_names, metrics_values, color=colors)
axes[0, 1].set_title('Performance Metrics')
axes[0, 1].set_ylim([0, 1])
axes[0, 1].set_ylabel('Score')

# 3. Feature Importance
feat_names = [imp.feature_name for imp in importances]
feat_scores = [imp.importance_score for imp in importances]
axes[1, 0].barh(feat_names, feat_scores, color='coral')
axes[1, 0].set_title('Feature Importance')
axes[1, 0].set_xlabel('Importance Score')

# 4. Fairness by Group
group_a_rate = sum(1 for i, p in enumerate(predictions) 
                   if protected_groups[i] == 'Group_A' and p >= 0.7) / sum(1 for g in protected_groups if g == 'Group_A')
group_b_rate = sum(1 for i, p in enumerate(predictions) 
                   if protected_groups[i] == 'Group_B' and p >= 0.7) / sum(1 for g in protected_groups if g == 'Group_B')
axes[1, 1].bar(['Group_A', 'Group_B'], [group_a_rate, group_b_rate], color=['blue', 'orange'])
axes[1, 1].set_title('Selection Rate by Group')
axes[1, 1].set_ylim([0, 1])
axes[1, 1].set_ylabel('Selection Rate')
axes[1, 1].axhline(0.8, color='red', linestyle='--', label='Fairness Threshold')
axes[1, 1].legend()

plt.tight_layout()
plt.show()

print("✓ Visualization complete!")
'''

print(code_cell_8)

# ============================================================================
# CELL 9: CONFIGURATION & SAVING RESULTS
# ============================================================================
print("\n" + "="*70)
print("CELL 9: Save Results")
print("="*70)

code_cell_9 = '''
import json
from google.colab import files

# Prepare results dictionary
results = {
    "safety": {
        "risk_level": assessment.risk_level.value,
        "overall_risk": assessment.overall_risk,
        "component_risks": assessment.component_risks,
        "should_deploy": safety_gate.should_deploy(assessment)
    },
    "performance": {
        "accuracy": metrics['accuracy'],
        "precision": metrics['precision'],
        "recall": metrics['recall'],
        "f1_score": metrics['f1_score']
    },
    "fairness": {
        report.metric_type.value: {
            "is_fair": report.is_fair,
            "score": report.score,
            "group_metrics": report.group_metrics
        }
        for report in fairness_reports
    }
}

# Save to JSON
with open('safety_assessment_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("✓ Results saved to safety_assessment_results.json")
print("\\nDownloading file...")
files.download('safety_assessment_results.json')
'''

print(code_cell_9)

# ============================================================================
# CELL 10: COMPLETE WORKFLOW
# ============================================================================
print("\n" + "="*70)
print("CELL 10: Complete Workflow (All-in-One)")
print("="*70)

code_cell_10 = '''
# All-in-one complete workflow

# 1. Initialize components
safety_gate = SafetyGate()
monitor = PerformanceMonitor()
fairness = FairnessAnalyzer()
explainer = ExplainabilityAnalyzer()

# 2. Load your data (replace with actual data)
# X_train, y_train = load_your_data()
# predictions = model.predict(X_test)
# reference_data = extract_features(X_train)
# current_data = extract_features(X_test)

# 3. Run all checks
print("Running AI Safety Analysis...")
print("-" * 50)

# Safety
safety_assessment = safety_gate.evaluate(predictions, reference_data, current_data)
print(f"✓ Safety: {safety_assessment.risk_level.value}")

# Performance
perf_metrics = monitor.calculate_metrics_from_predictions(predictions, true_labels)
monitor.record_metrics(**perf_metrics)
print(f"✓ Performance: Accuracy={perf_metrics['accuracy']:.3f}")

# Fairness
fairness_reports = fairness.comprehensive_fairness_check(
    predictions, protected_groups, true_labels
)
fair_status = all(r.is_fair for r in fairness_reports)
print(f"✓ Fairness: {'FAIR' if fair_status else 'BIASED'}")

# Explainability
importances = explainer.calculate_feature_importance(current_data, predictions)
print(f"✓ Top Feature: {importances[0].feature_name}")

# 4. Final decision
print("-" * 50)
if safety_gate.should_deploy(safety_assessment) and fair_status:
    print("✅ READY FOR PRODUCTION DEPLOYMENT")
else:
    print("❌ NEEDS FURTHER REVIEW BEFORE DEPLOYMENT")
    print(f"   Recommendations: {safety_assessment.recommendations}")
'''

print(code_cell_10)

# ============================================================================
# TIPS & TROUBLESHOOTING
# ============================================================================
print("\n" + "="*70)
print("TIPS & TROUBLESHOOTING")
print("="*70)

tips = """
✅ TIPS FOR COLAB:

1. Use !pip for package installation (with -q flag for quiet mode)

2. Save results to local files if you need to download:
   from google.colab import files
   files.download('results.json')

3. Mount Google Drive to load large datasets:
   from google.colab import drive
   drive.mount('/content/drive')

4. Use smaller datasets in Colab for faster execution

5. Enable GPU if needed:
   Runtime → Change Runtime Type → GPU

❌ TROUBLESHOOTING:

Problem: ImportError after installation
Solution: Restart kernel after pip install (Runtime → Restart runtime)

Problem: Memory error with large datasets
Solution: Use smaller sample or process in batches

Problem: Slow execution
Solution: Use GPU acceleration or reduce data size

Problem: Cannot download files
Solution: Check files.download() is called, file exists in working directory
"""

print(tips)

print("\n" + "="*70)
print("READY TO USE IN COLAB!")
print("="*70)
print("""
Copy the code cells above into your Google Colab notebook in order.
Each cell is independent and can be run separately.

Quick Start Path:
1. Cell 1 (Install)
2. Cell 2 (Imports)
3. Cell 3 (Data)
4. Cell 4 (Safety)
5. Cell 5-7 (Other analyses)

Or run Cell 10 for complete workflow!
""")
