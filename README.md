<div align="center">

# 🛰️ DisasterAI — Multimodal Disaster Response System

**A real-time AI dashboard that fuses satellite imagery analysis, NLP distress signals, sensor anomaly detection, and audio classification to assess disaster zones and recommend emergency actions.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Multimodal%20AI-blueviolet?style=flat)](https://github.com/)
[![Server](https://img.shields.io/badge/Server-Python%20HTTP%20(zero%20deps)-lightgrey?style=flat)](https://docs.python.org/3/library/http.server.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## Overview

DisasterAI is a prototype multimodal AI system for disaster zone triage. It simulates how a real emergency response platform would combine four independent AI modalities — satellite vision, natural language signals, IoT sensor streams, and audio classification — and fuse their outputs into a single, actionable risk score per zone.

The system runs as a self-contained Python HTTP server with a live web dashboard, requiring **zero external dependencies**.

## Why This Project

This project demonstrates applied AI engineering concepts at the system level:

- **Multimodal fusion** — combining heterogeneous signal types (visual, text, sensor, audio) into a unified risk estimate using weighted scoring.
- **Modular AI pipeline design** — each modality is an independent, swappable module with a consistent interface, mirroring production ML system architecture.
- **End-to-end delivery** — from raw simulated signals to a live, auto-refreshing web dashboard with no external framework required.
- **Real-world domain modeling** — disaster zone triage, urgency classification, anomaly detection, and action recommendation are all grounded in realistic emergency response logic.

## Live Dashboard

The system serves a real-time web dashboard on `http://localhost:5000` with:

- Zone-by-zone risk map with color-coded severity levels
- Per-zone breakdown of all 4 AI module outputs
- Weighted fusion score with confidence indicators
- Auto-generated recommended actions per zone
- Auto-refresh every 30 seconds

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │         DISASTER ZONE INPUT          │
                    │  (Location ID, Lat/Lon, Population)  │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼────────────────────────┐
              ▼                       ▼                        ▼                      ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │  MODULE 1        │  │  MODULE 2        │  │  MODULE 3        │  │  MODULE 4        │
   │  Visual Damage   │  │  NLP Distress    │  │  Sensor Anomaly  │  │  Audio           │
   │  Assessor        │  │  Extractor       │  │  Detector        │  │  Classifier      │
   │                  │  │                  │  │                  │  │                  │
   │  CNN simulation  │  │  BERT simulation │  │  LSTM simulation │  │  Whisper + CNN   │
   │  on satellite    │  │  on text signals │  │  on IoT sensor   │  │  on audio event  │
   │  imagery         │  │  from social,    │  │  time-series     │  │  streams         │
   │                  │  │  SMS, radio      │  │  data            │  │                  │
   │  → damage_class  │  │  → max_urgency   │  │  → sensor_risk   │  │  → audio_risk    │
   └──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
              │                       │                        │                      │
              └───────────────────────┼────────────────────────┘──────────────────────┘
                                      ▼
                    ┌─────────────────────────────────────┐
                    │   MODULE 5: MULTIMODAL FUSION ENGINE │
                    │                                     │
                    │   Score = 0.35×Visual + 0.30×NLP    │
                    │         + 0.20×Sensor + 0.15×Audio  │
                    │                                     │
                    │   → Fused Risk Score (0.0 – 1.0)    │
                    │   → Risk Level (Minimal → Critical)  │
                    │   → Recommended Emergency Actions    │
                    └─────────────────────────────────────┘
                                      │
                    ┌─────────────────────────────────────┐
                    │     LIVE WEB DASHBOARD (port 5000)   │
                    └─────────────────────────────────────┘
```

## AI Modules

| Module | Simulated Model | Input | Output |
|---|---|---|---|
| Visual Damage Assessor | CNN (Sentinel-2 satellite) | Location coordinates | Damage class (0–3), confidence |
| NLP Distress Extractor | BERT text classifier | Zone ID → distress messages | Urgency score, signal categories |
| Sensor Anomaly Detector | LSTM on time-series | Zone ID → sensor streams | Anomaly count, risk score |
| Audio Classifier | Whisper + CNN | Zone ID → audio events | Event type, severity, transcript |
| Multimodal Fusion Engine | Weighted ensemble | All 4 module outputs | Final risk score + actions |

## Risk Levels

| Score Range | Level | Label |
|---|---|---|
| 0.0 – 0.2 | 1 | 🟢 Minimal |
| 0.2 – 0.4 | 2 | 🟡 Low |
| 0.4 – 0.6 | 3 | 🟠 Moderate |
| 0.6 – 0.8 | 4 | 🔴 High |
| 0.8 – 1.0 | 5 | 🚨 Critical |

## Getting Started

### Prerequisites

- Python 3.9+
- No external packages required — uses only the Python standard library

### Run

```bash
git clone https://github.com/Thenmozhi-codes/disaster-ai.git
cd disaster-ai
python prototype.py
```

Then open your browser at:

```
http://localhost:5000
```

### API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Live web dashboard |
| `GET /api/zones` | Summary of all zones, sorted by risk score |
| `GET /api/zone/{id}` | Full multimodal analysis for a specific zone |

## Project Structure

```
disaster-ai/
├── prototype.py     # All modules, fusion engine, HTTP server, and dashboard
└── README.md
```

## Disaster Zones (Mock Data)

The system simulates 8 zones modelled on a metropolitan area:

- Downtown Core, Riverside District, Harbor Area, North Hills
- East Industrial, Medical District, Airport Zone, Westside Residential

## Roadmap

- [ ] Connect to real Sentinel-2 satellite image API
- [ ] Integrate live social media NLP (Twitter/X API)
- [ ] Replace simulated LSTM with real IoT sensor feeds
- [ ] Add WebSocket for real-time push updates
- [ ] Deploy as a cloud-hosted demo (Render / Railway)
- [ ] Export reports as PDF / CSV

## About

Built as a portfolio prototype to explore multimodal AI system design — specifically how multiple independent models can be fused together into a single, actionable decision system for high-stakes domains.

**Author:** Thenmozhi Sivanesan

## License

MIT License — free to use, modify, and build on.