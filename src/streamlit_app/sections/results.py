"""Results display for the Streamlit app."""

import os
from typing import Any, Dict, List, Tuple

import streamlit as st

from i18n import t


def _split_equation(equation_str: str) -> Tuple[str, str]:
    """Split equation string into formula (optional) and formatted equation. Both left-aligned."""
    parts = equation_str.strip().split("\n", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return "", parts[0].strip()


def _split_parameters_text(text: str) -> Tuple[List[str], List[str]]:
    """
    Split backend parameters text into:
    - Statistics: R², RMSE, χ², χ²_red, dof (exactly 5 lines).
    - Parameters: fit params (a, b, c) with uncertainties and their IC 95%.
    Backend order: (param=value , σ(param)=unc)* then 5 stats lines then (param IC 95%)*.
    """
    lines = [ln.strip() for ln in text.strip().split("\n") if ln.strip()]
    # Find where statistics start (first line containing R²)
    stats_start = -1
    for i, ln in enumerate(lines):
        if "R²" in ln or "R\u00B2" in ln:
            stats_start = i
            break
    if stats_start < 0:
        return [], lines
    stats_lines = lines[stats_start : stats_start + 5]
    param_value_lines = lines[:stats_start]  # param=value , σ(param)=unc
    param_ci_lines = lines[stats_start + 5 :]  # param IC 95%: [...]
    param_lines = param_value_lines + param_ci_lines
    return stats_lines, param_lines


def show_results(results: List[Dict[str, Any]]) -> None:
    """Display fitting results: equation (formula + formatted) left, params center, stats right; plot; download below."""
    if not results:
        return

    st.markdown('---')
    st.header(t('dialog.results_title'))

    for idx, result in enumerate(results):
        with st.container():
            st.markdown(f"### {result['plot_name']} - {result['equation_name']}")

            formula_line, formatted_line = _split_equation(result["equation"])
            stats_lines, param_lines = _split_parameters_text(result["parameters"])

            eq_col, params_col, stats_col = st.columns([1, 1, 1])

            with eq_col:
                if formula_line:
                    st.markdown(f"**{t('dialog.equation_formula')}**")
                    st.text(formula_line)
                st.markdown(f"**{t('dialog.equation_formatted')}**")
                st.text(formatted_line)

            with params_col:
                if param_lines:
                    st.markdown(f"**{t('dialog.results_params_heading')}**")
                    for line in param_lines:
                        st.text(line)

            with stats_col:
                if stats_lines:
                    st.markdown(f"**{t('dialog.results_stats_heading')}**")
                    for line in stats_lines:
                        st.text(line)

            if os.path.exists(result["plot_path"]):
                plot_path = result["plot_path"]
                plot_path_display = result.get("plot_path_display") or plot_path
                plot_ext = os.path.splitext(plot_path)[1].lower() or ".png"
                mime_map = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".pdf": "application/pdf",
                }
                mime = mime_map.get(plot_ext, "image/png")
                download_name = f"{result['plot_name']}{plot_ext}"

                if os.path.exists(plot_path_display) and os.path.splitext(plot_path_display)[1].lower() in (
                    ".png",
                    ".jpg",
                    ".jpeg",
                ):
                    st.image(plot_path_display, use_container_width=True)
                elif plot_ext == ".pdf":
                    st.caption(t("dialog.plot_pdf_preview_caption"))

                st.markdown("")  # spacing
                with open(plot_path, "rb") as file:
                    st.download_button(
                        label=f"📥 {t('dialog.download')}",
                        data=file,
                        file_name=download_name,
                        mime=mime,
                        key=f"download_{idx}",
                    )
            else:
                st.text(result["parameters"])
