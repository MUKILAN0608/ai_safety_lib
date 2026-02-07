"""
GETTING STARTED GUIDE - AI Safety Library

This script shows the different ways to use the AI Safety Library
"""

print("=" * 70)
print("AI SAFETY LIBRARY - USAGE GUIDE")
print("=" * 70)

# ============================================================================
# METHOD 1: BASIC INSTALLATION & IMPORT
# ============================================================================
print("\n1️⃣  INSTALLATION")
print("-" * 70)
print("""
From command line:
    pip install ai-safety-lib
    
Or with API features:
    pip install ai-safety-lib[api]
    
Or from source:
    git clone https://github.com/MUKILAN0608/ai_safety_lib.git
    cd ai_safety_lib
    pip install -e .
""")

# ============================================================================
# METHOD 2: BASIC SAFETY EVALUATION
# ============================================================================
print("\n2️⃣  BASIC SAFETY EVALUATION")
print("-" * 70)
print("""
from ai_safety_lib.safety_gate import SafetyGate
import numpy as np

# Initialize
safety_gate = SafetyGate(
    confidence_threshold=0.7,
    drift_threshold=0.3
)

# Your predictions
predictions = [0.8, 0.9, 0.75, ...]  # Your model outputs

# Reference & current data for drift detection
reference_data = {
    "age": [25, 30, 35, ...],
    "income": [50000, 60000, 70000, ...]
}
current_data = {
    "age": [26, 31, 36, ...],
    "income": [51000, 61000, 71000, ...]
}

# Evaluate
assessment = safety_gate.evaluate(
    predictions=predictions,
    reference_data=reference_data,
    current_data=current_data
)

# Check result
print(f"Risk Level: {assessment.risk_level}")
print(f"Deploy: {safety_gate.should_deploy(assessment)}")
""")

# ============================================================================
# METHOD 3: PERFORMANCE MONITORING
# ============================================================================
print("\n3️⃣  PERFORMANCE MONITORING")
print("-" * 70)
print("""
from ai_safety_lib.monitoring import PerformanceMonitor

# Initialize with alert settings
monitor = PerformanceMonitor(
    alert_thresholds={
        'accuracy': 0.75,
        'error_rate': 0.10,
        'latency_ms': 500
    }
)

# Record metrics
monitor.record_metrics(
    accuracy=0.85,
    precision=0.82,
    recall=0.88,
    f1_score=0.85,
    latency_ms=120.5,
    error_rate=0.05
)

# Check metrics summary
summary = monitor.get_metrics_summary(last_n=10)
print(summary)

# Get recent alerts
alerts = monitor.get_recent_alerts(limit=5)
for alert in alerts:
    print(f"[{alert.severity}] {alert.message}")
""")

# ============================================================================
# METHOD 4: FAIRNESS ANALYSIS
# ============================================================================
print("\n4️⃣  FAIRNESS ANALYSIS")
print("-" * 70)
print("""
from ai_safety_lib.fairness import FairnessAnalyzer

analyzer = FairnessAnalyzer(fairness_threshold=0.8)

predictions = [0.8, 0.9, 0.75, ...]
groups = ['Group_A', 'Group_B', 'Group_A', ...]  # Protected attribute
labels = [1, 0, 1, ...]  # True labels

# Check fairness
reports = analyzer.comprehensive_fairness_check(
    predictions=predictions,
    protected_groups=groups,
    true_labels=labels,
    privileged_group='Group_A'
)

# Review results
for report in reports:
    print(f"Metric: {report.metric_type.value}")
    print(f"Fair: {report.is_fair}")
    print(f"Score: {report.score:.3f}")
""")

# ============================================================================
# METHOD 5: EXPLAINABILITY
# ============================================================================
print("\n5️⃣  EXPLAINABILITY & FEATURE IMPORTANCE")
print("-" * 70)
print("""
from ai_safety_lib.explainability import ExplainabilityAnalyzer

analyzer = ExplainabilityAnalyzer()

# Feature values
features = {
    "age": [25, 30, 35],
    "income": [50000, 60000, 70000],
    "credit_score": [700, 750, 680]
}

predictions = [0.8, 0.9, 0.75]

# Get feature importance
importances = analyzer.calculate_feature_importance(
    feature_values=features,
    predictions=predictions
)

# Print
for imp in importances:
    print(f"{imp.rank}. {imp.feature_name}: {imp.importance_score:.4f}")

# Explain single prediction
explanation = analyzer.explain_prediction(
    prediction_index=0,
    prediction_value=0.8,
    feature_values={"age": 25, "income": 50000, "credit_score": 700},
    feature_importances=importances,
    top_k=2
)

print(analyzer.generate_explanation_report(explanation))
""")

# ============================================================================
# METHOD 6: CONFIGURATION MANAGEMENT
# ============================================================================
print("\n6️⃣  CONFIGURATION MANAGEMENT")
print("-" * 70)
print("""
from ai_safety_lib.config import ConfigManager

# Load from file
config_mgr = ConfigManager()
config = config_mgr.load_from_file('config.yaml')

# Usage
safety_gate = SafetyGate(
    confidence_threshold=config.safety.confidence_threshold,
    drift_threshold=config.safety.drift_threshold,
    allow_warning=config.safety.allow_warning
)

# Or set from environment variables
import os
os.environ['SAFETY_CONFIDENCE_THRESHOLD'] = '0.75'
config = config_mgr.load_from_env()
""")

# ============================================================================
# METHOD 7: REST API SERVER
# ============================================================================
print("\n7️⃣  REST API SERVER")
print("-" * 70)
print("""
# Start server:
python api_server.py

# Or with uvicorn:
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Docker:
docker build -t ai-safety-api .
docker run -p 8000:8000 ai-safety-api

# Access documentation:
http://localhost:8000/docs          (Swagger UI)
http://localhost:8000/redoc         (ReDoc)
http://localhost:8000/health        (Health check)

# Example API call:
curl -X POST http://localhost:8000/evaluate \\
  -H "Content-Type: application/json" \\
  -d '{
    "predictions": [0.8, 0.9],
    "reference_data": {"f1": [1.0, 2.0]},
    "current_data": {"f1": [1.1, 2.1]}
  }'
""")

# ============================================================================
# METHOD 8: COMPLETE WORKFLOW
# ============================================================================
print("\n8️⃣  COMPLETE WORKFLOW EXAMPLE")
print("-" * 70)
print("""
import numpy as np
from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.monitoring import PerformanceMonitor
from ai_safety_lib.fairness import FairnessAnalyzer
from ai_safety_lib.explainability import ExplainabilityAnalyzer

# 1. Initialize all components
safety_gate = SafetyGate()
performance_monitor = PerformanceMonitor()
fairness_analyzer = FairnessAnalyzer()
explainability_analyzer = ExplainabilityAnalyzer()

# 2. Prepare data
predictions = np.random.uniform(0.7, 0.95, 100).tolist()
reference_data = {
    "feature_1": np.random.normal(0, 1, 100).tolist(),
    "feature_2": np.random.normal(0, 1, 100).tolist(),
}
current_data = {
    "feature_1": np.random.normal(0.1, 1.1, 100).tolist(),
    "feature_2": np.random.normal(0, 1, 100).tolist(),
}
true_labels = np.random.binomial(1, 0.7, 100).tolist()
groups = np.random.choice(['A', 'B'], 100).tolist()

# 3. Evaluate safety
safety_assessment = safety_gate.evaluate(
    predictions=predictions,
    reference_data=reference_data,
    current_data=current_data
)

print(f"✓ Safety Check: {safety_assessment.risk_level}")
print(f"  Deploy: {safety_gate.should_deploy(safety_assessment)}")

# 4. Monitor performance
metrics = performance_monitor.calculate_metrics_from_predictions(
    predictions, true_labels
)
performance_monitor.record_metrics(
    accuracy=metrics['accuracy'],
    precision=metrics['precision'],
    recall=metrics['recall'],
    f1_score=metrics['f1_score']
)

print(f"✓ Performance: Accuracy={metrics['accuracy']:.3f}")

# 5. Check fairness
fairness_reports = fairness_analyzer.comprehensive_fairness_check(
    predictions=predictions,
    protected_groups=groups,
    true_labels=true_labels
)

for report in fairness_reports:
    print(f"✓ Fairness ({report.metric_type.value}): {report.is_fair}")

# 6. Generate explanations
importances = explainability_analyzer.calculate_feature_importance(
    feature_values=current_data,
    predictions=predictions
)

print(f"✓ Top Feature: {importances[0].feature_name} "
      f"(importance={importances[0].importance_score:.4f})")

print("\\n✅ All checks complete!")
""")

# ============================================================================
# DEPLOYMENT OPTIONS
# ============================================================================
print("\n9️⃣  DEPLOYMENT OPTIONS")
print("-" * 70)
print("""
OPTION A: Standalone Script
    - Run Python script directly
    - Use SafetyGate in your ML pipeline
    - Simple integration with existing code

OPTION B: REST API Server
    - Start API server: python api_server.py
    - Call endpoints from any language/service
    - Full monitoring & audit logs

OPTION C: Docker Container
    - docker build -t ai-safety-api .
    - docker run -p 8000:8000 ai-safety-api
    - Deploy to Kubernetes, AWS ECS, Azure Container Instances

OPTION D: Cloud Functions
    - Deploy API to AWS Lambda, Azure Functions, Google Cloud Run
    - See docs/DEPLOYMENT.md for detailed guides
""")

# ============================================================================
# EXAMPLES & DOCUMENTATION
# ============================================================================
print("\n🔟 EXAMPLES & DOCUMENTATION")
print("-" * 70)
print("""
Examples in examples/ directory:
    - comprehensive_example.py     → Full feature demo
    - config_example.py            → Configuration management
    - api_example.py               → API server usage

Documentation:
    - README.md                    → Main documentation
    - docs/API.md                  → API reference
    - docs/DEPLOYMENT.md           → Deployment guides
    - CONTRIBUTING.md              → Development guide

Run examples:
    python examples/comprehensive_example.py
    python examples/config_example.py
    python examples/api_example.py
""")

print("\n" + "=" * 70)
print("Need help? Check GitHub: https://github.com/MUKILAN0608/ai_safety_lib")
print("=" * 70)
