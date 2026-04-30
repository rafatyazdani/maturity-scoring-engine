import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

from scorer import (
    score_nist_csf, score_cis_v8, score_iso_27001,
    maturity_label, score_bar, MATURITY_LEVELS,
)
from report import generate_report
from frameworks import nist_csf, cis_controls, iso_27001

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="OrionMaturity",
    page_icon="🛡",
    layout="wide",
)

st.title("OrionMaturity — Security Program Maturity Scoring Engine")
st.caption("Quantitative maturity scoring for NIST CSF 2.0 · CIS Controls v8 · ISO/IEC 27001:2022")

# ── Colour palette ────────────────────────────────────────────────────────────

LEVEL_COLORS = {
    "Initial":    "#FF4B4B",
    "Developing": "#FFA500",
    "Defined":    "#FFD700",
    "Managed":    "#00C4B4",
    "Optimizing": "#00CC44",
}

def level_color(score):
    name, _ = maturity_label(score)
    return LEVEL_COLORS.get(name, "#888888")

# ── Sidebar — org info + framework selector ───────────────────────────────────

st.sidebar.header("Assessment Settings")
org      = st.sidebar.text_input("Organization", value="Acme Corporation")
assessor = st.sidebar.text_input("Assessor", value="Security Team")

framework = st.sidebar.radio(
    "Framework",
    ["NIST CSF 2.0", "CIS Controls v8", "ISO/IEC 27001:2022"],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Maturity Scale**")
for lo, hi, name, _ in MATURITY_LEVELS:
    color = LEVEL_COLORS[name]
    hi_str = f"{hi:.0f}" if hi == 5.0 else f"{hi:.1f}"
    st.sidebar.markdown(
        f'<span style="color:{color}">■</span> **{name}** ({lo:.1f}–{hi_str})',
        unsafe_allow_html=True,
    )

# ── Helper: render domain score bar ──────────────────────────────────────────

def render_score_metric(label, score, target, cols):
    name, _ = maturity_label(score)
    color = level_color(score)
    gap = target - score
    cols[0].markdown(f"**{label}**")
    cols[1].markdown(
        f'<span style="font-size:1.4rem;color:{color}"><b>{score:.1f}</b></span> / 5.0',
        unsafe_allow_html=True,
    )
    cols[2].markdown(f"`{name}`")
    cols[3].markdown(f"{'–' if gap <= 0 else f'-{gap:.1f}'}")


# ── NIST CSF 2.0 ─────────────────────────────────────────────────────────────

if framework == "NIST CSF 2.0":
    st.markdown("## NIST Cybersecurity Framework 2.0")

    scores_input = {"scores": {}}
    for fn_key, fn_def in nist_csf.FUNCTIONS.items():
        with st.expander(f"**{fn_def['label']}** — {fn_def['description']}", expanded=False):
            fn_scores = {}
            cols = st.columns(len(fn_def["subdomains"]))
            for i, (sd_key, sd_def) in enumerate(fn_def["subdomains"].items()):
                target = nist_csf.TARGET_SCORES[fn_key][sd_key]
                fn_scores[sd_key] = cols[i].slider(
                    sd_def["label"], 1.0, 5.0, 2.5, 0.5,
                    key=f"nist_{fn_key}_{sd_key}",
                    help=f"Target: {target}"
                )
            scores_input["scores"][fn_key] = fn_scores

    result = score_nist_csf(scores_input, org, assessor)

    # ── Overall score ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Overall Maturity Score")
    col1, col2, col3 = st.columns([1, 2, 1])
    color = level_color(result.overall_score)
    col1.markdown(
        f'<div style="font-size:3rem;color:{color};text-align:center"><b>{result.overall_score:.1f}</b><br>'
        f'<span style="font-size:1rem">{result.maturity_name}</span></div>',
        unsafe_allow_html=True,
    )
    with col2:
        fig, ax = plt.subplots(figsize=(6, 0.6))
        ax.barh([""], [result.overall_score], color=color, height=0.5)
        ax.barh([""], [5.0 - result.overall_score], left=[result.overall_score],
                color="#e0e0e0", height=0.5)
        ax.set_xlim(0, 5)
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(["1\nInitial", "2\nDeveloping", "3\nDefined", "4\nManaged", "5\nOptimizing"],
                           fontsize=7)
        ax.set_yticks([])
        fig.tight_layout(pad=0.2)
        st.pyplot(fig)
    col3.markdown(f"> {result.maturity_desc}")

    # ── Domain chart ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Domain Scores vs. Targets")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    labels = [d.label for d in result.domains]
    scores = [d.weighted_score for d in result.domains]
    targets = [d.target_score for d in result.domains]
    colors = [level_color(s) for s in scores]
    x = np.arange(len(labels))
    bars = ax2.bar(x, scores, color=colors, alpha=0.85, label="Current")
    ax2.plot(x, targets, "o--", color="#333", linewidth=1.2, markersize=5, label="Target")
    ax2.set_ylim(0, 5.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9)
    ax2.set_ylabel("Maturity Score")
    ax2.set_title("NIST CSF 2.0 — Function Scores vs. Targets")
    ax2.legend(fontsize=8)
    for bar, score in zip(bars, scores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{score:.1f}", ha="center", va="bottom", fontsize=8)
    fig2.tight_layout()
    st.pyplot(fig2)

    # ── Gap table ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Priority Gap Analysis")
    if result.gaps:
        gap_data = [{
            "Sub-domain": g.label,
            "Current": g.score,
            "Target": g.target,
            "Gap": round(g.gap, 1),
            "Level": g.maturity_name,
        } for g in result.gaps[:10]]
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
    else:
        st.success("No significant gaps. All domains within 0.5 of target.")

    # ── Download report ───────────────────────────────────────────────────────
    st.markdown("---")
    report_md = generate_report(result)
    st.download_button("Download Full Report (.md)", report_md,
                       file_name="nist_csf_maturity_report.md", mime="text/markdown")


# ── CIS Controls v8 ──────────────────────────────────────────────────────────

elif framework == "CIS Controls v8":
    st.markdown("## CIS Controls v8")

    scores_input = {"scores": {}}
    for ig_num in [1, 2, 3]:
        ig_controls = {k: v for k, v in cis_controls.CONTROLS.items() if v["ig"] == ig_num}
        with st.expander(f"**{cis_controls.IG_LABELS[ig_num]}**", expanded=(ig_num == 1)):
            cols = st.columns(min(len(ig_controls), 4))
            for i, (ctrl_key, ctrl_def) in enumerate(ig_controls.items()):
                target = cis_controls.TARGET_SCORES[ctrl_key]
                scores_input["scores"][ctrl_key] = cols[i % 4].slider(
                    f"{ctrl_key}: {ctrl_def['label'][:30]}",
                    1.0, 5.0, 2.5, 0.5,
                    key=f"cis_{ctrl_key}",
                    help=f"Target: {target}"
                )

    result = score_cis_v8(scores_input, org, assessor)

    st.markdown("---")
    st.markdown("### Overall Maturity Score")
    col1, col2, col3 = st.columns([1, 2, 1])
    color = level_color(result.overall_score)
    col1.markdown(
        f'<div style="font-size:3rem;color:{color};text-align:center"><b>{result.overall_score:.1f}</b><br>'
        f'<span style="font-size:1rem">{result.maturity_name}</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### All 18 Controls — Heat Map")
    ctrl_keys = list(cis_controls.CONTROLS.keys())
    ctrl_labels = [f"{k}\n{v['label'][:20]}" for k, v in cis_controls.CONTROLS.items()]
    ctrl_scores = [scores_input["scores"].get(k, 1.0) for k in ctrl_keys]
    ctrl_targets = [cis_controls.TARGET_SCORES[k] for k in ctrl_keys]

    fig3, ax3 = plt.subplots(figsize=(12, 4))
    colors_h = [level_color(s) for s in ctrl_scores]
    x = np.arange(len(ctrl_keys))
    bars = ax3.bar(x, ctrl_scores, color=colors_h, alpha=0.85)
    ax3.plot(x, ctrl_targets, "o--", color="#333", linewidth=1, markersize=4, label="Target")
    ax3.set_ylim(0, 5.5)
    ax3.set_xticks(x)
    ax3.set_xticklabels([k for k in ctrl_keys], fontsize=7, rotation=45)
    ax3.set_ylabel("Score")
    ax3.set_title("CIS Controls v8 — All Controls vs. Targets")
    ax3.legend(fontsize=8)
    patches = [mpatches.Patch(color=v, label=k) for k, v in LEVEL_COLORS.items()]
    ax3.legend(handles=patches + [plt.Line2D([0], [0], color="#333", linestyle="--", marker="o",
               label="Target")], fontsize=7, loc="upper right")
    fig3.tight_layout()
    st.pyplot(fig3)

    st.markdown("---")
    st.markdown("### Priority Gap Analysis")
    if result.gaps:
        gap_data = [{
            "Control": g.label,
            "Current": g.score,
            "Target": g.target,
            "Gap": round(g.gap, 1),
            "Level": g.maturity_name,
        } for g in result.gaps[:10]]
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
    else:
        st.success("No significant gaps.")

    st.markdown("---")
    report_md = generate_report(result)
    st.download_button("Download Full Report (.md)", report_md,
                       file_name="cis_v8_maturity_report.md", mime="text/markdown")


# ── ISO 27001 ─────────────────────────────────────────────────────────────────

else:
    st.markdown("## ISO/IEC 27001:2022")

    scores_input = {"scores": {}, "clause_scores": {}}

    for theme_key, theme_def in iso_27001.ANNEX_A.items():
        with st.expander(f"**{theme_def['label']}** — {theme_def['description']}", expanded=False):
            theme_scores = {}
            cols = st.columns(len(theme_def["subdomains"]))
            for i, (sd_key, sd_def) in enumerate(theme_def["subdomains"].items()):
                target = iso_27001.TARGET_SCORES[theme_key][sd_key]
                theme_scores[sd_key] = cols[i].slider(
                    sd_def["label"], 1.0, 5.0, 2.5, 0.5,
                    key=f"iso_{theme_key}_{sd_key}",
                    help=f"Target: {target}"
                )
            scores_input["scores"][theme_key] = theme_scores

    with st.expander("**Management System Clauses (4–10)**", expanded=False):
        cols = st.columns(len(iso_27001.CLAUSES))
        for i, (c_key, c_def) in enumerate(iso_27001.CLAUSES.items()):
            scores_input["clause_scores"][c_key] = cols[i].slider(
                c_def["label"][:25], 1.0, 5.0, 2.5, 0.5,
                key=f"iso_clause_{c_key}"
            )

    result = score_iso_27001(scores_input, org, assessor)

    st.markdown("---")
    st.markdown("### Overall Maturity Score")
    col1, col2, col3 = st.columns([1, 2, 1])
    color = level_color(result.overall_score)
    col1.markdown(
        f'<div style="font-size:3rem;color:{color};text-align:center"><b>{result.overall_score:.1f}</b><br>'
        f'<span style="font-size:1rem">{result.maturity_name}</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Annex A Control Themes vs. Targets")
    annex_domains = [d for d in result.domains if d.key != "CLAUSES"]
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    labels = [d.label.split(" — ")[0] for d in annex_domains]
    scores = [d.weighted_score for d in annex_domains]
    targets = [d.target_score for d in annex_domains]
    colors4 = [level_color(s) for s in scores]
    x = np.arange(len(labels))
    bars = ax4.bar(x, scores, color=colors4, alpha=0.85)
    ax4.plot(x, targets, "o--", color="#333", linewidth=1.2, markersize=5, label="Target")
    ax4.set_ylim(0, 5.5)
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, fontsize=9)
    ax4.set_ylabel("Maturity Score")
    ax4.set_title("ISO 27001:2022 — Annex A Themes vs. Targets")
    ax4.legend(fontsize=8)
    for bar, score in zip(bars, scores):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{score:.1f}", ha="center", va="bottom", fontsize=9)
    fig4.tight_layout()
    st.pyplot(fig4)

    st.markdown("---")
    st.markdown("### Priority Gap Analysis")
    if result.gaps:
        gap_data = [{
            "Control Area": g.label,
            "Current": g.score,
            "Target": g.target,
            "Gap": round(g.gap, 1),
            "Level": g.maturity_name,
        } for g in result.gaps[:10]]
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
    else:
        st.success("No significant gaps.")

    st.markdown("---")
    report_md = generate_report(result)
    st.download_button("Download Full Report (.md)", report_md,
                       file_name="iso_27001_maturity_report.md", mime="text/markdown")


# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown(
    """
    ---
    **OrionMaturity** — Data-driven security program maturity scoring.
    Scores feed directly into financial risk models (ALE, ROSI) via the CRQ-F methodology.
    """
)
