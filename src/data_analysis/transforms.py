"""Data transforms: Fourier, DCT, Laplace, Hilbert, log, etc."""

from typing import List, Optional

import numpy as np
import pandas as pd

try:
    from scipy.fft import dct, idct
    _HAS_SCIPY_DCT = True
except ImportError:
    dct = None  # type: ignore[assignment, misc]
    idct = None  # type: ignore[assignment, misc]
    _HAS_SCIPY_DCT = False

try:
    from scipy.signal import hilbert
    _HAS_SCIPY_HILBERT = True
except ImportError:
    hilbert = None  # type: ignore[assignment, misc]
    _HAS_SCIPY_HILBERT = False

try:
    from scipy.linalg import hadamard
    _HAS_SCIPY_HADAMARD = True
except ImportError:
    hadamard = None  # type: ignore[assignment, misc]
    _HAS_SCIPY_HADAMARD = False

from data_analysis._utils import get_numeric_columns
from utils import get_logger

logger = get_logger(__name__)

# Transform identifiers for UI
TRANSFORM_FFT = 'fft'
TRANSFORM_FFT_MAGNITUDE = 'fft_magnitude'
TRANSFORM_DCT = 'dct'
TRANSFORM_LOG = 'log'
TRANSFORM_LOG10 = 'log10'
TRANSFORM_EXP = 'exp'
TRANSFORM_SQRT = 'sqrt'
TRANSFORM_SQUARE = 'square'
TRANSFORM_STANDARDIZE = 'standardize'
TRANSFORM_NORMALIZE = 'normalize'
# Laplace, Hilbert, telecom
TRANSFORM_LAPLACE = 'laplace'
TRANSFORM_ILAPLACE = 'ilaplace'
TRANSFORM_HILBERT = 'hilbert'
TRANSFORM_IHILBERT = 'ihilbert'
TRANSFORM_CEPSTRUM = 'cepstrum'
TRANSFORM_HADAMARD = 'hadamard'
TRANSFORM_IHADAMARD = 'ihadamard'
TRANSFORM_ENVELOPE = 'envelope'
# Inverse transforms
TRANSFORM_IFFT = 'ifft'
TRANSFORM_IDCT = 'idct'

# Order: most important/common first (FFT/DCT, log/exp, normalize, Hilbert/Laplace, telecom)
TRANSFORM_OPTIONS: dict[str, str] = {
    TRANSFORM_FFT: 'FFT (complex)',
    TRANSFORM_FFT_MAGNITUDE: 'FFT magnitude',
    TRANSFORM_IFFT: 'Inverse FFT',
    TRANSFORM_DCT: 'DCT (cosine)',
    TRANSFORM_IDCT: 'Inverse DCT',
    TRANSFORM_LOG: 'Log (natural)',
    TRANSFORM_LOG10: 'Log10',
    TRANSFORM_EXP: 'Exp',
    TRANSFORM_SQRT: 'Square root',
    TRANSFORM_SQUARE: 'Square',
    TRANSFORM_STANDARDIZE: 'Standardize (z-score)',
    TRANSFORM_NORMALIZE: 'Normalize [0,1]',
    TRANSFORM_HILBERT: 'Hilbert',
    TRANSFORM_IHILBERT: 'Inverse Hilbert',
    TRANSFORM_ENVELOPE: 'Envelope (Hilbert)',
    TRANSFORM_LAPLACE: 'Laplace (discrete)',
    TRANSFORM_ILAPLACE: 'Inverse Laplace',
    TRANSFORM_CEPSTRUM: 'Cepstrum (real)',
    TRANSFORM_HADAMARD: 'Hadamard (Walsh)',
    TRANSFORM_IHADAMARD: 'Inverse Hadamard',
}


def _apply_to_column(series: pd.Series, transform_id: str) -> pd.Series:
    """
    Apply a single transform to a numeric series.

    Args:
        series: Numeric pandas Series to transform.
        transform_id: One of TRANSFORM_* constants.

    Returns:
        New Series with transformed values (NaN preserved where present).
    """
    arr = np.asarray(series, dtype=float)
    nan_mask = np.isnan(arr)
    valid = arr.copy()
    valid[nan_mask] = 0  # temporary for transforms that don't handle NaN

    if transform_id == TRANSFORM_FFT:
        out = np.fft.fft(valid)
        result = np.real(out)  # store real part in one column, could add imag
        result = np.where(nan_mask, np.nan, result)
        return pd.Series(result, index=series.index, name=series.name)

    if transform_id == TRANSFORM_FFT_MAGNITUDE:
        out = np.fft.fft(valid)
        mag = np.abs(out)
        mag = np.where(nan_mask, np.nan, mag)
        return pd.Series(mag, index=series.index, name=series.name)

    if transform_id == TRANSFORM_DCT:
        if _HAS_SCIPY_DCT and dct is not None:
            out = dct(valid, type=2)
        else:
            out = np.fft.fft(valid).real  # fallback
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_LOG:
        out = np.log(np.where(valid <= 0, np.nan, valid))
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_LOG10:
        out = np.log10(np.where(valid <= 0, np.nan, valid))
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_EXP:
        out = np.exp(valid)
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_SQRT:
        out = np.sqrt(np.where(valid < 0, np.nan, valid))
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_SQUARE:
        out = valid ** 2
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_STANDARDIZE:
        valid_clean = arr[~nan_mask]
        if len(valid_clean) == 0:
            return pd.Series(np.full_like(arr, np.nan), index=series.index, name=series.name)
        mean, std = valid_clean.mean(), valid_clean.std()  # z-score uses population std (ddof=0)
        if std == 0:
            out = np.zeros_like(arr)
        else:
            out = (arr - mean) / std
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_NORMALIZE:
        valid_clean = arr[~nan_mask]
        if len(valid_clean) == 0:
            return pd.Series(np.full_like(arr, np.nan), index=series.index, name=series.name)
        lo, hi = valid_clean.min(), valid_clean.max()
        if hi == lo:
            out = np.zeros_like(arr)
        else:
            out = (arr - lo) / (hi - lo)
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Laplace (discrete cumulative): out[n] = sum_{k=0}^{n} x[k] * exp(-alpha*k), alpha=0.1
    # Uses alpha < 1 for numerical stability in the inverse
    if transform_id == TRANSFORM_LAPLACE:
        alpha = 0.1
        n = len(valid)
        exp_neg = np.exp(-alpha * np.arange(n, dtype=float))
        out = np.cumsum(valid * exp_neg)
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Inverse Laplace: x[n] = (out[n] - out[n-1]) * exp(alpha*n) for n>0, x[0]=out[0]
    if transform_id == TRANSFORM_ILAPLACE:
        alpha = 0.1
        out = np.empty_like(valid)
        out[0] = valid[0]
        n = len(valid)
        if n > 1:
            out[1:] = (valid[1:] - valid[:-1]) * np.exp(alpha * np.arange(1, n, dtype=float))
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Hilbert transform (imaginary part of analytic signal)
    if transform_id == TRANSFORM_HILBERT:
        if _HAS_SCIPY_HILBERT and hilbert is not None:
            analytic = hilbert(valid)
            out = np.imag(analytic)
        else:
            # Fallback: FFT-based Hilbert
            n = len(valid)
            h = np.zeros(n)
            h[0] = 1
            h[n // 2] = 1 if n % 2 == 0 else 0
            h[1 : n // 2] = 2
            out = np.real(np.fft.ifft(np.fft.fft(valid) * h))
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Inverse Hilbert: H(H(x)) = -x, so H^{-1}(y) = -H(y)
    if transform_id == TRANSFORM_IHILBERT:
        if _HAS_SCIPY_HILBERT and hilbert is not None:
            analytic = hilbert(valid)
            out = -np.imag(analytic)
        else:
            n = len(valid)
            h = np.zeros(n)
            h[0] = 1
            h[n // 2] = 1 if n % 2 == 0 else 0
            h[1 : n // 2] = 2
            out = -np.real(np.fft.ifft(np.fft.fft(valid) * h))
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Cepstrum (real): ifft(log(|fft|^2 + eps))
    if transform_id == TRANSFORM_CEPSTRUM:
        spec = np.fft.fft(valid)
        eps = 1e-12
        log_spec = np.log(np.abs(spec) ** 2 + eps)
        out = np.real(np.fft.ifft(log_spec))
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Hadamard (Walsh): orthogonal transform, requires length power of 2
    if transform_id == TRANSFORM_HADAMARD:
        if _HAS_SCIPY_HADAMARD and hadamard is not None:
            n = len(valid)
            n2 = 1 << (n - 1).bit_length()  # next power of 2
            padded = np.zeros(n2)
            padded[:n] = valid
            H = hadamard(n2)
            out_full = (H @ padded) / np.sqrt(n2)
            out = out_full[:n].copy()
        else:
            out = valid.copy()  # fallback: identity
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Inverse Hadamard: H/sqrt(n) is orthonormal, so inverse = H/sqrt(n) (same as forward)
    if transform_id == TRANSFORM_IHADAMARD:
        if _HAS_SCIPY_HADAMARD and hadamard is not None:
            n = len(valid)
            n2 = 1 << (n - 1).bit_length()
            padded = np.zeros(n2)
            padded[:n] = valid
            H = hadamard(n2)
            out_full = (H @ padded) / np.sqrt(n2)
            out = out_full[:n].copy()
        else:
            out = valid.copy()
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Envelope (Hilbert): |analytic signal| = amplitude envelope
    if transform_id == TRANSFORM_ENVELOPE:
        if _HAS_SCIPY_HILBERT and hilbert is not None:
            analytic = hilbert(valid)
            out = np.abs(analytic)
        else:
            n = len(valid)
            h = np.zeros(n)
            h[0] = 1
            h[n // 2] = 1 if n % 2 == 0 else 0
            h[1 : n // 2] = 2
            analytic = np.fft.ifft(np.fft.fft(valid) * h)
            out = np.abs(analytic)
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    # Inverse transforms
    if transform_id == TRANSFORM_IFFT:
        out = np.fft.ifft(valid).real
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    if transform_id == TRANSFORM_IDCT:
        if _HAS_SCIPY_DCT and idct is not None:
            out = idct(valid, type=2)
        else:
            out = np.fft.ifft(valid).real  # fallback
        out = np.where(nan_mask, np.nan, out)
        return pd.Series(out, index=series.index, name=series.name)

    raise ValueError(f"Unknown transform: {transform_id}")


def apply_transform(
    data: pd.DataFrame,
    transform_id: str,
    columns: Optional[List[str]] = None,
    in_place: bool = True,
) -> pd.DataFrame:
    """
    Apply a transform to selected numeric columns.

    Args:
        data: Input DataFrame.
        transform_id: One of TRANSFORM_* constants.
        columns: Columns to transform. If None, all numeric columns.
        in_place: If True, replace columns. If False, add new columns with suffix.

    Returns:
        New DataFrame with transformed columns.
    """
    cols = get_numeric_columns(data, columns)
    if not cols:
        logger.warning("No numeric columns to transform")
        return data.copy()

    result = data.copy()
    for col in cols:
        try:
            transformed = _apply_to_column(result[col], transform_id)
            if in_place:
                result[col] = transformed
            else:
                result[f"{col}_{transform_id}"] = transformed
        except Exception as e:
            logger.warning(f"Transform {transform_id} failed for column {col}: {e}")

    return result
