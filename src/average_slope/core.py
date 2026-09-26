"""Calculation of average slope from concentration-time observations."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Literal, Sequence

TieRule = Literal["first", "last", "error"]


@dataclass(frozen=True)
class AverageSlopeResult:
    """Calculated metric and the observations used in its calculation."""

    average_slope: float
    cmax: float
    tmax: float
    n_points: int
    interval_slopes: tuple[float, ...]


def average_slope(
    times: Sequence[float] | Iterable[float],
    concentrations: Sequence[float] | Iterable[float],
    *,
    tmax_tie: TieRule = "first",
) -> AverageSlopeResult:
    """Calculate average slope from t=0 through the observed Tmax.

    For ``n`` observations from time zero through Tmax, inclusive:

        AS = (1 / (n - 1)) * sum((C[i+1] - C[i]) / (t[i+1] - t[i]))

    Times must be finite, non-negative, strictly increasing, and start at zero.
    Concentrations must be finite and non-negative. When Cmax occurs more than
    once, ``tmax_tie`` selects the first or last occurrence, or raises an error.
    The default, ``first``, follows the conventional observed-Tmax definition.
    """
    t = tuple(float(value) for value in times)
    c = tuple(float(value) for value in concentrations)

    if len(t) != len(c):
        raise ValueError("times and concentrations must have the same length")
    if len(t) < 2:
        raise ValueError("at least two observations are required")
    if tmax_tie not in ("first", "last", "error"):
        raise ValueError("tmax_tie must be 'first', 'last', or 'error'")
    if not all(isfinite(value) for value in t + c):
        raise ValueError("times and concentrations must contain only finite values")
    if t[0] != 0.0:
        raise ValueError("the first observation must be at t=0")
    if any(value < 0.0 for value in t):
        raise ValueError("times must be non-negative")
    if any(value < 0.0 for value in c):
        raise ValueError("concentrations must be non-negative")
    if any(right <= left for left, right in zip(t, t[1:])):
        raise ValueError("times must be strictly increasing with no duplicates")

    cmax = max(c)
    maxima = [index for index, value in enumerate(c) if value == cmax]
    if len(maxima) > 1 and tmax_tie == "error":
        raise ValueError("Cmax occurs at more than one time; choose a tie rule")
    peak_index = maxima[-1] if tmax_tie == "last" else maxima[0]
    if peak_index == 0:
        raise ValueError("Tmax is t=0, so no ascending interval exists")

    slopes = tuple(
        (c[index + 1] - c[index]) / (t[index + 1] - t[index])
        for index in range(peak_index)
    )
    return AverageSlopeResult(
        average_slope=sum(slopes) / len(slopes),
        cmax=cmax,
        tmax=t[peak_index],
        n_points=peak_index + 1,
        interval_slopes=slopes,
    )

