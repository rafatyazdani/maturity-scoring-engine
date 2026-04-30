# Maturity Scale — CMM-Aligned 1–5

All three frameworks use the same underlying maturity scale, enabling cross-framework comparison and consistent scoring.

---

## Scale Definition

| Level | Name | Score Range | Description |
|-------|------|-------------|-------------|
| 1 | **Initial** | 1.0 – 1.9 | Ad-hoc, undocumented, reactive. No formal process exists. Controls are applied inconsistently or not at all. |
| 2 | **Developing** | 2.0 – 2.9 | Some documentation exists, inconsistently applied. Processes depend on individual effort, not institutional practice. |
| 3 | **Defined** | 3.0 – 3.9 | Documented, standardized processes deployed organization-wide. Repeatable outcomes regardless of who executes. |
| 4 | **Managed** | 4.0 – 4.9 | Measured and monitored with KPIs. Metrics-driven management. Deviations are detected and corrected. |
| 5 | **Optimizing** | 5.0 | Continuously improving, automated, predictive capabilities. Industry-leading practice. |

---

## Scoring Guidance

### How to assign a score

**Score 1.0 — Initial**
- No policy or process exists
- Controls applied only when an incident forces it
- No ownership assigned

**Score 2.0 — Developing**
- Policy exists but is not enforced
- Some staff follow the process; most don't
- Manual, ad-hoc execution
- No metrics tracked

**Score 3.0 — Defined**
- Policy is documented, approved, and communicated
- Process is followed consistently across the org
- Ownership clearly defined
- Basic metrics exist

**Score 4.0 — Managed**
- Automated where possible
- KPIs defined and tracked (e.g., MTTR, patch SLA compliance %)
- Regular reporting to leadership
- Exceptions formally tracked and risk-accepted

**Score 5.0 — Optimizing**
- Continuous improvement cycle in place
- Predictive/proactive controls (threat intel-driven, automated response)
- Benchmarked against peers
- Feeds back into strategy

---

## Scoring Conventions

- Use **half-point increments** (1.0, 1.5, 2.0, 2.5, ...) for precision
- Score based on **actual state**, not intended or planned state
- When in doubt, **score conservatively** — a 3.0 means it's actually working, not just documented
- **Evidence-based scoring** is preferred: logs, audit reports, tool screenshots, policy documents

---

## Target Score Philosophy

Default targets are set at **4.0 (Managed)** for most controls — the level where security is measurable and defensible to auditors, boards, and regulators.

A score of **3.0** is adequate for lower-risk controls. A score of **5.0** is rarely required and typically only justified for the highest-risk domains (e.g., privileged access, incident response for critical infrastructure).

The goal is not perfection — it is **deliberate, measurable security investment** calibrated to actual risk.
