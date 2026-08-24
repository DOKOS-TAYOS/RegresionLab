"""Tests for plotting utilities."""

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from config import PLOT_CONFIG
from loaders import excel_reader, get_variable_names
from plotting import create_pair_plots, create_plot


def test_pair_plots_preserve_dollar_delimited_column_names_as_mathtext() -> None:
    """Pair plots must retain scientific MathText column labels."""
    data = pd.DataFrame(
        {
            "$x (m)$": [0.0, 1.0, 2.0],
            "$y (m)$": [1.0, 2.0, 3.0],
        }
    )

    figure = create_pair_plots(data, ["$x (m)$", "$y (m)$"])
    figure.canvas.draw()

    assert figure.axes[1].get_xlabel() == r"$y\;(\mathrm{m})$"
    assert figure.axes[1].get_ylabel() == r"$x\;(\mathrm{m})$"

    plt.close(figure)


def test_pair_plots_format_uncertainty_mathtext_as_one_expression() -> None:
    """Uncertainty prefixes must be included in the MathText expression."""
    data = pd.DataFrame(
        {
            "$x (m)$": [0.0, 1.0, 2.0],
            "u$x (m)$": [0.1, 0.1, 0.1],
        }
    )

    figure = create_pair_plots(data, ["$x (m)$", "u$x (m)$"])
    figure.canvas.draw()

    assert figure.axes[1].get_xlabel() == r"$\mathrm{u}x\;(\mathrm{m})$"

    plt.close(figure)


def test_pair_plots_fall_back_to_plain_labels_when_mathtext_is_invalid() -> None:
    """Invalid MathText labels must not prevent a pair plot from rendering."""
    data = pd.DataFrame(
        {
            r"$x\notacommand$": [0.0, 1.0, 2.0],
            "$y (m)$": [1.0, 2.0, 3.0],
        }
    )

    figure = create_pair_plots(data, [r"$x\notacommand$", "$y (m)$"])
    figure.canvas.draw()

    assert figure.axes[1].get_ylabel() == "xnotacommand"

    plt.close(figure)


def test_pair_plots_render_mathtext_headers_from_all_input_workbooks() -> None:
    """Every bundled workbook with MathText headers must render without errors."""
    input_dir = Path(__file__).parent.parent / "input"

    for workbook in sorted(input_dir.glob("*.xlsx")):
        data = excel_reader(str(workbook))
        variable_names = get_variable_names(data, filter_uncertainty=True)
        figure = create_pair_plots(data, variable_names)
        figure.canvas.draw()

        if len(variable_names) > 1:
            for label in (figure.axes[1].get_xlabel(), figure.axes[1].get_ylabel()):
                assert (
                    label.startswith("$") and label.endswith("$")
                    if "$" in label
                    else True
                )

        plt.close(figure)


def test_fit_plot_falls_back_to_plain_title_when_mathtext_is_invalid(
    tmp_path: Path,
) -> None:
    """An invalid MathText title must not prevent a fitted plot from being saved."""
    output_path = tmp_path / "fit.png"

    result = create_plot(
        x=np.array([0.0, 1.0, 2.0]),
        y=np.array([0.0, 1.0, 2.0]),
        ux=np.zeros(3),
        uy=np.zeros(3),
        y_fitted=np.array([0.0, 1.0, 2.0]),
        fit_name=r"$x\notacommand$",
        x_name="x(m)",
        y_name="y(m)",
        plot_config={**PLOT_CONFIG, "show_title": True},
        output_path=output_path,
    )

    assert result == str(output_path)
    assert output_path.exists()
