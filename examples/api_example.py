"""Example: Using the FastAPI server."""

import requests
import numpy as np


def main():
    """Demonstrate API usage with examples."""
    base_url = "http://localhost:8000"
    
    print("AI Safety Library API Example")
    print("Make sure the API server is running: python api_server.py\n")
    
    # Check health
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Server health: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: API server is not running!")
        print("Start it with: python api_server.py")
        return
    
    # Prepare test data
    np.random.seed(42)
    predictions = np.random.uniform(0.7, 0.95, 50).tolist()
    reference_data = {
        "feature_1": np.random.normal(0, 1, 50).tolist(),
        "feature_2": np.random.normal(0, 1, 50).tolist(),
    }
    current_data = {
        "feature_1": np.random.normal(0.1, 1.1, 50).tolist(),
        "feature_2": np.random.normal(0, 1, 50).tolist(),
    }
    
    # 1. Evaluate safety
    print("\n1. Safety Evaluation")
    print("-" * 60)
    
    eval_request = {
        "predictions": predictions,
        "reference_data": reference_data,
        "current_data": current_data,
        "dataset_name": "api_test"
    }
    
    response = requests.post(f"{base_url}/evaluate", json=eval_request)
    evaluation = response.json()
    
    print(f"Overall Risk: {evaluation['overall_risk']:.3f}")
    print(f"Risk Level: {evaluation['risk_level']}")
    print(f"Should Deploy: {'✅ Yes' if evaluation['should_deploy'] else '❌ No'}")
    print(f"Recommendations: {evaluation['recommendations']}")
    
    # 2. Record performance metrics
    print("\n2. Record Performance Metrics")
    print("-" * 60)
    
    metrics_request = {
        "accuracy": 0.85,
        "precision": 0.82,
        "recall": 0.88,
        "f1_score": 0.85,
        "latency_ms": 120.5,
        "error_rate": 0.03
    }
    
    response = requests.post(f"{base_url}/metrics", json=metrics_request)
    print(f"✓ Metrics recorded: {response.json()['status']}")
    
    # 3. Get metrics summary
    print("\n3. Metrics Summary")
    print("-" * 60)
    
    response = requests.get(f"{base_url}/metrics/summary")
    summary = response.json()['summary']
    
    for metric_name, stats in summary.items():
        print(f"{metric_name}:")
        print(f"  Mean: {stats['mean']:.3f}")
        print(f"  Latest: {stats['latest']:.3f}")
    
    # 4. Fairness analysis
    print("\n4. Fairness Analysis")
    print("-" * 60)
    
    fairness_request = {
        "predictions": predictions,
        "protected_groups": ["Group_A"] * 25 + ["Group_B"] * 25,
        "true_labels": [1, 0] * 25,
        "privileged_group": "Group_A"
    }
    
    response = requests.post(f"{base_url}/fairness/analyze", json=fairness_request)
    fairness_reports = response.json()['reports']
    
    for report in fairness_reports:
        status = "✅ FAIR" if report['is_fair'] else "⚠️ BIASED"
        print(f"{report['metric_type']}: {status} (score: {report['score']:.3f})")
    
    # 5. Explainability
    print("\n5. Explainability Analysis")
    print("-" * 60)
    
    explain_request = {
        "feature_values": current_data,
        "predictions": predictions,
        "top_k": 2
    }
    
    response = requests.post(f"{base_url}/explain", json=explain_request)
    importances = response.json()['feature_importances']
    
    print("Top Features:")
    for feat in importances:
        print(f"  {feat['rank']}. {feat['feature_name']}: {feat['importance_score']:.4f}")
    
    # 6. Get alerts
    print("\n6. Recent Alerts")
    print("-" * 60)
    
    response = requests.get(f"{base_url}/alerts?limit=5")
    alerts = response.json()['alerts']
    
    if alerts:
        for alert in alerts:
            print(f"[{alert['severity']}] {alert['message']}")
    else:
        print("No alerts ✅")
    
    print("\n" + "=" * 60)
    print("API example complete!")


if __name__ == "__main__":
    main()
