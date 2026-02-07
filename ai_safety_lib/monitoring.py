"""Performance monitoring and alerting module."""

from typing import List, Dict, Any, Optional, Callable
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""
    timestamp: datetime
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    latency_ms: Optional[float] = None
    throughput: Optional[float] = None
    error_rate: Optional[float] = None


@dataclass
class Alert:
    """Alert notification."""
    severity: AlertSeverity
    message: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.now)


class PerformanceMonitor:
    """Monitor model performance metrics over time."""
    
    def __init__(
        self,
        alert_thresholds: Optional[Dict[str, float]] = None,
        alert_callback: Optional[Callable[[Alert], None]] = None
    ):
        """
        Initialize performance monitor.
        
        Args:
            alert_thresholds: Dictionary of metric names to threshold values
            alert_callback: Callback function to call when alert is triggered
        """
        self.metrics_history: List[PerformanceMetrics] = []
        self.alert_thresholds = alert_thresholds or {
            'accuracy': 0.7,
            'error_rate': 0.1,
            'latency_ms': 1000.0
        }
        self.alert_callback = alert_callback
        self.alerts: List[Alert] = []
    
    def record_metrics(
        self,
        accuracy: Optional[float] = None,
        precision: Optional[float] = None,
        recall: Optional[float] = None,
        f1_score: Optional[float] = None,
        latency_ms: Optional[float] = None,
        throughput: Optional[float] = None,
        error_rate: Optional[float] = None
    ) -> PerformanceMetrics:
        """
        Record performance metrics.
        
        Returns:
            PerformanceMetrics object
        """
        metrics = PerformanceMetrics(
            timestamp=datetime.now(),
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            latency_ms=latency_ms,
            throughput=throughput,
            error_rate=error_rate
        )
        
        self.metrics_history.append(metrics)
        self._check_alerts(metrics)
        
        return metrics
    
    def _check_alerts(self, metrics: PerformanceMetrics) -> None:
        """Check if any metrics violate thresholds and trigger alerts."""
        # Check accuracy
        if metrics.accuracy is not None:
            threshold = self.alert_thresholds.get('accuracy')
            if threshold and metrics.accuracy < threshold:
                self._trigger_alert(
                    AlertSeverity.CRITICAL,
                    f"Accuracy dropped below threshold: {metrics.accuracy:.3f} < {threshold}",
                    "accuracy",
                    metrics.accuracy,
                    threshold
                )
        
        # Check error rate
        if metrics.error_rate is not None:
            threshold = self.alert_thresholds.get('error_rate')
            if threshold and metrics.error_rate > threshold:
                self._trigger_alert(
                    AlertSeverity.WARNING,
                    f"Error rate exceeded threshold: {metrics.error_rate:.3f} > {threshold}",
                    "error_rate",
                    metrics.error_rate,
                    threshold
                )
        
        # Check latency
        if metrics.latency_ms is not None:
            threshold = self.alert_thresholds.get('latency_ms')
            if threshold and metrics.latency_ms > threshold:
                self._trigger_alert(
                    AlertSeverity.WARNING,
                    f"Latency exceeded threshold: {metrics.latency_ms:.1f}ms > {threshold}ms",
                    "latency_ms",
                    metrics.latency_ms,
                    threshold
                )
    
    def _trigger_alert(
        self,
        severity: AlertSeverity,
        message: str,
        metric_name: str,
        current_value: float,
        threshold: float
    ) -> None:
        """Trigger an alert."""
        alert = Alert(
            severity=severity,
            message=message,
            metric_name=metric_name,
            current_value=current_value,
            threshold=threshold
        )
        
        self.alerts.append(alert)
        
        if self.alert_callback:
            self.alert_callback(alert)
    
    def get_metrics_summary(self, last_n: Optional[int] = None) -> Dict[str, Any]:
        """
        Get summary of recent metrics.
        
        Args:
            last_n: Number of recent metrics to include (None for all)
            
        Returns:
            Dictionary with metric summaries
        """
        if not self.metrics_history:
            return {}
        
        recent_metrics = self.metrics_history[-last_n:] if last_n else self.metrics_history
        
        summary = {}
        
        # Calculate averages for each metric
        for metric_name in ['accuracy', 'precision', 'recall', 'f1_score', 
                            'latency_ms', 'throughput', 'error_rate']:
            values = [
                getattr(m, metric_name) 
                for m in recent_metrics 
                if getattr(m, metric_name) is not None
            ]
            
            if values:
                summary[metric_name] = {
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'latest': values[-1]
                }
        
        return summary
    
    def get_recent_alerts(
        self,
        severity: Optional[AlertSeverity] = None,
        limit: Optional[int] = None
    ) -> List[Alert]:
        """
        Get recent alerts.
        
        Args:
            severity: Filter by severity level
            limit: Maximum number of alerts to return
            
        Returns:
            List of Alert objects
        """
        alerts = self.alerts
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        if limit:
            alerts = alerts[-limit:]
        
        return alerts
    
    def calculate_metrics_from_predictions(
        self,
        predictions: List[float],
        true_labels: List[int],
        threshold: float = 0.5
    ) -> Dict[str, float]:
        """
        Calculate classification metrics from predictions.
        
        Args:
            predictions: Model predictions (probabilities)
            true_labels: True labels (0 or 1)
            threshold: Classification threshold
            
        Returns:
            Dictionary of calculated metrics
        """
        binary_preds = [1 if p >= threshold else 0 for p in predictions]
        
        # Calculate confusion matrix values
        tp = sum(1 for i in range(len(true_labels)) 
                if true_labels[i] == 1 and binary_preds[i] == 1)
        fp = sum(1 for i in range(len(true_labels)) 
                if true_labels[i] == 0 and binary_preds[i] == 1)
        tn = sum(1 for i in range(len(true_labels)) 
                if true_labels[i] == 0 and binary_preds[i] == 0)
        fn = sum(1 for i in range(len(true_labels)) 
                if true_labels[i] == 1 and binary_preds[i] == 0)
        
        # Calculate metrics
        accuracy = (tp + tn) / len(true_labels) if true_labels else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }
