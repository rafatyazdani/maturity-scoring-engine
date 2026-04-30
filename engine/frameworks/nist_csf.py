"""
NIST Cybersecurity Framework 2.0 — Scorecard Definition

Six functions, each with weighted sub-domains.
Scores are 1.0–5.0 (CMM-aligned, see MATURITY-SCALE.md).
"""

FRAMEWORK_ID = "nist_csf_2"
FRAMEWORK_NAME = "NIST Cybersecurity Framework 2.0"

# Each function has a weight (must sum to 1.0) and sub-domains.
# Each sub-domain has a weight within its function (must sum to 1.0).

FUNCTIONS = {
    "GOVERN": {
        "label": "Govern",
        "weight": 0.20,
        "description": "Organizational context, risk strategy, supply chain, and oversight.",
        "subdomains": {
            "policy_governance":    {"label": "Policy & Governance",    "weight": 0.40},
            "risk_management":      {"label": "Risk Management Strategy","weight": 0.35},
            "supply_chain_risk":    {"label": "Supply Chain Risk",       "weight": 0.25},
        },
    },
    "IDENTIFY": {
        "label": "Identify",
        "weight": 0.15,
        "description": "Asset management, business context, and risk assessment.",
        "subdomains": {
            "asset_management":     {"label": "Asset Management",        "weight": 0.35},
            "business_environment": {"label": "Business Environment",    "weight": 0.25},
            "risk_assessment":      {"label": "Risk Assessment",         "weight": 0.40},
        },
    },
    "PROTECT": {
        "label": "Protect",
        "weight": 0.25,
        "description": "Safeguards to limit the impact of cybersecurity events.",
        "subdomains": {
            "identity_access":      {"label": "Identity & Access Mgmt",  "weight": 0.30},
            "awareness_training":   {"label": "Awareness & Training",    "weight": 0.20},
            "data_security":        {"label": "Data Security",           "weight": 0.25},
            "platform_security":    {"label": "Platform Security",       "weight": 0.25},
        },
    },
    "DETECT": {
        "label": "Detect",
        "weight": 0.15,
        "description": "Timely discovery of cybersecurity events.",
        "subdomains": {
            "anomalies_events":     {"label": "Anomalies & Events",      "weight": 0.50},
            "security_monitoring":  {"label": "Security Monitoring",     "weight": 0.50},
        },
    },
    "RESPOND": {
        "label": "Respond",
        "weight": 0.15,
        "description": "Actions taken regarding a detected cybersecurity incident.",
        "subdomains": {
            "incident_management":  {"label": "Incident Management",     "weight": 0.50},
            "incident_analysis":    {"label": "Incident Analysis",       "weight": 0.50},
        },
    },
    "RECOVER": {
        "label": "Recover",
        "weight": 0.10,
        "description": "Resilience and restoration of capabilities after an incident.",
        "subdomains": {
            "recovery_planning":    {"label": "Recovery Planning",       "weight": 0.60},
            "improvements":         {"label": "Improvements",            "weight": 0.40},
        },
    },
}

# Target scores by sub-domain — what "good" looks like for most organizations
TARGET_SCORES = {
    "GOVERN":   {"policy_governance": 4.0, "risk_management": 4.0, "supply_chain_risk": 3.5},
    "IDENTIFY": {"asset_management": 4.0, "business_environment": 3.5, "risk_assessment": 4.0},
    "PROTECT":  {"identity_access": 4.5, "awareness_training": 3.5, "data_security": 4.0, "platform_security": 4.0},
    "DETECT":   {"anomalies_events": 4.0, "security_monitoring": 4.0},
    "RESPOND":  {"incident_management": 4.0, "incident_analysis": 3.5},
    "RECOVER":  {"recovery_planning": 3.5, "improvements": 3.5},
}
