"""Demo script for AI Safety Library."""

import numpy as np
from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.utils import format_assessment_report


def main():
    """Run demo of AI safety monitoring."""
    print("AI Safety Library Demo\n")
    
    # Initialize safety gate
    safety_gate = SafetyGate(
        confidence_threshold=0.7,
        drift_threshold=0.3,
        allow_warning=False
    )
    
    # Generate sample data
    np.random.seed(42)
    
    # Simulate model predictions (confidence scores)
    predictions = np.random.uniform(0.6, 0.95, 100).tolist()
    
    # Simulate reference and current datasets for drift detection
    reference_data = {
        "feature_1": np.random.normal(0, 1, 50).tolist(),
        "feature_2": np.random.normal(0, 1, 50).tolist(),
    }
    
    current_data = {
        "feature_1": np.random.normal(0.1, 1, 50).tolist(),
        "feature_2": np.random.normal(0, 1.1, 50).tolist(),
    }
    
    # Evaluate safety
    print("Evaluating model safety...")
    assessment = safety_gate.evaluate(
        predictions=predictions,
        reference_data=reference_data,
        current_data=current_data,
        dataset_name="demo_dataset"
    )
    
    # Display results
    report = format_assessment_report(vars(assessment), verbose=True)
    print(report)
    
    # Check if model should be deployed
    should_deploy = safety_gate.should_deploy(assessment)
    print(f"\nShould deploy: {should_deploy}")
    
    # Show audit log
    print(f"\nAudit Log Entries: {len(safety_gate.get_audit_log())}")


if __name__ == "__main__":
    main()
