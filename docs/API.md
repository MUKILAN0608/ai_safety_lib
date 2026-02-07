# API Documentation

## REST API Endpoints

The AI Safety Library provides a comprehensive REST API for safety monitoring, risk assessment, fairness evaluation, and explainability analysis.

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
**GET** `/health`

Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-07T12:00:00"
}
```

---

#### 2. Safety Evaluation
**POST** `/evaluate`

Evaluate model safety based on predictions, drift detection, and risk assessment.

**Request Body:**
```json
{
  "predictions": [0.85, 0.92, 0.78, ...],
  "reference_data": {
    "feature_1": [1.2, 3.4, 2.1, ...],
    "feature_2": [5.6, 7.8, 6.3, ...]
  },
  "current_data": {
    "feature_1": [1.3, 3.5, 2.2, ...],
    "feature_2": [5.7, 7.9, 6.4, ...]
  },
  "dataset_name": "production_data"
}
```

**Response:**
```json
{
  "overall_risk": 0.25,
  "risk_level": "safe",
  "component_risks": {
    "confidence": 0.0,
    "drift": 0.5
  },
  "recommendations": [],
  "should_deploy": true,
  "timestamp": "2026-02-07T12:00:00"
}
```

---

#### 3. Record Performance Metrics
**POST** `/metrics`

Record model performance metrics for monitoring.

**Request Body:**
```json
{
  "accuracy": 0.85,
  "precision": 0.82,
  "recall": 0.88,
  "f1_score": 0.85,
  "latency_ms": 120.5,
  "throughput": 1000.0,
  "error_rate": 0.03
}
```

**Response:**
```json
{
  "status": "recorded",
  "timestamp": "2026-02-07T12:00:00",
  "metrics": { ... }
}
```

---

#### 4. Get Metrics Summary
**GET** `/metrics/summary?last_n=10`

Get summary statistics of recent metrics.

**Query Parameters:**
- `last_n` (optional): Number of recent metrics to include

**Response:**
```json
{
  "summary": {
    "accuracy": {
      "mean": 0.85,
      "std": 0.02,
      "min": 0.82,
      "max": 0.88,
      "latest": 0.85
    },
    ...
  },
  "timestamp": "2026-02-07T12:00:00"
}
```

---

#### 5. Get Alerts
**GET** `/alerts?severity=critical&limit=10`

Retrieve recent alerts.

**Query Parameters:**
- `severity` (optional): Filter by severity (info/warning/critical)
- `limit` (optional): Maximum number of alerts to return

**Response:**
```json
{
  "alerts": [
    {
      "severity": "critical",
      "message": "Accuracy dropped below threshold",
      "metric_name": "accuracy",
      "current_value": 0.65,
      "threshold": 0.7,
      "timestamp": "2026-02-07T12:00:00"
    }
  ]
}
```

---

#### 6. Fairness Analysis
**POST** `/fairness/analyze`

Analyze model fairness across protected groups.

**Request Body:**
```json
{
  "predictions": [0.8, 0.9, ...],
  "protected_groups": ["Group_A", "Group_B", ...],
  "true_labels": [1, 0, ...],
  "privileged_group": "Group_A"
}
```

**Response:**
```json
{
  "reports": [
    {
      "protected_attribute": "group",
      "metric_type": "demographic_parity",
      "score": 0.85,
      "is_fair": true,
      "group_metrics": {
        "Group_A": 0.75,
        "Group_B": 0.70
      },
      "threshold": 0.8
    }
  ]
}
```

---

#### 7. Explainability Analysis
**POST** `/explain`

Generate feature importance explanations.

**Request Body:**
```json
{
  "feature_values": {
    "age": [25, 30, 35, ...],
    "income": [50000, 60000, 70000, ...]
  },
  "predictions": [0.8, 0.9, ...],
  "top_k": 5
}
```

**Response:**
```json
{
  "feature_importances": [
    {
      "feature_name": "income",
      "importance_score": 0.85,
      "rank": 1
    },
    {
      "feature_name": "age",
      "importance_score": 0.72,
      "rank": 2
    }
  ]
}
```

---

#### 8. Audit Log
**GET** `/audit-log`

Get audit trail of all safety evaluations.

**Response:**
```json
{
  "audit_log": [
    {
      "overall_risk": 0.25,
      "risk_level": "safe",
      "component_risks": { ... },
      "metrics": { ... }
    }
  ],
  "count": 10
}
```

---

## Running the API Server

### Development Mode
```bash
python api_server.py
```

### Production Mode with Uvicorn
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
docker build -t ai-safety-api .
docker run -p 8000:8000 ai-safety-api
```

### With Docker Compose
```bash
docker-compose up
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
