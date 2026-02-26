# 📡 EcoPulse AI: API Reference Guide

This document provides a detailed overview of the available REST API endpoints within the EcoPulse AI ecosystem. These endpoints facilitate communication between the presentation layer, the streaming analytics engine, and the AI intelligence services.

---

## 🔐 Authentication
All routes except `/login` require a valid session cookie managed by Flask-Login.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Authenticate a user and start a session. |
| `GET` | `/logout` | Terminate the current user session. |

---

## 📊 Environmental Telemetry

### 1. Get Real-Time Metrics
Returns the latest environmental telemetry, including alerts and forecasts.

- **Endpoint**: `/api/metrics`
- **Method**: `GET`
- **Response Example**:
```json
{
  "latest": {
    "aqi": 65.4,
    "co2": 420.1,
    "health_score": 88.5,
    "severity": "Optimal",
    "attribution": {
      "traffic": 45.2,
      "industrial": 30.1
    }
  },
  "alerts": [],
  "forecast": 67.2,
  "history": [...]
}
```

### 2. Get National Context
Fetches a high-level overview of environmental conditions across different regions.

- **Endpoint**: `/api/national`
- **Method**: `GET`

### 3. Get District Comparison
Returns a comparative analysis of different city districts.

- **Endpoint**: `/api/districts`
- **Method**: `GET`

---

## 🧠 AI & Reasoning

### 1. Climate Copilot Chat
Interacts with the LLM-powered scientific advisor, providing real-time data context.

- **Endpoint**: `/api/chat`
- **Method**: `POST`
- **Payload**:
```json
{
  "query": "Should I wear a mask today?"
}
```
- **Response**:
```json
{
  "response": "Based on the current AQI of 150 (Warning level), it is recommended to wear an N95 mask if spending extended time outdoors..."
}
```

### 2. Action Plan Generation
Generates a structured municipal response strategy.

- **Endpoint**: `/action-plan`
- **Method**: `GET`
- **Output**: HTML page rendered with AI-generated tactical mandates.

---

## 📄 Reporting & Exports

| Endpoint | Description |
| :--- | :--- |
| `/reports/export` | Generates a high-fidelity PDF 'Environmental Health Audit'. |
| `/reports/mayor-brief` | Generates a streamlined strategic 'Mayor Briefing' PDF. |

---

## 🛠️ Internal Simulation Engine
The system supports on-the-fly "What-if" simulations through the streaming engine.

- **Endpoint**: `/environmental_metrics` (Internal Pipeline Port: 8080)
- **Parameters**:
  - `traffic_reduction`: (0-100) Percentage of traffic to remove.
  - `industrial_restriction`: (0-100) Percentage of industrial activity to halt.
  - `green_cover`: (0-100) Percentage increase in urban greenery.
