"""Configuration management module."""

from typing import Dict, Any, Optional
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class SafetyConfig:
    """Safety gate configuration."""

    confidence_threshold: float = 0.7
    drift_threshold: float = 0.3
    allow_warning: bool = False
    fairness_threshold: float = 0.8


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""

    enable_alerts: bool = True
    alert_thresholds: Dict[str, float] = None
    metrics_retention_days: int = 30

    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "accuracy": 0.7,
                "error_rate": 0.1,
                "latency_ms": 1000.0,
            }


@dataclass
class Config:
    """Main configuration container."""

    safety: SafetyConfig = None
    monitoring: MonitoringConfig = None

    def __post_init__(self):
        if self.safety is None:
            self.safety = SafetyConfig()
        if self.monitoring is None:
            self.monitoring = MonitoringConfig()


class ConfigManager:
    """Manage configuration loading and saving."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config manager.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = Config()

    def load_from_file(self, filepath: Path) -> Config:
        """
        Load configuration from file.

        Args:
            filepath: Path to config file (JSON or YAML)

        Returns:
            Config object
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        with open(filepath, "r") as f:
            if filepath.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif filepath.suffix == ".json":
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {filepath.suffix}")

        return self._dict_to_config(data)

    def save_to_file(self, filepath: Path, config: Optional[Config] = None) -> None:
        """
        Save configuration to file.

        Args:
            filepath: Path to save config file
            config: Config object to save (uses self.config if None)
        """
        filepath = Path(filepath)
        config = config or self.config

        data = self._config_to_dict(config)

        with open(filepath, "w") as f:
            if filepath.suffix in [".yaml", ".yml"]:
                yaml.dump(data, f, default_flow_style=False)
            elif filepath.suffix == ".json":
                json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported config format: {filepath.suffix}")

    def _dict_to_config(self, data: Dict[str, Any]) -> Config:
        """Convert dictionary to Config object."""
        safety_data = data.get("safety", {})
        monitoring_data = data.get("monitoring", {})

        return Config(
            safety=SafetyConfig(**safety_data),
            monitoring=MonitoringConfig(**monitoring_data),
        )

    def _config_to_dict(self, config: Config) -> Dict[str, Any]:
        """Convert Config object to dictionary."""
        return {
            "safety": asdict(config.safety),
            "monitoring": asdict(config.monitoring),
        }

    def load_from_env(self) -> Config:
        """Load configuration from environment variables."""
        import os

        config = Config()

        # Load safety config from env
        if os.getenv("SAFETY_CONFIDENCE_THRESHOLD"):
            config.safety.confidence_threshold = float(os.getenv("SAFETY_CONFIDENCE_THRESHOLD"))
        if os.getenv("SAFETY_DRIFT_THRESHOLD"):
            config.safety.drift_threshold = float(os.getenv("SAFETY_DRIFT_THRESHOLD"))
        if os.getenv("SAFETY_ALLOW_WARNING"):
            config.safety.allow_warning = os.getenv("SAFETY_ALLOW_WARNING").lower() == "true"

        # Load monitoring config from env
        if os.getenv("MONITORING_ENABLE_ALERTS"):
            config.monitoring.enable_alerts = (
                os.getenv("MONITORING_ENABLE_ALERTS").lower() == "true"
            )

        return config


# Default configuration
DEFAULT_CONFIG = Config()
