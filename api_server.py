"""FastAPI server for AI Safety Library."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime

from ai_safety_lib.safety_gate import SafetyGate
from ai_safety_lib.monitoring import PerformanceMonitor, Alert
from ai_safety_lib.fairness import FairnessAnalyzer
from ai_safety_lib.explainability import ExplainabilityAnalyzer


# Pydantic models for API
class PredictionRequest(BaseModel):
    """Request model for safety evaluation."""
    predictions: List[float] = Field(..., description="Model predictions")
    reference_data: Dict[str, List[float]] = Field(..., description="Reference dataset")
    current_data: Dict[str, List[float]] = Field(..., description="Current dataset")
    dataset_name: str = Field(default="default", description="Dataset name")


class SafetyResponse(BaseModel):
    """Response model for safety evaluation."""
    overall_risk: float
    risk_level: str
    component_risks: Dict[str, float]
    recommendations: List[str]
    should_deploy: bool
    timestamp: datetime = Field(default_factory=datetime.now)


class MetricsRequest(BaseModel):
    """Request model for performance metrics."""
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    latency_ms: Optional[float] = None
    throughput: Optional[float] = None
    error_rate: Optional[float] = None


class FairnessRequest(BaseModel):
    """Request model for fairness analysis."""
    predictions: List[float]
    protected_groups: List[str]
    true_labels: Optional[List[int]] = None
    privileged_group: Optional[str] = None


class ExplainabilityRequest(BaseModel):
    """Request model for explainability analysis."""
    feature_values: Dict[str, List[float]]
    predictions: List[float]
    top_k: int = Field(default=5, description="Number of top features")


# Initialize FastAPI app
app = FastAPI(
    title="AI Safety Library API",
    description="REST API for AI safety monitoring, risk assessment, and fairness evaluation",
    version="0.2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
safety_gate = SafetyGate()
performance_monitor = PerformanceMonitor()
fairness_analyzer = FairnessAnalyzer()
explainability_analyzer = ExplainabilityAnalyzer()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AI Safety Library API",
        "version": "0.2.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}


@app.post("/evaluate", response_model=SafetyResponse)
async def evaluate_safety(request: PredictionRequest):
    """
    Evaluate model safety.
    
    Analyzes predictions for confidence and drift, performs risk assessment,
    and determines if the model should be deployed.
    """
    try:
        assessment = safety_gate.evaluate(
            predictions=request.predictions,
            reference_data=request.reference_data,
            current_data=request.current_data,
            dataset_name=request.dataset_name
        )
        
        should_deploy = safety_gate.should_deploy(assessment)
        
        return SafetyResponse(
            overall_risk=assessment.overall_risk,
            risk_level=assessment.risk_level.value,
            component_risks=assessment.component_risks,
            recommendations=assessment.recommendations,
            should_deploy=should_deploy
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics")
async def record_metrics(request: MetricsRequest):
    """Record performance metrics."""
    try:
        metrics = performance_monitor.record_metrics(
            accuracy=request.accuracy,
            precision=request.precision,
            recall=request.recall,
            f1_score=request.f1_score,
            latency_ms=request.latency_ms,
            throughput=request.throughput,
            error_rate=request.error_rate
        )
        
        return {
            "status": "recorded",
            "timestamp": metrics.timestamp,
            "metrics": request.dict(exclude_none=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/summary")
async def get_metrics_summary(last_n: Optional[int] = None):
    """Get metrics summary."""
    try:
        summary = performance_monitor.get_metrics_summary(last_n=last_n)
        return {"summary": summary, "timestamp": datetime.now()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts")
async def get_alerts(severity: Optional[str] = None, limit: Optional[int] = 10):
    """Get recent alerts."""
    try:
        from ai_safety_lib.monitoring import AlertSeverity
        
        severity_filter = AlertSeverity(severity) if severity else None
        alerts = performance_monitor.get_recent_alerts(
            severity=severity_filter,
            limit=limit
        )
        
        return {
            "alerts": [
                {
                    "severity": alert.severity.value,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold,
                    "timestamp": alert.timestamp
                }
                for alert in alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fairness/analyze")
async def analyze_fairness(request: FairnessRequest):
    """Analyze model fairness."""
    try:
        reports = fairness_analyzer.comprehensive_fairness_check(
            predictions=request.predictions,
            protected_groups=request.protected_groups,
            true_labels=request.true_labels,
            privileged_group=request.privileged_group
        )
        
        return {
            "reports": [
                {
                    "protected_attribute": report.protected_attribute,
                    "metric_type": report.metric_type.value,
                    "score": report.score,
                    "is_fair": report.is_fair,
                    "group_metrics": report.group_metrics,
                    "threshold": report.threshold
                }
                for report in reports
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def explain_predictions(request: ExplainabilityRequest):
    """Generate explanations for predictions."""
    try:
        # Calculate feature importance
        feature_importances = explainability_analyzer.calculate_feature_importance(
            feature_values=request.feature_values,
            predictions=request.predictions
        )
        
        return {
            "feature_importances": [
                {
                    "feature_name": fi.feature_name,
                    "importance_score": fi.importance_score,
                    "rank": fi.rank
                }
                for fi in feature_importances[:request.top_k]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit-log")
async def get_audit_log():
    """Get audit log of safety evaluations."""
    try:
        log = safety_gate.get_audit_log()
        return {"audit_log": log, "count": len(log)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the API server."""
    uvicorn.run("api_server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server(reload=True)
