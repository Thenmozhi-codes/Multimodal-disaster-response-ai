

import json
import time
import random
import math
import threading
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ─────────────────────────────────────────────
#  MODULE 1: VISUAL DAMAGE ASSESSMENT
#  Simulates satellite image analysis
# ─────────────────────────────────────────────
class VisualDamageAssessor:
    DAMAGE_LABELS = ["No Damage", "Minor Damage", "Major Damage", "Destroyed"]
    
    def assess(self, location_id, lat, lon):
        """Simulate CNN damage classification from satellite imagery."""
        # Deterministic but varied scores per location
        seed = hash(f"{location_id}{lat:.2f}{lon:.2f}") % 1000
        random.seed(seed + int(time.time() / 30))  # Changes every 30s
        
        scores = [random.uniform(0, 1) for _ in range(4)]
        total = sum(scores)
        probs = [s / total for s in scores]
        
        damage_class = probs.index(max(probs))
        confidence = max(probs)
        
        return {
            "module": "Visual Assessment",
            "damage_class": damage_class,
            "damage_label": self.DAMAGE_LABELS[damage_class],
            "confidence": round(confidence, 3),
            "probabilities": {
                label: round(p, 3) 
                for label, p in zip(self.DAMAGE_LABELS, probs)
            },
            "source": "Sentinel-2 Satellite (simulated)",
            "timestamp": datetime.now().isoformat()
        }


# ─────────────────────────────────────────────
#  MODULE 2: NLP DISTRESS SIGNAL EXTRACTOR
#  Simulates BERT-based text classification
# ─────────────────────────────────────────────
class NLPDistressExtractor:
    DISTRESS_MESSAGES = [
        {"text": "HELP! Family of 4 trapped under collapsed building on Oak Street!", "urgency": 5, "type": "Rescue"},
        {"text": "Water rising fast, need evacuation assistance at Riverside Ave", "urgency": 4, "type": "Evacuation"},
        {"text": "Medical emergency, elderly woman needs insulin, stranded on 3rd floor", "urgency": 5, "type": "Medical"},
        {"text": "No food or water for 2 days, shelter needed for 15 people", "urgency": 3, "type": "Shelter"},
        {"text": "Fire spreading from main street toward the school building", "urgency": 5, "type": "Fire"},
        {"text": "Road completely blocked by debris near the bridge, rescue teams cannot pass", "urgency": 3, "type": "Infrastructure"},
        {"text": "Gas leak detected near downtown area, strong smell coming from pipes", "urgency": 4, "type": "Hazmat"},
        {"text": "Two survivors spotted waving from rooftop of flooded apartment complex", "urgency": 4, "type": "Rescue"},
        {"text": "Hospital running low on generators, backup power failing", "urgency": 5, "type": "Critical Infrastructure"},
        {"text": "Children separated from parents near the main evacuation center", "urgency": 4, "type": "Missing Persons"},
        {"text": "Communication tower down, entire district has no phone signal", "urgency": 3, "type": "Communications"},
        {"text": "Landslide blocking highway, multiple vehicles trapped in mud", "urgency": 4, "type": "Rescue"},
    ]
    
    def extract_signals(self, zone_id):
        """Simulate NLP classification of incoming distress messages."""
        random.seed(zone_id * 7 + int(time.time() / 20))
        
        num_signals = random.randint(1, 4)
        signals = random.sample(self.DISTRESS_MESSAGES, min(num_signals, len(self.DISTRESS_MESSAGES)))
        
        results = []
        for sig in signals:
            results.append({
                "text": sig["text"],
                "urgency_score": sig["urgency"] / 5.0,
                "urgency_level": sig["urgency"],
                "category": sig["type"],
                "confidence": round(random.uniform(0.72, 0.97), 3),
                "source": random.choice(["Twitter/X", "Emergency Radio", "SMS Hotline", "Field Report"]),
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 45))).isoformat()
            })
        
        max_urgency = max(r["urgency_score"] for r in results) if results else 0
        return {
            "module": "NLP Distress Extractor",
            "signals_detected": len(results),
            "max_urgency": round(max_urgency, 3),
            "signals": results
        }


# ─────────────────────────────────────────────
#  MODULE 3: SENSOR ANOMALY DETECTOR
#  Simulates LSTM on seismic/weather sensors
# ─────────────────────────────────────────────
class SensorAnomalyDetector:
    SENSOR_TYPES = ["Seismic", "Flood Gauge", "Wind Speed", "Temperature", "Air Quality"]
    
    def _generate_time_series(self, sensor_type, base_val, anomaly=False):
        """Generate fake time-series data with optional anomaly spike."""
        readings = []
        val = base_val
        for i in range(12):  # Last 12 readings (1 hour)
            noise = random.gauss(0, base_val * 0.05)
            if anomaly and i >= 9:
                spike = base_val * random.uniform(0.4, 1.2)
                val += spike
            val = max(0, val + noise)
            readings.append(round(val, 2))
        return readings
    
    def analyze(self, zone_id):
        """Simulate LSTM anomaly detection on sensor streams."""
        random.seed(zone_id * 13 + int(time.time() / 60))
        
        sensors = []
        anomaly_count = 0
        
        for stype in self.SENSOR_TYPES:
            is_anomaly = random.random() < 0.35
            base_vals = {"Seismic": 0.2, "Flood Gauge": 1.5, "Wind Speed": 25, "Temperature": 28, "Air Quality": 45}
            base = base_vals.get(stype, 1.0)
            
            readings = self._generate_time_series(stype, base, anomaly=is_anomaly)
            anomaly_score = round(random.uniform(0.65, 0.95) if is_anomaly else random.uniform(0.05, 0.3), 3)
            
            if is_anomaly:
                anomaly_count += 1
                
            sensors.append({
                "type": stype,
                "readings": readings,
                "current": readings[-1],
                "anomaly_detected": is_anomaly,
                "anomaly_score": anomaly_score,
                "status": "ALERT" if is_anomaly else "Normal"
            })
        
        overall_risk = anomaly_count / len(self.SENSOR_TYPES)
        return {
            "module": "Sensor Anomaly Detector",
            "sensors": sensors,
            "anomalies_detected": anomaly_count,
            "overall_sensor_risk": round(overall_risk, 3)
        }


# ─────────────────────────────────────────────
#  MODULE 4: AUDIO CLASSIFIER
#  Simulates Whisper + CNN audio analysis
# ─────────────────────────────────────────────
class AudioClassifier:
    AUDIO_EVENTS = [
        {"event": "Structural Collapse Sound", "severity": 0.95},
        {"event": "People Calling for Help", "severity": 0.90},
        {"event": "Explosion Detected", "severity": 0.98},
        {"event": "Flooding/Water Rush", "severity": 0.75},
        {"event": "Emergency Siren", "severity": 0.60},
        {"event": "Background Noise Only", "severity": 0.05},
        {"event": "Crying/Distress Vocalization", "severity": 0.85},
        {"event": "Vehicle Crash", "severity": 0.70},
    ]
    
    TRANSCRIPTS = [
        "Help, we are trapped, please send rescue to block seven",
        "Fire on the second floor, evacuate the building now",
        "Multiple casualties reported, need medical teams immediately",
        "The bridge is cracking, do not attempt to cross",
        "Survivor located at grid reference four-niner-alpha",
        "We have a family with young children needing evacuation",
    ]
    
    def classify(self, zone_id):
        """Simulate audio event classification and speech transcription."""
        random.seed(zone_id * 3 + int(time.time() / 45))
        
        detected = random.sample(self.AUDIO_EVENTS, random.randint(1, 3))
        top_event = max(detected, key=lambda x: x["severity"])
        
        has_speech = random.random() > 0.4
        
        return {
            "module": "Audio Classifier",
            "events_detected": detected,
            "top_event": top_event["event"],
            "top_severity": top_event["severity"],
            "speech_detected": has_speech,
            "transcript": random.choice(self.TRANSCRIPTS) if has_speech else None,
            "audio_risk_score": round(top_event["severity"], 3),
            "source": random.choice(["Drone Microphone", "Field Radio", "Emergency Call Recording"])
        }


# ─────────────────────────────────────────────
#  MODULE 5: MULTIMODAL FUSION ENGINE
#  Combines all modality scores into final risk
# ─────────────────────────────────────────────
class MultimodalFusionEngine:
    # Weights for each modality (sum = 1.0)
    WEIGHTS = {
        "visual": 0.35,
        "nlp": 0.30,
        "sensor": 0.20,
        "audio": 0.15
    }
    
    RISK_LEVELS = {
        (0.0, 0.2): {"level": 1, "label": "Minimal", "color": "#22c55e"},
        (0.2, 0.4): {"level": 2, "label": "Low",     "color": "#84cc16"},
        (0.4, 0.6): {"level": 3, "label": "Moderate","color": "#f59e0b"},
        (0.6, 0.8): {"level": 4, "label": "High",    "color": "#f97316"},
        (0.8, 1.0): {"level": 5, "label": "Critical", "color": "#ef4444"},
    }
    
    def fuse(self, visual_result, nlp_result, sensor_result, audio_result):
        """Weighted fusion of all modality outputs."""
        
        # Extract risk scores from each module
        visual_risk = visual_result["damage_class"] / 3.0
        nlp_risk = nlp_result["max_urgency"]
        sensor_risk = sensor_result["overall_sensor_risk"]
        audio_risk = audio_result["audio_risk_score"]
        
        # Weighted combination
        fused_score = (
            visual_risk  * self.WEIGHTS["visual"] +
            nlp_risk     * self.WEIGHTS["nlp"] +
            sensor_risk  * self.WEIGHTS["sensor"] +
            audio_risk   * self.WEIGHTS["audio"]
        )
        fused_score = round(min(1.0, fused_score), 3)
        
        # Determine risk level
        risk_info = {"level": 3, "label": "Moderate", "color": "#f59e0b"}
        for (low, high), info in self.RISK_LEVELS.items():
            if low <= fused_score < high or (fused_score >= 0.8 and high == 1.0):
                risk_info = info
                break
        
        # Generate recommended actions
        actions = self._recommend_actions(fused_score, nlp_result, sensor_result, visual_result)
        
        return {
            "fused_risk_score": fused_score,
            "risk_level": risk_info["level"],
            "risk_label": risk_info["label"],
            "risk_color": risk_info["color"],
            "component_scores": {
                "visual": round(visual_risk, 3),
                "nlp": round(nlp_risk, 3),
                "sensor": round(sensor_risk, 3),
                "audio": round(audio_risk, 3)
            },
            "recommended_actions": actions,
            "last_updated": datetime.now().isoformat()
        }
    
    def _recommend_actions(self, score, nlp, sensor, visual):
        actions = []
        if score >= 0.8:
            actions.append("🚨 IMMEDIATE: Deploy search and rescue team")
            actions.append("🚁 Request aerial support / drone surveillance")
        if score >= 0.6:
            actions.append("🏥 Pre-position medical units at zone perimeter")
            actions.append("📡 Establish emergency communications relay")
        if nlp["max_urgency"] > 0.7:
            top = nlp["signals"][0] if nlp["signals"] else None
            if top:
                actions.append(f"📢 Respond to: {top['category']} — {top['text'][:60]}...")
        if sensor["anomalies_detected"] > 2:
            actions.append("⚠️ Multiple sensor anomalies — check structural integrity")
        if visual["damage_class"] >= 3:
            actions.append("🏗️ Heavy structural damage — restrict zone access")
        if not actions:
            actions.append("👁️ Continue monitoring — no immediate action required")
        return actions[:4]


# ─────────────────────────────────────────────
#  DISASTER ZONE MAP (Mock geographic data)
# ─────────────────────────────────────────────
DISASTER_ZONES = [
    {"id": 1, "name": "Downtown Core",      "lat": 34.052,  "lon": -118.243, "pop": 12400},
    {"id": 2, "name": "Riverside District", "lat": 34.058,  "lon": -118.251, "pop": 8700},
    {"id": 3, "name": "Harbor Area",        "lat": 34.044,  "lon": -118.237, "pop": 5200},
    {"id": 4, "name": "North Hills",        "lat": 34.065,  "lon": -118.248, "pop": 9100},
    {"id": 5, "name": "East Industrial",    "lat": 34.050,  "lon": -118.228, "pop": 3300},
    {"id": 6, "name": "Medical District",   "lat": 34.062,  "lon": -118.260, "pop": 6800},
    {"id": 7, "name": "Airport Zone",       "lat": 34.039,  "lon": -118.254, "pop": 2100},
    {"id": 8, "name": "Westside Res.",      "lat": 34.055,  "lon": -118.267, "pop": 14200},
]

# Initialize all modules
visual_module  = VisualDamageAssessor()
nlp_module     = NLPDistressExtractor()
sensor_module  = SensorAnomalyDetector()
audio_module   = AudioClassifier()
fusion_engine  = MultimodalFusionEngine()


def analyze_zone(zone):
    """Run full multimodal analysis on a single zone."""
    z_id = zone["id"]
    visual  = visual_module.assess(z_id, zone["lat"], zone["lon"])
    nlp     = nlp_module.extract_signals(z_id)
    sensor  = sensor_module.analyze(z_id)
    audio   = audio_module.classify(z_id)
    fusion  = fusion_engine.fuse(visual, nlp, sensor, audio)
    
    return {
        "zone": zone,
        "visual": visual,
        "nlp": nlp,
        "sensor": sensor,
        "audio": audio,
        "fusion": fusion
    }


def get_all_zones_summary():
    """Quick summary of all zones for the map view."""
    results = []
    for zone in DISASTER_ZONES:
        data = analyze_zone(zone)
        results.append({
            "id": zone["id"],
            "name": zone["name"],
            "lat": zone["lat"],
            "lon": zone["lon"],
            "population": zone["pop"],
            "risk_score": data["fusion"]["fused_risk_score"],
            "risk_level": data["fusion"]["risk_level"],
            "risk_label": data["fusion"]["risk_label"],
            "risk_color": data["fusion"]["risk_color"],
            "top_action": data["fusion"]["recommended_actions"][0] if data["fusion"]["recommended_actions"] else "",
            "damage_label": data["visual"]["damage_label"],
            "signals": data["nlp"]["signals_detected"],
            "sensor_anomalies": data["sensor"]["anomalies_detected"]
        })
    return sorted(results, key=lambda x: x["risk_score"], reverse=True)


# ─────────────────────────────────────────────
#  WEB DASHBOARD (Served via built-in HTTP)
# ─────────────────────────────────────────────
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DisasterAI — Multimodal Response System</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:       #050a0f;
    --surface:  #0a1520;
    --panel:    #0d1e2e;
    --border:   #1a3a5c;
    --accent:   #00d4ff;
    --accent2:  #ff6b35;
    --text:     #c8e6f5;
    --dim:      #4a7a9b;
    --green:    #22c55e;
    --yellow:   #f59e0b;
    --orange:   #f97316;
    --red:      #ef4444;
    --font-mono: 'Share Tech Mono', monospace;
    --font-ui:   'Rajdhani', sans-serif;
    --font-body: 'Exo 2', sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { 
    background: var(--bg); 
    color: var(--text);
    font-family: var(--font-body);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Grid background */
  body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image: 
      linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }

  /* ── HEADER ── */
  header {
    position: relative; z-index: 10;
    background: linear-gradient(135deg, #050e1a 0%, #081525 100%);
    border-bottom: 1px solid var(--border);
    padding: 12px 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 30px rgba(0,0,0,0.6);
  }
  .logo {
    display: flex; align-items: center; gap: 14px;
  }
  .logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, var(--accent), #0084ff);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(0,212,255,0.4);
  }
  .logo-text { 
    font-family: var(--font-ui); 
    font-size: 22px; font-weight: 700; 
    color: #fff; letter-spacing: 1px;
  }
  .logo-sub { font-size: 11px; color: var(--dim); letter-spacing: 2px; text-transform: uppercase; }

  .header-right { display: flex; align-items: center; gap: 20px; }
  .live-badge {
    display: flex; align-items: center; gap: 8px;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    padding: 6px 14px; border-radius: 20px;
    font-family: var(--font-mono); font-size: 12px; color: var(--green);
  }
  .live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green);
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
    50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(34,197,94,0); }
  }
  .clock { font-family: var(--font-mono); font-size: 13px; color: var(--accent); }

  /* ── LAYOUT ── */
  .main { position: relative; z-index: 1; padding: 20px 24px; }
  
  /* Stats bar */
  .stats-bar {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
    margin-bottom: 20px;
  }
  .stat-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px; padding: 16px 20px;
    position: relative; overflow: hidden;
    transition: border-color 0.3s;
  }
  .stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  }
  .stat-card.critical::before { background: var(--red); }
  .stat-card.high::before { background: var(--orange); }
  .stat-card.zones::before { background: var(--accent); }
  .stat-card.pop::before { background: #8b5cf6; }
  .stat-label { font-size: 11px; color: var(--dim); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; font-family: var(--font-ui); }
  .stat-value { font-size: 32px; font-weight: 700; font-family: var(--font-ui); line-height: 1; }
  .stat-card.critical .stat-value { color: var(--red); }
  .stat-card.high .stat-value { color: var(--orange); }
  .stat-card.zones .stat-value { color: var(--accent); }
  .stat-card.pop .stat-value { color: #a78bfa; }
  .stat-sub { font-size: 12px; color: var(--dim); margin-top: 6px; }

  /* ── GRID ── */
  .grid { display: grid; grid-template-columns: 340px 1fr; gap: 16px; }
  
  /* Zone list */
  .panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
  }
  .panel-header {
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(0,0,0,0.2);
  }
  .panel-title {
    font-family: var(--font-ui); font-size: 14px; font-weight: 600;
    color: var(--accent); letter-spacing: 1px; text-transform: uppercase;
  }
  .refresh-btn {
    background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent); padding: 5px 12px; border-radius: 6px;
    font-size: 11px; font-family: var(--font-mono); cursor: pointer;
    transition: all 0.2s;
  }
  .refresh-btn:hover { background: rgba(0,212,255,0.2); }

  .zone-list { max-height: 600px; overflow-y: auto; }
  .zone-list::-webkit-scrollbar { width: 4px; }
  .zone-list::-webkit-scrollbar-track { background: transparent; }
  .zone-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  .zone-item {
    padding: 14px 18px;
    border-bottom: 1px solid rgba(26,58,92,0.5);
    cursor: pointer; transition: background 0.2s;
    display: flex; align-items: center; gap: 14px;
  }
  .zone-item:hover { background: rgba(0,212,255,0.05); }
  .zone-item.active { background: rgba(0,212,255,0.08); border-left: 3px solid var(--accent); }

  .risk-badge {
    width: 44px; height: 44px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-ui); font-size: 18px; font-weight: 700;
    flex-shrink: 0;
  }
  .zone-info { flex: 1; min-width: 0; }
  .zone-name { font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 4px; font-family: var(--font-ui); }
  .zone-meta { font-size: 11px; color: var(--dim); font-family: var(--font-mono); }
  .risk-score { 
    font-family: var(--font-mono); font-size: 20px; font-weight: 700;
    color: var(--text); text-align: right;
  }

  /* Detail panel */
  .detail-area { display: flex; flex-direction: column; gap: 14px; }
  
  .module-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  
  .module-card {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
  }
  .module-header {
    padding: 12px 16px;
    background: rgba(0,0,0,0.3);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 10px;
  }
  .module-icon { font-size: 18px; }
  .module-name { font-family: var(--font-ui); font-size: 13px; font-weight: 600; color: var(--accent); letter-spacing: 0.5px; }
  .module-body { padding: 14px 16px; }

  .score-bar-wrap { margin-bottom: 10px; }
  .score-label { font-size: 11px; color: var(--dim); margin-bottom: 5px; display: flex; justify-content: space-between; font-family: var(--font-mono); }
  .score-bar { height: 6px; background: rgba(255,255,255,0.07); border-radius: 3px; overflow: hidden; }
  .score-fill { height: 100%; border-radius: 3px; transition: width 0.8s ease; }

  .data-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .data-key { font-size: 12px; color: var(--dim); font-family: var(--font-mono); }
  .data-val { font-size: 13px; color: var(--text); font-family: var(--font-ui); font-weight: 600; }
  .tag { 
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 11px; font-family: var(--font-mono);
    background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3);
  }
  .tag.ok { background: rgba(34,197,94,0.15); color: #86efac; border-color: rgba(34,197,94,0.3); }
  .tag.warn { background: rgba(245,158,11,0.15); color: #fcd34d; border-color: rgba(245,158,11,0.3); }

  .signal-item {
    padding: 8px 10px; margin-bottom: 6px;
    background: rgba(0,0,0,0.3); border-radius: 8px;
    border-left: 3px solid var(--accent2);
    font-size: 12px; color: var(--text);
    font-family: var(--font-body);
  }
  .signal-meta { font-size: 10px; color: var(--dim); margin-top: 4px; font-family: var(--font-mono); }

  /* Fusion panel */
  .fusion-panel {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
  }
  .fusion-header {
    padding: 14px 20px;
    background: linear-gradient(90deg, rgba(0,0,0,0.4) 0%, rgba(0,212,255,0.05) 100%);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }
  .fusion-title { font-family: var(--font-ui); font-size: 15px; font-weight: 700; color: var(--accent); letter-spacing: 1px; }
  .fusion-body { padding: 20px; }
  .fusion-score-big {
    text-align: center; margin-bottom: 20px;
  }
  .big-score { font-size: 72px; font-weight: 700; font-family: var(--font-ui); line-height: 1; }
  .big-label { font-size: 16px; color: var(--dim); font-family: var(--font-mono); letter-spacing: 2px; margin-top: 6px; }
  
  .component-scores { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
  .comp-score {
    text-align: center; padding: 12px;
    background: rgba(0,0,0,0.3); border-radius: 8px;
    border: 1px solid var(--border);
  }
  .comp-val { font-size: 24px; font-weight: 700; font-family: var(--font-ui); }
  .comp-name { font-size: 10px; color: var(--dim); font-family: var(--font-mono); letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; }

  .actions-list { }
  .action-item {
    padding: 10px 14px; margin-bottom: 8px;
    background: rgba(255,107,53,0.07);
    border: 1px solid rgba(255,107,53,0.2);
    border-radius: 8px;
    font-size: 13px; color: var(--text);
    font-family: var(--font-body);
  }

  /* Sensor sparkline */
  .sparkline { display: flex; align-items: flex-end; gap: 2px; height: 30px; margin-top: 6px; }
  .spark-bar { flex: 1; border-radius: 2px 2px 0 0; transition: height 0.5s; min-height: 2px; }

  /* Loading state */
  .loading { 
    display: flex; align-items: center; justify-content: center; 
    height: 300px; color: var(--dim); font-family: var(--font-mono);
    gap: 10px;
  }
  .spinner { 
    width: 20px; height: 20px; border: 2px solid var(--border);
    border-top-color: var(--accent); border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Radar chart area */
  .radar-wrap { display: flex; justify-content: center; margin: 10px 0; }

  /* Tooltip */
  .tooltip { position: relative; }
  .tooltip:hover::after {
    content: attr(data-tip);
    position: absolute; bottom: 110%; left: 50%; transform: translateX(-50%);
    background: #1a2d42; color: var(--text); padding: 6px 10px; border-radius: 6px;
    font-size: 11px; white-space: nowrap; font-family: var(--font-mono);
    border: 1px solid var(--border); z-index: 100;
  }

  @media (max-width: 900px) {
    .grid { grid-template-columns: 1fr; }
    .module-grid { grid-template-columns: 1fr; }
    .stats-bar { grid-template-columns: repeat(2,1fr); }
  }
</style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-icon">🛰️</div>
    <div>
      <div class="logo-text">DISASTER<span style="color:var(--accent)">AI</span></div>
      <div class="logo-sub">Multimodal Response Intelligence System</div>
    </div>
  </div>
  <div class="header-right">
    <div class="live-badge"><div class="live-dot"></div> LIVE PROTOTYPE</div>
    <div class="clock" id="clock">--:--:--</div>
  </div>
</header>

<div class="main">
  <!-- Stats Bar -->
  <div class="stats-bar" id="statsBar">
    <div class="stat-card critical">
      <div class="stat-label">Critical Zones</div>
      <div class="stat-value" id="statCritical">—</div>
      <div class="stat-sub">Risk Level 4-5</div>
    </div>
    <div class="stat-card high">
      <div class="stat-label">Active Alerts</div>
      <div class="stat-value" id="statAlerts">—</div>
      <div class="stat-sub">Distress signals</div>
    </div>
    <div class="stat-card zones">
      <div class="stat-label">Zones Monitored</div>
      <div class="stat-value" id="statZones">—</div>
      <div class="stat-sub">Active scanning</div>
    </div>
    <div class="stat-card pop">
      <div class="stat-label">Population at Risk</div>
      <div class="stat-value" id="statPop">—</div>
      <div class="stat-sub">Est. affected</div>
    </div>
  </div>

  <div class="grid">
    <!-- Zone List -->
    <div class="panel">
      <div class="panel-header">
        <span class="panel-title">⚠ Zone Priority Queue</span>
        <button class="refresh-btn" onclick="refreshAll()">↻ REFRESH</button>
      </div>
      <div class="zone-list" id="zoneList">
        <div class="loading"><div class="spinner"></div> Analyzing zones...</div>
      </div>
    </div>

    <!-- Detail Panel -->
    <div class="detail-area" id="detailArea">
      <div class="panel" style="padding: 60px; text-align: center;">
        <div style="font-size: 40px; margin-bottom: 16px;">🛰️</div>
        <div style="font-family: var(--font-ui); font-size: 18px; color: var(--dim);">Select a zone to view full multimodal analysis</div>
      </div>
    </div>
  </div>
</div>

<script>
let currentZone = null;
let allZones = [];

// Clock
function updateClock() {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// Color helpers
function riskColor(score) {
  if (score >= 0.8) return '#ef4444';
  if (score >= 0.6) return '#f97316';
  if (score >= 0.4) return '#f59e0b';
  if (score >= 0.2) return '#84cc16';
  return '#22c55e';
}
function scoreColor(s) { return riskColor(s); }

// Load zone list
async function loadZones() {
  try {
    const res = await fetch('/api/zones');
    allZones = await res.json();
    renderZoneList(allZones);
    updateStats(allZones);
  } catch(e) {
    document.getElementById('zoneList').innerHTML = '<div class="loading">⚠ Error loading data</div>';
  }
}

function updateStats(zones) {
  const critical = zones.filter(z => z.risk_level >= 4).length;
  const alerts = zones.reduce((a,z) => a + z.signals, 0);
  const atRisk = zones.filter(z => z.risk_level >= 3).reduce((a,z) => a + z.population, 0);
  document.getElementById('statCritical').textContent = critical;
  document.getElementById('statAlerts').textContent = alerts;
  document.getElementById('statZones').textContent = zones.length;
  document.getElementById('statPop').textContent = atRisk.toLocaleString();
}

function renderZoneList(zones) {
  const html = zones.map((z, i) => `
    <div class="zone-item ${currentZone === z.id ? 'active' : ''}" onclick="selectZone(${z.id})">
      <div class="risk-badge" style="background:${z.risk_color}22; color:${z.risk_color}; border: 1px solid ${z.risk_color}55;">
        ${z.risk_level}
      </div>
      <div class="zone-info">
        <div class="zone-name">${z.name}</div>
        <div class="zone-meta">${z.risk_label} • ${z.signals} signals • ${z.sensor_anomalies} anomalies</div>
      </div>
      <div class="risk-score" style="color:${z.risk_color}">${(z.risk_score*100).toFixed(0)}<span style="font-size:12px;color:var(--dim)">%</span></div>
    </div>
  `).join('');
  document.getElementById('zoneList').innerHTML = html;
}

async function selectZone(id) {
  currentZone = id;
  renderZoneList(allZones);
  document.getElementById('detailArea').innerHTML = '<div class="panel"><div class="loading"><div class="spinner"></div> Running multimodal analysis...</div></div>';
  
  try {
    const res = await fetch(`/api/zone/${id}`);
    const data = await res.json();
    renderDetail(data);
  } catch(e) {
    document.getElementById('detailArea').innerHTML = '<div class="panel"><div class="loading">⚠ Analysis failed</div></div>';
  }
}

function renderDetail(d) {
  const f = d.fusion;
  const v = d.visual;
  const nlp = d.nlp;
  const s = d.sensor;
  const a = d.audio;
  const z = d.zone;

  // Sensor sparklines
  const sensorHTML = s.sensors.map(sensor => {
    const maxVal = Math.max(...sensor.readings, 0.01);
    const bars = sensor.readings.map(r => {
      const h = Math.max(4, Math.round((r / maxVal) * 28));
      const col = sensor.anomaly_detected ? '#f97316' : '#22c55e';
      return `<div class="spark-bar" style="height:${h}px;background:${col}44;"></div>`;
    }).join('');
    return `
      <div class="score-bar-wrap">
        <div class="score-label">
          <span>${sensor.type}</span>
          <span class="tag ${sensor.anomaly_detected ? '' : 'ok'}">${sensor.status}</span>
        </div>
        <div class="sparkline">${bars}</div>
      </div>`;
  }).join('');

  // Signals
  const sigHTML = nlp.signals.slice(0,3).map(sig => `
    <div class="signal-item">
      ${sig.text.substring(0,90)}${sig.text.length>90?'...':''}
      <div class="signal-meta">
        📡 ${sig.source} &nbsp;|&nbsp; 🏷 ${sig.category} &nbsp;|&nbsp; 
        🔥 Urgency ${sig.urgency_level}/5 &nbsp;|&nbsp; ${new Date(sig.timestamp).toLocaleTimeString()}
      </div>
    </div>`).join('');

  // Prob bars for visual
  const probHTML = Object.entries(v.probabilities).map(([label, prob]) => `
    <div class="score-bar-wrap">
      <div class="score-label"><span>${label}</span><span>${(prob*100).toFixed(1)}%</span></div>
      <div class="score-bar"><div class="score-fill" style="width:${prob*100}%;background:${riskColor(prob)};"></div></div>
    </div>`).join('');

  // Component score colors
  const cs = f.component_scores;

  document.getElementById('detailArea').innerHTML = `
    <!-- Fusion Summary -->
    <div class="fusion-panel">
      <div class="fusion-header">
        <span class="fusion-title">⚡ FUSION ENGINE — ${z.name}</span>
        <span style="font-family:var(--font-mono);font-size:12px;color:var(--dim)">Pop: ${z.pop.toLocaleString()} | Updated: ${new Date(f.last_updated).toLocaleTimeString()}</span>
      </div>
      <div class="fusion-body">
        <div style="display:grid;grid-template-columns:auto 1fr;gap:30px;align-items:center">
          <div class="fusion-score-big">
            <div class="big-score" style="color:${f.risk_color}">${(f.fused_risk_score*100).toFixed(1)}</div>
            <div class="big-label">${f.risk_label} Risk</div>
          </div>
          <div>
            <div class="component-scores">
              <div class="comp-score"><div class="comp-val" style="color:${scoreColor(cs.visual)}">${(cs.visual*100).toFixed(0)}</div><div class="comp-name">Visual</div></div>
              <div class="comp-score"><div class="comp-val" style="color:${scoreColor(cs.nlp)}">${(cs.nlp*100).toFixed(0)}</div><div class="comp-name">NLP</div></div>
              <div class="comp-score"><div class="comp-val" style="color:${scoreColor(cs.sensor)}">${(cs.sensor*100).toFixed(0)}</div><div class="comp-name">Sensor</div></div>
              <div class="comp-score"><div class="comp-val" style="color:${scoreColor(cs.audio)}">${(cs.audio*100).toFixed(0)}</div><div class="comp-name">Audio</div></div>
            </div>
            <div class="actions-list">
              ${f.recommended_actions.map(a => `<div class="action-item">${a}</div>`).join('')}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Module Grid -->
    <div class="module-grid">
      <!-- Visual Module -->
      <div class="module-card">
        <div class="module-header"><span class="module-icon">🛰</span><span class="module-name">Visual Damage Assessment</span></div>
        <div class="module-body">
          <div class="data-row">
            <span class="data-key">Classification</span>
            <span class="data-val" style="color:${riskColor(v.damage_class/3)}">${v.damage_label}</span>
          </div>
          <div class="data-row">
            <span class="data-key">Confidence</span>
            <span class="data-val">${(v.confidence*100).toFixed(1)}%</span>
          </div>
          <div class="data-row">
            <span class="data-key">Source</span>
            <span class="data-val" style="font-size:11px;color:var(--dim)">${v.source}</span>
          </div>
          <div style="margin-top:12px">${probHTML}</div>
        </div>
      </div>

      <!-- NLP Module -->
      <div class="module-card">
        <div class="module-header"><span class="module-icon">📡</span><span class="module-name">NLP Distress Signals</span></div>
        <div class="module-body">
          <div class="data-row">
            <span class="data-key">Signals Detected</span>
            <span class="data-val" style="color:var(--accent)">${nlp.signals_detected}</span>
          </div>
          <div class="data-row">
            <span class="data-key">Max Urgency</span>
            <span class="data-val" style="color:${riskColor(nlp.max_urgency)}">${(nlp.max_urgency*100).toFixed(0)}%</span>
          </div>
          <div style="margin-top:12px">${sigHTML}</div>
        </div>
      </div>

      <!-- Sensor Module -->
      <div class="module-card">
        <div class="module-header"><span class="module-icon">📊</span><span class="module-name">Sensor Anomaly Detector</span></div>
        <div class="module-body">
          <div class="data-row">
            <span class="data-key">Anomalies Found</span>
            <span class="data-val" style="color:${s.anomalies_detected>0?'var(--orange)':'var(--green)'}">${s.anomalies_detected} / ${s.sensors.length}</span>
          </div>
          <div style="margin-top:12px">${sensorHTML}</div>
        </div>
      </div>

      <!-- Audio Module -->
      <div class="module-card">
        <div class="module-header"><span class="module-icon">🎙</span><span class="module-name">Audio Classifier</span></div>
        <div class="module-body">
          <div class="data-row">
            <span class="data-key">Top Event</span>
            <span class="data-val" style="color:${riskColor(a.top_severity)};font-size:12px">${a.top_event}</span>
          </div>
          <div class="data-row">
            <span class="data-key">Severity</span>
            <span class="data-val">${(a.top_severity*100).toFixed(0)}%</span>
          </div>
          <div class="data-row">
            <span class="data-key">Source</span>
            <span class="data-val" style="font-size:11px;color:var(--dim)">${a.source}</span>
          </div>
          ${a.speech_detected ? `
          <div style="margin-top:12px; padding:10px; background:rgba(0,0,0,0.3); border-radius:8px; border-left:3px solid var(--accent)">
            <div style="font-size:10px;color:var(--dim);margin-bottom:6px;font-family:var(--font-mono)">TRANSCRIPT</div>
            <div style="font-size:12px;font-style:italic;">"${a.transcript}"</div>
          </div>` : '<div style="color:var(--dim);font-size:12px;margin-top:10px;font-family:var(--font-mono)">No speech detected</div>'}
          <div style="margin-top:12px">
            ${a.events_detected.map(e => `
              <div class="data-row">
                <span class="data-key" style="font-size:11px">${e.event}</span>
                <div class="score-bar" style="width:80px"><div class="score-fill" style="width:${e.severity*100}%;background:${riskColor(e.severity)};"></div></div>
              </div>`).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
}

function refreshAll() {
  loadZones();
  if (currentZone) selectZone(currentZone);
}

// Auto-refresh every 30 seconds
setInterval(refreshAll, 30000);

// Initial load
loadZones();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────
#  HTTP SERVER
# ─────────────────────────────────────────────
class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logs
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self._send(200, 'text/html', HTML_PAGE.encode())
            
        elif path == '/api/zones':
            data = get_all_zones_summary()
            self._send(200, 'application/json', json.dumps(data).encode())
            
        elif path.startswith('/api/zone/'):
            try:
                zone_id = int(path.split('/')[-1])
                zone = next((z for z in DISASTER_ZONES if z['id'] == zone_id), None)
                if zone:
                    result = analyze_zone(zone)
                    self._send(200, 'application/json', json.dumps(result).encode())
                else:
                    self._send(404, 'application/json', b'{"error":"Zone not found"}')
            except ValueError:
                self._send(400, 'application/json', b'{"error":"Invalid zone id"}')
        else:
            self._send(404, 'text/plain', b'Not found')
    
    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == '__main__':
    PORT = 5000
    server = HTTPServer(('localhost', PORT), RequestHandler)
    
    print("\n" + "="*55)
    print("  🛰️  DISASTER AI — MULTIMODAL RESPONSE SYSTEM")
    print("="*55)
    print(f"\n  ✅  Server running at: http://localhost:{PORT}")
    print(f"  📡  {len(DISASTER_ZONES)} disaster zones loaded")
    print(f"  🧠  4 AI modules active: Visual | NLP | Sensor | Audio")
    print(f"  ⚡  Fusion engine: online")
    print(f"\n  Press Ctrl+C to stop\n")
    print("="*55 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  🔴  Server stopped.\n")