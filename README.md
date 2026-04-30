# OrionMaturity — Security Program Maturity Scoring Engine

> Automated, quantitative maturity scoring for NIST CSF 2.0, CIS Controls v8, and ISO/IEC 27001:2022. Built to replace manual, interview-based assessments with data-driven, reproducible results.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Frameworks](https://img.shields.io/badge/Frameworks-NIST%20CSF%202.0%20%7C%20CIS%20v8%20%7C%20ISO%2027001-green)]()

---

## The Problem with Current Maturity Assessments

| Problem | Impact |
|---------|--------|
| Too manual — relies on interviews and spreadsheets | 4–12 weeks per cycle |
| Subjective — results vary widely across assessors | Scores are not comparable |
| Static — not tied to real-time telemetry or configs | Stale the day after delivery |
| Disconnected — ignores actual technical configurations | Compliance theater, not security |
| Expensive — out of reach for mid-sized organizations | Only large orgs can afford it |

OrionMaturity addresses all five by replacing opinion with measurement.

---

## What This Does

Produces **quantitative, weighted maturity scores** across three industry frameworks:

- **NIST CSF 2.0** — 6 functions, 16 sub-domains, weighted by risk contribution
- **CIS Controls v8** — 18 controls across 3 Implementation Groups
- **ISO/IEC 27001:2022** — 4 Annex A control themes + 7 management system clauses

For each framework it produces:
- Overall maturity score (1.0–5.0, CMM-aligned)
- Domain-level scores with progress bars
- Prioritized gap analysis (largest gaps from target, ranked)
- Remediation guidance per gap

---

## Quick Start

### Option A — Interactive Dashboard (recommended)

```bash
git clone https://github.com/rafatyazdani/maturity-scoring-engine.git
cd maturity-scoring-engine

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
# source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
python -m streamlit run app.py
```

Opens at `http://localhost:8501`. Select a framework, adjust scores with sliders, and download a full markdown report.

### Option B — Command Line

```bash
cd maturity-scoring-engine/engine

# Score all three frameworks from one input file
python scorer.py --all --json ../examples/sample_all.json --output ../examples/outputs/

# Score a single framework
python scorer.py --framework nist_csf  --json ../examples/sample_all.json
python scorer.py --framework cis_v8    --json ../examples/sample_all.json
python scorer.py --framework iso_27001 --json ../examples/sample_all.json
```

The CLI requires no dependencies beyond Python 3.9+ standard library. The dashboard requires `streamlit`, `matplotlib`, `pandas`, and `numpy` (see `requirements.txt`).

---

## Sample Output

See [`examples/outputs/`](examples/outputs/) for pre-generated reports:

- [`nist_csf_report.md`](examples/outputs/nist_csf_report.md) — NIST CSF 2.0 assessment
- [`cis_v8_report.md`](examples/outputs/cis_v8_report.md) — CIS Controls v8 assessment
- [`iso_27001_report.md`](examples/outputs/iso_27001_report.md) — ISO 27001 assessment

---

## Input Format

Scores are provided as JSON, one value per sub-domain (1.0–5.0):

```json
{
  "org": "Acme Corporation",
  "assessor": "Jane Smith, CISSP",
  "nist_csf": {
    "scores": {
      "GOVERN":  { "policy_governance": 2.5, "risk_management": 2.0, "supply_chain_risk": 1.5 },
      "PROTECT": { "identity_access": 3.5, "data_security": 2.5 }
    }
  },
  "cis_v8": {
    "scores": { "CIS01": 2.5, "CIS05": 2.0, "CIS07": 2.5 }
  }
}
```

See [`examples/sample_all.json`](examples/sample_all.json) for a complete example.

---

## Maturity Scale

| Level | Score | Description |
|-------|-------|-------------|
| Initial | 1.0–1.9 | Ad-hoc, reactive, undocumented |
| Developing | 2.0–2.9 | Inconsistently applied |
| Defined | 3.0–3.9 | Standardized and documented |
| Managed | 4.0–4.9 | Measured, KPI-driven |
| Optimizing | 5.0 | Automated, continuous improvement |

Full scoring guidance: [MATURITY-SCALE.md](MATURITY-SCALE.md)

---

## Repository Structure

```
maturity-scoring-engine/
├── engine/
│   ├── scorer.py                  # Scoring engine + CLI entry point
│   ├── report.py                  # Markdown report generator
│   └── frameworks/
│       ├── nist_csf.py            # NIST CSF 2.0 domain/weight definitions
│       ├── cis_controls.py        # CIS Controls v8 definitions
│       └── iso_27001.py           # ISO 27001:2022 definitions
├── examples/
│   ├── sample_all.json            # Sample input (all three frameworks)
│   └── outputs/                   # Pre-generated sample reports
├── rubrics/                       # Scoring rubrics per framework
├── architecture/
│   └── architecture.md            # System design + Mermaid diagrams
├── MATURITY-SCALE.md              # CMM-aligned scale definition and guidance
└── README.md
```

---

## Framework Documentation

- [NIST CSF 2.0 Scoring Rubric](rubrics/nist-csf-rubric.md)
- [CIS Controls v8 Scoring Rubric](rubrics/cis-controls-rubric.md)
- [ISO 27001:2022 Scoring Rubric](rubrics/iso-27001-rubric.md)
- [Architecture & Design](architecture/architecture.md)

---

## Strategic Context

This engine is designed to address the **GRC ↔ Quantification gap** — the disconnect between qualitative maturity assessments and the financial risk models that boards and CFOs actually use.

Output scores feed directly into the [CRQ-F Framework](https://github.com/rafatyazdani/cyber-risk-quantification) for financial risk modeling: a Defined (3.0) posture vs. a Managed (4.0) posture translates directly into different ALE estimates, control ROI calculations, and cyber insurance premiums.

---

## License

Apache 2.0 — free to use, adapt, and deploy in commercial contexts with attribution.

---

*Built by a CISSP + CPA with 10+ years in GRC and cybersecurity strategy.*
