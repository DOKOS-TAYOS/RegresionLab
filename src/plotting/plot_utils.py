# Standard library
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Union

# Third-party packages
import matplotlib.pyplot as plt

# Local imports
from config import FONT_CONFIG, PLOT_CONFIG, get_output_path, setup_fonts
from utils.logger import get_logger

logger = get_logger(__name__)


def create_plot(
    x: Sequence[float],
    y: Sequence[float],
    ux: Sequence[float],
    uy: Sequence[float],
    y_fitted: Sequence[float],
    fit_name: str,
    x_name: str,
    y_name: str,
    plot_config: Optional[Dict[str, Any]] = None,
    font_config: Optional[Dict[str, Any]] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Create and save a plot with experimental data and fitted curve.

    Args:
        x: Independent variable data (array-like).
        y: Dependent variable data (array-like).
        ux: Uncertainties in x (array-like).
        uy: Uncertainties in y (array-like).
        y_fitted: Fitted y values (array-like).
        fit_name: Name of the fit for plot title.
        x_name: Label for x-axis.
        y_name: Label for y-axis.
        plot_config: Optional plot configuration dict. Defaults to PLOT_CONFIG.
        font_config: Optional font configuration dict. Defaults to FONT_CONFIG.
        output_path: Optional full path to save the plot. If None, uses get_output_path(fit_name).

    Returns:
        Path to the saved plot file (as string).

    Raises:
        OSError: If the plot file cannot be written.
        RuntimeError: If matplotlib fails during plot creation or saving.
    """
    logger.info(f"Creating plot: {fit_name}")
    logger.debug(f"Data points: {len(x)}, x_label: {x_name}, y_label: {y_name}")

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_path = str(output_path)
    else:
        save_path = get_output_path(fit_name)

    try:
        if plot_config is None:
            plot_config = PLOT_CONFIG
        if font_config is None:
            font_config = FONT_CONFIG

        fontt, fonta = setup_fonts()
        logger.debug("Fonts configured")

        fig, ax = plt.subplots(figsize=plot_config['figsize'])
        logger.debug(f"Figure created with size: {plot_config['figsize']}")

        ax.plot(
            x, y_fitted,
            color=plot_config['line_color'],
            lw=plot_config['line_width'],
            ls=plot_config['line_style'],
        )
        ax.errorbar(
            x, y,
            fmt=plot_config['marker_format'],
            markersize=plot_config['marker_size'],
            yerr=uy,
            xerr=ux,
            ecolor=plot_config['error_color'],
            markerfacecolor=plot_config['marker_face_color'],
            markeredgecolor=plot_config['marker_edge_color'],
        )
        logger.debug("Data plotted")

        ax.set_xlabel(x_name, fontproperties=fonta)
        ax.set_ylabel(y_name, fontproperties=fonta)

        if plot_config.get('show_title', False):
            ax.set_title(fit_name, fontproperties=fontt)

        ax.tick_params(axis='both', which='major', labelsize=font_config['tick_size'])
        plt.tight_layout()

        logger.debug(f"Saving plot to: {save_path}")
        plt.savefig(save_path, bbox_inches='tight', dpi=plot_config['dpi'])
        plt.close(fig)

        logger.info(f"Plot saved successfully: {save_path}")
        return save_path

    except Exception as e:
        logger.error(f"Failed to create plot: {str(e)}", exc_info=True)
        try:
            plt.close('all')
        except Exception:
            pass
        raise