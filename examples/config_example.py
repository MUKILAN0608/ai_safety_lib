"""Example: Using configuration management."""

from pathlib import Path
from ai_safety_lib.config import ConfigManager, Config, SafetyConfig, MonitoringConfig
from ai_safety_lib.safety_gate import SafetyGate


def main():
    """Demonstrate configuration management."""
    print("Configuration Management Example\n")
    
    # Create a custom configuration
    config = Config(
        safety=SafetyConfig(
            confidence_threshold=0.75,
            drift_threshold=0.25,
            allow_warning=True,
            fairness_threshold=0.85
        ),
        monitoring=MonitoringConfig(
            enable_alerts=True,
            alert_thresholds={
                'accuracy': 0.8,
                'error_rate': 0.05,
                'latency_ms': 500.0
            },
            metrics_retention_days=60
        )
    )
    
    # Save configuration to file
    config_manager = ConfigManager()
    config_path = Path("config_example.json")
    config_manager.save_to_file(config_path, config)
    print(f"✓ Configuration saved to {config_path}")
    
    # Load configuration from file
    loaded_config = config_manager.load_from_file(config_path)
    print(f"✓ Configuration loaded from {config_path}")
    print(f"\nSafety Config:")
    print(f"  Confidence Threshold: {loaded_config.safety.confidence_threshold}")
    print(f"  Drift Threshold: {loaded_config.safety.drift_threshold}")
    print(f"  Allow Warning: {loaded_config.safety.allow_warning}")
    
    print(f"\nMonitoring Config:")
    print(f"  Enable Alerts: {loaded_config.monitoring.enable_alerts}")
    print(f"  Alert Thresholds: {loaded_config.monitoring.alert_thresholds}")
    
    # Use configuration with safety gate
    safety_gate = SafetyGate(
        confidence_threshold=loaded_config.safety.confidence_threshold,
        drift_threshold=loaded_config.safety.drift_threshold,
        allow_warning=loaded_config.safety.allow_warning
    )
    
    print(f"\n✓ SafetyGate initialized with loaded configuration")
    
    # Clean up
    config_path.unlink()
    print(f"\n✓ Example config file deleted")


if __name__ == "__main__":
    main()
