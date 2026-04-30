"""
CIS Controls v8 — Scorecard Definition

18 controls grouped into 3 Implementation Groups (IG).
IG1 = essential hygiene, IG2 = intermediate, IG3 = advanced.
Scores are 1.0–5.0 (CMM-aligned, see MATURITY-SCALE.md).
"""

FRAMEWORK_ID = "cis_v8"
FRAMEWORK_NAME = "CIS Controls v8"

CONTROLS = {
    "CIS01": {"label": "Inventory & Control of Enterprise Assets",  "ig": 1, "weight": 0.07},
    "CIS02": {"label": "Inventory & Control of Software Assets",    "ig": 1, "weight": 0.06},
    "CIS03": {"label": "Data Protection",                           "ig": 1, "weight": 0.07},
    "CIS04": {"label": "Secure Configuration of Assets",            "ig": 1, "weight": 0.06},
    "CIS05": {"label": "Account Management",                        "ig": 1, "weight": 0.07},
    "CIS06": {"label": "Access Control Management",                 "ig": 1, "weight": 0.06},
    "CIS07": {"label": "Continuous Vulnerability Management",       "ig": 1, "weight": 0.06},
    "CIS08": {"label": "Audit Log Management",                      "ig": 1, "weight": 0.05},
    "CIS09": {"label": "Email & Web Browser Protections",           "ig": 1, "weight": 0.04},
    "CIS10": {"label": "Malware Defenses",                          "ig": 1, "weight": 0.05},
    "CIS11": {"label": "Data Recovery",                             "ig": 2, "weight": 0.05},
    "CIS12": {"label": "Network Infrastructure Management",         "ig": 2, "weight": 0.05},
    "CIS13": {"label": "Network Monitoring & Defense",              "ig": 2, "weight": 0.06},
    "CIS14": {"label": "Security Awareness & Skills Training",      "ig": 1, "weight": 0.04},
    "CIS15": {"label": "Service Provider Management",               "ig": 2, "weight": 0.04},
    "CIS16": {"label": "Application Software Security",             "ig": 2, "weight": 0.05},
    "CIS17": {"label": "Incident Response Management",              "ig": 1, "weight": 0.06},
    "CIS18": {"label": "Penetration Testing",                       "ig": 3, "weight": 0.06},
}

# Group labels for reporting
IG_LABELS = {
    1: "IG1 — Basic Cyber Hygiene",
    2: "IG2 — Intermediate",
    3: "IG3 — Advanced",
}

TARGET_SCORES = {k: 4.0 if v["ig"] == 1 else 3.5 if v["ig"] == 2 else 3.0
                 for k, v in CONTROLS.items()}
