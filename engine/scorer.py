#!/usr/bin/env python3
"""
OrionMaturity Scoring Engine
-----------------------------
Computes weighted maturity scores for NIST CSF 2.0, CIS Controls v8,
and ISO/IEC 27001:2022. Accepts JSON input, produces structured results
for report generation.

Usage:
    python scorer.py --framework nist_csf --json examples/sample_nist.json
    python scorer.py --framework cis_v8   --json examples/sample_cis.json
    python scorer.py --framework iso_27001 --json examples/sample_iso.json
    python scorer.py --all --json examples/sample_all.json --output examples/outputs/
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from frameworks import nist_csf, cis_controls, iso_27001


# ── Maturity scale ────────────────────────────────────────────────────────────

MATURITY_LEVELS = [
    (1.0, 1.9, "Initial",    "Ad-hoc, undocumented, reactive. No formal process exists."),
    (2.0, 2.9, "Developing", "Some documentation, inconsistently applied."),
    (3.0, 3.9, "Defined",    "Documented, standardized processes deployed org-wide."),
    (4.0, 4.9, "Managed",    "Measured, monitored with KPIs. Metrics-driven management."),
    (5.0, 5.0, "Optimizing", "Continuously improving, automated, predictive capabilities."),
]

def maturity_label(score: float) -> tuple:
    for low, high, name, desc in MATURITY_LEVELS:
        if low <= score <= high + 0.05:
            return name, desc
    return "Optimizing", MATURITY_LEVELS[-1][3]

def score_bar(score: float, width: int = 20) -> str:
    filled = int((score / 5.0) * width)
    return "█" * filled + "░" * (width - filled)


# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class SubdomainResult:
    key: str
    label: str
    score: float
    target: float
    gap: float
    maturity_name: str

@dataclass
class DomainResult:
    key: str
    label: str
    weighted_score: float
    target_score: float
    gap: float
    maturity_name: str
    subdomains: list = field(default_factory=list)

@dataclass
class FrameworkResult:
    framework_id: str
    framework_name: str
    org: str
    assessor: str
    date: str
    overall_score: float
    maturity_name: str
    maturity_desc: str
    domains: list = field(default_factory=list)
    gaps: list = field(default_factory=list)


# ── NIST CSF 2.0 scorer ───────────────────────────────────────────────────────

def score_nist_csf(data: dict, org: str, assessor: str) -> FrameworkResult:
    scores = data.get("scores", {})
    domains = []
    overall = 0.0

    for fn_key, fn_def in nist_csf.FUNCTIONS.items():
        fn_scores = scores.get(fn_key, {})
        fn_targets = nist_csf.TARGET_SCORES.get(fn_key, {})
        subdomains = []
        fn_weighted = 0.0

        for sd_key, sd_def in fn_def["subdomains"].items():
            raw = float(fn_scores.get(sd_key, 1.0))
            raw = max(1.0, min(5.0, raw))
            target = fn_targets.get(sd_key, 4.0)
            gap = target - raw
            name, _ = maturity_label(raw)
            subdomains.append(SubdomainResult(sd_key, sd_def["label"], raw, target, gap, name))
            fn_weighted += raw * sd_def["weight"]

        target_fn = sum(fn_targets.get(k, 4.0) * v["weight"]
                        for k, v in fn_def["subdomains"].items())
        name, _ = maturity_label(fn_weighted)
        domains.append(DomainResult(fn_key, fn_def["label"], fn_weighted,
                                    target_fn, target_fn - fn_weighted, name, subdomains))
        overall += fn_weighted * fn_def["weight"]

    name, desc = maturity_label(overall)
    gaps = sorted([sd for d in domains for sd in d.subdomains if sd.gap > 0.5],
                  key=lambda x: x.gap, reverse=True)

    return FrameworkResult(nist_csf.FRAMEWORK_ID, nist_csf.FRAMEWORK_NAME,
                           org, assessor, datetime.now().strftime("%Y-%m-%d"),
                           round(overall, 2), name, desc, domains, gaps)


# ── CIS Controls v8 scorer ────────────────────────────────────────────────────

def score_cis_v8(data: dict, org: str, assessor: str) -> FrameworkResult:
    scores = data.get("scores", {})
    controls = []
    overall = 0.0

    for ctrl_key, ctrl_def in cis_controls.CONTROLS.items():
        raw = float(scores.get(ctrl_key, 1.0))
        raw = max(1.0, min(5.0, raw))
        target = cis_controls.TARGET_SCORES.get(ctrl_key, 4.0)
        gap = target - raw
        name, _ = maturity_label(raw)
        controls.append(SubdomainResult(ctrl_key, ctrl_def["label"], raw, target, gap, name))
        overall += raw * ctrl_def["weight"]

    name, desc = maturity_label(overall)

    # Group controls by IG for domain display
    ig_groups = {}
    for c in controls:
        ig = cis_controls.CONTROLS[c.key]["ig"]
        ig_groups.setdefault(ig, []).append(c)

    domains = []
    for ig_num in sorted(ig_groups):
        items = ig_groups[ig_num]
        avg = sum(i.score for i in items) / len(items)
        tgt = sum(i.target for i in items) / len(items)
        lname, _ = maturity_label(avg)
        domains.append(DomainResult(f"IG{ig_num}", cis_controls.IG_LABELS[ig_num],
                                    round(avg, 2), round(tgt, 2), round(tgt - avg, 2),
                                    lname, items))

    gaps = sorted([c for c in controls if c.gap > 0.5], key=lambda x: x.gap, reverse=True)

    return FrameworkResult(cis_controls.FRAMEWORK_ID, cis_controls.FRAMEWORK_NAME,
                           org, assessor, datetime.now().strftime("%Y-%m-%d"),
                           round(overall, 2), name, desc, domains, gaps)


# ── ISO 27001 scorer ──────────────────────────────────────────────────────────

def score_iso_27001(data: dict, org: str, assessor: str) -> FrameworkResult:
    scores = data.get("scores", {})
    clause_scores_raw = data.get("clause_scores", {})
    domains = []
    annex_overall = 0.0
    annex_weight_sum = 0.0

    for theme_key, theme_def in iso_27001.ANNEX_A.items():
        theme_scores = scores.get(theme_key, {})
        theme_targets = iso_27001.TARGET_SCORES.get(theme_key, {})
        subdomains = []
        theme_weighted = 0.0

        for sd_key, sd_def in theme_def["subdomains"].items():
            raw = float(theme_scores.get(sd_key, 1.0))
            raw = max(1.0, min(5.0, raw))
            target = theme_targets.get(sd_key, 4.0)
            gap = target - raw
            name, _ = maturity_label(raw)
            subdomains.append(SubdomainResult(sd_key, sd_def["label"], raw, target, gap, name))
            theme_weighted += raw * sd_def["weight"]

        target_theme = sum(theme_targets.get(k, 4.0) * v["weight"]
                           for k, v in theme_def["subdomains"].items())
        name, _ = maturity_label(theme_weighted)
        domains.append(DomainResult(theme_key, theme_def["label"], round(theme_weighted, 2),
                                    round(target_theme, 2), round(target_theme - theme_weighted, 2),
                                    name, subdomains))
        annex_overall += theme_weighted * theme_def["weight"]
        annex_weight_sum += theme_def["weight"]

    # Clause scores
    clause_results = []
    clause_overall = 0.0
    for c_key, c_def in iso_27001.CLAUSES.items():
        raw = float(clause_scores_raw.get(c_key, 1.0))
        raw = max(1.0, min(5.0, raw))
        target = iso_27001.CLAUSE_TARGETS.get(c_key, 4.0)
        gap = target - raw
        name, _ = maturity_label(raw)
        clause_results.append(SubdomainResult(c_key, c_def["label"], raw, target, gap, name))
        clause_overall += raw * c_def["weight"]

    clause_name, _ = maturity_label(clause_overall)
    domains.append(DomainResult("CLAUSES", "Management System Clauses (4–10)",
                                round(clause_overall, 2), 4.0,
                                round(4.0 - clause_overall, 2), clause_name, clause_results))

    overall = (annex_overall * 0.70) + (clause_overall * 0.30)
    name, desc = maturity_label(overall)
    gaps = sorted([sd for d in domains for sd in d.subdomains if sd.gap > 0.5],
                  key=lambda x: x.gap, reverse=True)

    return FrameworkResult(iso_27001.FRAMEWORK_ID, iso_27001.FRAMEWORK_NAME,
                           org, assessor, datetime.now().strftime("%Y-%m-%d"),
                           round(overall, 2), name, desc, domains, gaps)


# ── Entry point ───────────────────────────────────────────────────────────────

SCORERS = {
    "nist_csf":  score_nist_csf,
    "cis_v8":    score_cis_v8,
    "iso_27001": score_iso_27001,
}

def main():
    parser = argparse.ArgumentParser(description="OrionMaturity Scoring Engine")
    parser.add_argument("--framework", choices=list(SCORERS.keys()),
                        help="Framework to score")
    parser.add_argument("--all", action="store_true", help="Score all frameworks from one input file")
    parser.add_argument("--json", required=True, metavar="FILE", help="Input JSON file")
    parser.add_argument("--output", metavar="DIR", help="Output directory for reports")
    parser.add_argument("--org", default="", help="Organization name")
    parser.add_argument("--assessor", default="", help="Assessor name")
    args = parser.parse_args()

    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    org = args.org or data.get("org", "Unknown Organization")
    assessor = args.assessor or data.get("assessor", "Unknown Assessor")

    from report import generate_report
    import os

    frameworks_to_run = list(SCORERS.keys()) if args.all else [args.framework]

    for fw in frameworks_to_run:
        fw_data = data.get(fw, data) if args.all else data
        result = SCORERS[fw](fw_data, org, assessor)
        report = generate_report(result)

        if args.output:
            os.makedirs(args.output, exist_ok=True)
            path = os.path.join(args.output, f"{fw}_report.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report written to {path}")
        else:
            print(report)

if __name__ == "__main__":
    main()
