"""
ISO/IEC 27001:2022 — Scorecard Definition

Covers the 4 control themes from Annex A (93 controls)
grouped into assessable domains, plus the 7 management
system clauses (4–10).
Scores are 1.0–5.0 (CMM-aligned, see MATURITY-SCALE.md).
"""

FRAMEWORK_ID = "iso_27001"
FRAMEWORK_NAME = "ISO/IEC 27001:2022"

# Annex A control themes
ANNEX_A = {
    "A5_org": {
        "label": "A.5 Organizational Controls",
        "weight": 0.30,
        "description": "Policies, roles, responsibilities, threat intelligence, supplier relationships.",
        "subdomains": {
            "policies":         {"label": "Information Security Policies",    "weight": 0.20},
            "roles":            {"label": "Roles & Responsibilities",         "weight": 0.20},
            "threat_intel":     {"label": "Threat Intelligence",              "weight": 0.20},
            "supplier_mgmt":    {"label": "Supplier & Cloud Security",        "weight": 0.20},
            "incident_mgmt":    {"label": "Incident Management",              "weight": 0.20},
        },
    },
    "A6_people": {
        "label": "A.6 People Controls",
        "weight": 0.15,
        "description": "Screening, terms of employment, awareness, disciplinary process.",
        "subdomains": {
            "screening":        {"label": "Screening",                        "weight": 0.30},
            "awareness":        {"label": "Security Awareness & Training",    "weight": 0.40},
            "remote_working":   {"label": "Remote Working",                   "weight": 0.30},
        },
    },
    "A7_physical": {
        "label": "A.7 Physical Controls",
        "weight": 0.10,
        "description": "Physical security perimeters, access, equipment protection.",
        "subdomains": {
            "perimeter":        {"label": "Physical Security Perimeters",     "weight": 0.40},
            "equipment":        {"label": "Equipment Security",               "weight": 0.35},
            "clear_desk":       {"label": "Clear Desk & Screen",              "weight": 0.25},
        },
    },
    "A8_tech": {
        "label": "A.8 Technological Controls",
        "weight": 0.45,
        "description": "Endpoint, IAM, crypto, logging, vulnerability, network, SDLC.",
        "subdomains": {
            "endpoint":         {"label": "Endpoint & Device Security",       "weight": 0.15},
            "iam":              {"label": "Identity & Access Management",     "weight": 0.20},
            "crypto":           {"label": "Cryptography & Key Management",    "weight": 0.10},
            "logging":          {"label": "Logging & Monitoring",             "weight": 0.15},
            "vuln_mgmt":        {"label": "Vulnerability Management",         "weight": 0.15},
            "network":          {"label": "Network Security",                 "weight": 0.15},
            "sdlc":             {"label": "Secure Development",               "weight": 0.10},
        },
    },
}

# Management system clauses (4–10)
CLAUSES = {
    "C4":  {"label": "Clause 4 — Context of the Organization", "weight": 0.10},
    "C5":  {"label": "Clause 5 — Leadership",                  "weight": 0.15},
    "C6":  {"label": "Clause 6 — Planning",                    "weight": 0.15},
    "C7":  {"label": "Clause 7 — Support",                     "weight": 0.15},
    "C8":  {"label": "Clause 8 — Operation",                   "weight": 0.20},
    "C9":  {"label": "Clause 9 — Performance Evaluation",      "weight": 0.15},
    "C10": {"label": "Clause 10 — Improvement",                "weight": 0.10},
}

TARGET_SCORES = {
    "A5_org":    {"policies": 4.0, "roles": 4.0, "threat_intel": 3.5, "supplier_mgmt": 3.5, "incident_mgmt": 4.0},
    "A6_people": {"screening": 3.5, "awareness": 4.0, "remote_working": 3.5},
    "A7_physical":{"perimeter": 3.5, "equipment": 3.5, "clear_desk": 3.0},
    "A8_tech":   {"endpoint": 4.0, "iam": 4.5, "crypto": 3.5, "logging": 4.0,
                  "vuln_mgmt": 4.0, "network": 4.0, "sdlc": 3.5},
}

CLAUSE_TARGETS = {k: 4.0 for k in CLAUSES}
