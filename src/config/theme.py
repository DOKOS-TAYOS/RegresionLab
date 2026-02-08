"""UI theme, plot style, and font configuration.

All UI appearance is controlled by a single set of env vars. Fonts, sizes,
colors, relief and spacing are unified for consistency.
"""

import tkinter
from typing import Any, Type, Union

from tkinter import ttk

from config.env import get_env

# -----------------------------------------------------------------------------
# Single source: env vars (reduced set) + derived constants (same default look)
# -----------------------------------------------------------------------------

def _e(key: str, default: Any, cast_type: Type[Union[str, int, float, bool]] = str) -> Any:
    """Read env with default and type (str, int, float, bool)."""
    return get_env(key, default, cast_type)


def _darken_bg(color: str) -> str:
    """Return a slightly darker shade for backgrounds (button active, widget hover)."""
    key = color.lower() if isinstance(color, str) else ''
    m = {
        'navy': 'midnight blue',
        'midnight blue': 'dark slate blue',
        'gray15': 'gray10',
        'gray20': 'gray12',
        'gray25': 'gray20',
    }
    return m.get(key, 'gray12')


def _lighten_fg(color: str) -> str:
    """Return a slightly lighter shade for foreground (button text when active/pressed)."""
    key = color.lower() if isinstance(color, str) else ''
    m = {
        'snow': 'white',
        'lime green': 'pale green',
        'red2': 'indian red',
        'cyan2': 'light cyan',
        'yellow': 'light yellow',
        'white': 'white',
        'forest green': 'lime green',
    }
    return m.get(key, 'white')


def _tooltip_bg_from_ui(ui_bg: str) -> str:
    """UI background -> tooltip background: more grayish and slightly lighter."""
    key = ui_bg.lower() if isinstance(ui_bg, str) else ''
    m = {
        'navy': 'gray30',
        'midnight blue': 'gray30',
        'gray15': 'gray25',
        'gray20': 'gray28',
    }
    return m.get(key, 'gray30')


# Colors (only main knobs; rest derived where used)
_bg = _e('UI_BACKGROUND', 'navy')
_fg = _e('UI_FOREGROUND', 'snow')
_btn_bg = _e('UI_BUTTON_BG', 'midnight blue')
_btn_fg_primary = _e('UI_BUTTON_FG', 'lime green')
_btn_fg_cancel = _e('UI_BUTTON_FG_CANCEL', 'red2')
_btn_fg_accent = _e('UI_BUTTON_FG_CYAN', 'cyan2')
_btn_fg_accent2 = _e('UI_BUTTON_FG_ACCENT2', 'yellow')
_text_bg = _e('UI_TEXT_BG', 'gray15')
_text_fg = _e('UI_TEXT_FG', 'light cyan')
_text_select_bg = _e('UI_TEXT_SELECT_BG', 'steel blue')
_text_select_fg = _e('UI_TEXT_SELECT_FG', 'white')

# Layout and sizes (fixed or derived)
_border = 8
_relief = 'raised'
_padding = _e('UI_PADDING', 8, int)
_btn_w = _e('UI_BUTTON_WIDTH', 12, int)
_btn_wide = int(2.5 * _btn_w)
_spin_w = _e('UI_SPINBOX_WIDTH', 10, int)
_entry_w = _e('UI_ENTRY_WIDTH', 25, int)
_font_family = _e('UI_FONT_FAMILY', 'Menlo')
_font_size = _e('UI_FONT_SIZE', 16, int)
_font_size_large = int(1.25 * _font_size)

# -----------------------------------------------------------------------------
# UI_STYLE: single dict used everywhere (includes aliases for compatibility)
# -----------------------------------------------------------------------------

# Computed once for UI_STYLE (derived from base colors)
_active_bg = _darken_bg(_btn_bg)
_hover_bg = _darken_bg(_bg)
_tooltip_bg = _tooltip_bg_from_ui(_bg)

UI_STYLE = {
    # Core colors
    'bg': _bg,
    'fg': _fg,
    'background': _bg,
    'foreground': _fg,
    'button_bg': _btn_bg,
    'active_bg': _active_bg,
    'button_fg_accept': _btn_fg_primary,
    'button_fg_cancel': _btn_fg_cancel,
    'button_fg_cyan': _btn_fg_accent,
    'button_fg_accent2': _btn_fg_accent2,
    # Hover/focus: element bg darkened (entry, combobox, check, radio use _bg)
    'widget_hover_bg': _hover_bg,
    'checkbutton_hover_bg': _hover_bg,
    'combobox_focus_bg': _hover_bg,
    # Text widget (cursor = text colour)
    'text_bg': _text_bg,
    'text_fg': _text_fg,
    'text_insert_bg': _text_fg,
    'text_select_bg': _text_select_bg,
    'text_select_fg': _text_select_fg,
    # Tooltip: UI bg grayish+lighter, text = UI fg
    'tooltip_bg': _tooltip_bg,
    'tooltip_fg': _fg,
    'tooltip_border': 'gray40',
    # Layout: fixed relief and border
    'relief': _relief,
    'border_width': _border,
    'button_relief': _relief,
    'button_borderwidth': max(1, min(_border, 4)),
    'padding': _padding,
    'padding_x': _padding,
    'padding_y': _padding,
    # Sizes (wide = 2.5*normal, font large = 1.25*normal)
    'button_width': _btn_w,
    'button_width_wide': _btn_wide,
    'spinbox_width': _spin_w,
    'entry_width': _entry_w,
    # Fonts
    'font_family': _font_family,
    'font_size': _font_size,
    'font_size_large': _font_size_large,
    'entry_fg': _bg,
    'text_font_family': _font_family,
    'text_font_size': _font_size,
    'entry_font_size': _font_size,
}

# Backward compatibility: UI_THEME is the same source
UI_THEME = UI_STYLE

# tk Spinbox options so it matches ttk Combobox (same bg, fg, font, relief).
# readonlybackground: needed so readonly state uses theme bg on Windows.
SPINBOX_STYLE: dict[str, Any] = {
    'bg': _bg,
    'fg': _fg,
    'readonlybackground': _bg,
    'font': (_font_family, _font_size),
    'relief': 'sunken',
    'bd': 2,
    'highlightthickness': 0,
    'insertbackground': _fg,
}

# -----------------------------------------------------------------------------
# Button style presets (tk widgets): same relief/border/font, color by role
# -----------------------------------------------------------------------------

def _tk_button_base() -> dict[str, Any]:
    base = {
        'relief': UI_STYLE['button_relief'],
        'bd': UI_STYLE['button_borderwidth'],
        'highlightthickness': 0,
        'activebackground': UI_STYLE['active_bg'],
        'font': (UI_STYLE['font_family'], UI_STYLE['font_size']),
    }
    return base

_BASE_BUTTON = _tk_button_base()

BUTTON_STYLE_PRIMARY = {**_BASE_BUTTON, 'bg': UI_STYLE['button_bg'], 'fg': UI_STYLE['button_fg_accept'], 'activeforeground': _lighten_fg(UI_STYLE['button_fg_accept'])}
BUTTON_STYLE_SECONDARY = {**_BASE_BUTTON, 'bg': UI_STYLE['button_bg'], 'fg': UI_STYLE['fg'], 'activeforeground': _lighten_fg(UI_STYLE['fg'])}
BUTTON_STYLE_DANGER = {**_BASE_BUTTON, 'bg': UI_STYLE['button_bg'], 'fg': UI_STYLE['button_fg_cancel'], 'activeforeground': _lighten_fg(UI_STYLE['button_fg_cancel'])}
BUTTON_STYLE_ACCENT = {**_BASE_BUTTON, 'bg': UI_STYLE['button_bg'], 'fg': UI_STYLE['button_fg_cyan'], 'activeforeground': _lighten_fg(UI_STYLE['button_fg_cyan'])}

# -----------------------------------------------------------------------------
# Plot config (unchanged)
# -----------------------------------------------------------------------------

PLOT_CONFIG = {
    'figsize': (
        get_env('PLOT_FIGSIZE_WIDTH', 12, int),
        get_env('PLOT_FIGSIZE_HEIGHT', 6, int)
    ),
    'dpi': get_env('DPI', 100, int),
    'show_title': get_env('PLOT_SHOW_TITLE', False, bool),
    'line_color': get_env('PLOT_LINE_COLOR', 'black'),
    'line_width': get_env('PLOT_LINE_WIDTH', 1.00, float),
    'line_style': get_env('PLOT_LINE_STYLE', '-'),
    'marker_format': get_env('PLOT_MARKER_FORMAT', 'o'),
    'marker_size': get_env('PLOT_MARKER_SIZE', 5, int),
    'error_color': get_env('PLOT_ERROR_COLOR', 'crimson'),
    'marker_face_color': get_env('PLOT_MARKER_FACE_COLOR', 'crimson'),
    'marker_edge_color': get_env('PLOT_MARKER_EDGE_COLOR', 'crimson'),
}

FONT_CONFIG = {
    'family': get_env('FONT_FAMILY', 'serif'),
    'title_size': get_env('FONT_TITLE_SIZE', 'xx-large'),
    'title_weight': get_env('FONT_TITLE_WEIGHT', 'semibold'),
    'axis_size': get_env('FONT_AXIS_SIZE', 30, int),
    'axis_style': get_env('FONT_AXIS_STYLE', 'italic'),
    'tick_size': get_env('FONT_TICK_SIZE', 16, int)
}

_font_cache = None


def get_entry_font() -> tuple[str, int]:
    """Font tuple for ttk Entry and Combobox (unified with UI base font)."""
    return (UI_STYLE['font_family'], UI_STYLE['font_size'])


def _edge_color(bg_color: str, lighter: bool) -> str:
    """Return a lighter or darker shade for 3D button highlight/shadow."""
    key = bg_color.lower() if isinstance(bg_color, str) else ''
    if lighter:
        m = {'midnight blue': 'steel blue', 'navy': 'steel blue', 'gray15': 'gray30', 'gray20': 'gray35'}
    else:
        m = {'midnight blue': 'midnight blue', 'navy': 'midnight blue', 'gray15': 'gray10', 'gray20': 'gray12'}
    return m.get(key, 'steel blue' if lighter else 'gray12')


def configure_ttk_styles(root: Any) -> None:
    """
    Configure ttk styles from the unified UI_STYLE. Call once after creating
    the Tk root. Uses 'clam' theme for consistent field colors.
    """
    style = ttk.Style(root)
    for theme_name in ('clam', 'alt', 'classic'):
        try:
            style.theme_use(theme_name)
            break
        except tkinter.TclError:
            continue

    fam = UI_STYLE['font_family']
    sz = UI_STYLE['font_size']
    sz_l = UI_STYLE['font_size_large']
    font_normal = (fam, sz)
    font_large = (fam, sz_l)
    font_bold = (fam, sz, 'bold')
    font_large_bold = (fam, sz_l, 'bold')

    bg = UI_STYLE['bg']
    fg = UI_STYLE['fg']
    btn_bg = UI_STYLE['button_bg']
    hover_bg = UI_STYLE['widget_hover_bg']
    btn_light = _edge_color(btn_bg, True)
    btn_dark = _edge_color(btn_bg, False)

    style.configure('TFrame', background=bg)
    style.configure('TLabel', background=bg, foreground=fg, font=font_normal)
    style.configure('Bold.TLabel', background=bg, foreground=fg, font=font_bold)
    style.configure('Large.TLabel', background=bg, foreground=fg, font=font_large)
    style.configure('LargeBold.TLabel', background=bg, foreground=fg, font=font_large_bold)
    style.configure(
        'Tooltip.TLabel',
        background=UI_STYLE['tooltip_bg'],
        foreground=UI_STYLE['tooltip_fg'],
        font=(fam, max(8, sz - 2)),
        padding=(6, 4),
    )
    style.configure('Raised.TFrame', background=btn_light)

    pad = (UI_STYLE['padding'], UI_STYLE['padding'])
    btn_common = {'font': font_normal, 'padding': pad, 'lightcolor': btn_light, 'darkcolor': btn_dark}

    def _btn_style(name: str, fg_color: str) -> None:
        active_fg = _lighten_fg(fg_color)
        style.configure(name, background=btn_bg, foreground=fg_color, **btn_common)
        style.map(
            name,
            background=[('active', UI_STYLE['active_bg']), ('pressed', UI_STYLE['active_bg'])],
            foreground=[('active', active_fg), ('pressed', active_fg)],
            lightcolor=[('pressed', btn_dark)],
            darkcolor=[('pressed', btn_light)],
        )

    _btn_style('TButton', fg)
    _btn_style('Primary.TButton', UI_STYLE['button_fg_accept'])
    _btn_style('Secondary.TButton', fg)
    _btn_style('Danger.TButton', UI_STYLE['button_fg_cancel'])
    _btn_style('Accent.TButton', UI_STYLE['button_fg_cyan'])
    _btn_style('Equation.TButton', UI_STYLE['button_fg_accent2'])

    # Entry: same font as rest of UI
    style.configure(
        'TEntry',
        fieldbackground=bg,
        foreground=fg,
        font=font_normal,
        padding=UI_STYLE['padding'],
    )
    style.configure(
        'TEntry.Hover',
        fieldbackground=hover_bg,
        foreground=fg,
        font=font_normal,
        padding=UI_STYLE['padding'],
    )

    # Combobox
    style.configure(
        'TCombobox',
        fieldbackground=bg,
        foreground=fg,
        background=bg,
        arrowcolor=fg,
        font=font_normal,
        padding=UI_STYLE['padding'],
    )
    style.configure(
        'TCombobox.Hover',
        fieldbackground=hover_bg,
        foreground=fg,
        background=bg,
        arrowcolor=fg,
        font=font_normal,
        padding=UI_STYLE['padding'],
    )
    style.map(
        'TCombobox',
        fieldbackground=[('readonly', bg), ('focus', hover_bg)],
        foreground=[('readonly', fg)],
        background=[('focus', bg)],
        arrowcolor=[('focus', fg), ('readonly', fg)],
    )
    style.map(
        'TCombobox.Hover',
        fieldbackground=[('readonly', hover_bg), ('focus', hover_bg)],
        foreground=[('readonly', fg)],
        background=[('focus', bg)],
        arrowcolor=[('focus', fg), ('readonly', fg)],
    )

    # Radiobutton and Checkbutton: same font and hover
    style.configure('TRadiobutton', background=bg, foreground=fg, font=font_normal)
    style.configure('TRadiobutton.Hover', background=hover_bg, foreground=fg, font=font_normal)
    style.map('TRadiobutton', background=[('active', bg)], foreground=[('active', fg)])
    style.map('TRadiobutton.Hover', background=[('active', hover_bg)], foreground=[('active', fg)])
    style.configure('TCheckbutton', background=bg, foreground=fg, font=font_normal)
    style.configure('TCheckbutton.Hover', background=hover_bg, foreground=fg, font=font_normal)
    style.map('TCheckbutton', background=[('active', bg)], foreground=[('active', fg)])
    style.map('TCheckbutton.Hover', background=[('active', hover_bg)], foreground=[('active', fg)])

    # Scrollbars
    style.configure('Vertical.TScrollbar', background=bg, troughcolor=bg, arrowcolor=fg)
    style.configure('Horizontal.TScrollbar', background=bg, troughcolor=bg, arrowcolor=fg)

    # Config dialog sections
    style.configure('ConfigSectionHeader.TFrame', background=btn_light)
    style.configure('ConfigSectionHeader.TLabel', background=btn_light, foreground=fg, font=font_bold)
    style.configure('ConfigSectionContent.TFrame', background=bg)


def apply_hover_to_children(parent: Any) -> None:
    """Bind hover highlight to ttk Entry, Combobox, Checkbutton, Radiobutton under parent."""
    for w in parent.winfo_children():
        apply_hover_to_children(w)
        cls = w.winfo_class()
        if cls not in ('TEntry', 'TCombobox', 'TCheckbutton', 'TRadiobutton'):
            continue
        hover_style = cls + '.Hover'
        normal_style = w.cget('style') or cls

        def _on_enter(ev: Any, widget: Any = w, norm: str = normal_style, hov: str = hover_style) -> None:
            widget.configure(style=hov)

        def _on_leave(ev: Any, widget: Any = w, norm: str = normal_style, hov: str = hover_style) -> None:
            widget.configure(style=norm)

        w.bind('<Enter>', _on_enter)
        w.bind('<Leave>', _on_leave)


def setup_fonts() -> tuple[Any, Any]:
    """
    Configure and cache font properties for plot titles and axes.
    Returns (title_font, axis_font) from FONT_CONFIG.
    """
    global _font_cache
    if _font_cache is not None:
        return _font_cache

    from matplotlib.font_manager import FontProperties

    try:
        from utils import get_logger
        logger = get_logger(__name__)
    except ImportError:
        logger = None

    def _set_font_property(setter_method: Any, value: Any, property_name: str, default_value: Any) -> None:
        try:
            setter_method(value)
        except (ValueError, KeyError) as e:
            if logger:
                logger.warning(
                    f"Invalid {property_name} '{value}': {e}. Using default '{default_value}'."
                )
            setter_method(default_value)

    font0 = FontProperties()
    fontt = font0.copy()
    fonta = font0.copy()

    _set_font_property(fontt.set_family, FONT_CONFIG['family'], 'font family', 'serif')
    _set_font_property(fontt.set_size, FONT_CONFIG['title_size'], 'title size', 'xx-large')
    _set_font_property(fontt.set_weight, FONT_CONFIG['title_weight'], 'title weight', 'semibold')
    _set_font_property(fonta.set_family, FONT_CONFIG['family'], 'font family', 'serif')
    _set_font_property(fonta.set_size, FONT_CONFIG['axis_size'], 'axis size', 30)
    _set_font_property(fonta.set_style, FONT_CONFIG['axis_style'], 'axis style', 'italic')

    _font_cache = (fontt, fonta)
    return _font_cache
