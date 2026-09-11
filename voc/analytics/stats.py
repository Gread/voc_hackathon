"""Small statistics helpers shared by the analytics: Wilson interval, log rate ratio, WLS direction."""
from __future__ import annotations

import math
from typing import Sequence

Z95 = 1.96
T_CUT = 2.0


def wilson_interval(n: int, N: int, z: float = Z95) -> tuple[float, float]:
    """Wilson 95 % interval for a share n/N; (0, 0) when the slice is empty."""
    if N <= 0:
        return (0.0, 0.0)
    p = n / N
    denom = 1.0 + z * z / N
    centre = (p + z * z / (2 * N)) / denom
    half = z * math.sqrt(p * (1.0 - p) / N + z * z / (4.0 * N * N)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def log_rate_ratio(n_a: int, N_a: int, n_b: int, N_b: int, z: float = Z95) -> tuple[float, float, float]:
    """Rate ratio (a / b) with a log-scale interval; 0.5 continuity correction keeps zeros finite."""
    r_a = (n_a + 0.5) / (N_a + 1.0)
    r_b = (n_b + 0.5) / (N_b + 1.0)
    rr = r_a / r_b
    se = math.sqrt(1.0 / (n_a + 0.5) + 1.0 / (n_b + 0.5))
    return (rr, rr * math.exp(-z * se), rr * math.exp(z * se))


def wls_direction(shares: Sequence[float], weights: Sequence[float], t_cut: float = T_CUT) -> tuple[str, float, float]:
    """Weighted least squares of share on period index.

    Returns (direction, t_stat, change_pts): direction is rising/falling/flat with |t| >= t_cut as the cut,
    change_pts is the fitted change over the window in share points (slope x (k-1) x 100).
    """
    k = len(shares)
    if k != len(weights):
        raise ValueError("shares and weights must have the same length")
    if k < 3 or sum(weights) <= 0:
        return ("flat", 0.0, 0.0)
    w = [float(v) for v in weights]
    x = [float(i) for i in range(k)]
    y = [float(v) for v in shares]
    sw = sum(w)
    x_bar = sum(wi * xi for wi, xi in zip(w, x)) / sw
    y_bar = sum(wi * yi for wi, yi in zip(w, y)) / sw
    sxx = sum(wi * (xi - x_bar) ** 2 for wi, xi in zip(w, x))
    if sxx <= 0:
        return ("flat", 0.0, 0.0)
    slope = sum(wi * (xi - x_bar) * (yi - y_bar) for wi, xi, yi in zip(w, x, y)) / sxx
    intercept = y_bar - slope * x_bar
    rss = sum(wi * (yi - (intercept + slope * xi)) ** 2 for wi, xi, yi in zip(w, x, y))
    s2 = rss / (k - 2)
    se = math.sqrt(s2 / sxx) if s2 > 0 else 0.0
    if se == 0.0:
        t = 0.0 if abs(slope) < 1e-12 else math.copysign(float("inf"), slope)
    else:
        t = slope / se
    direction = "rising" if t >= t_cut else "falling" if t <= -t_cut else "flat"
    return (direction, t, slope * (k - 1) * 100.0)


def period_change(n_cur: int, N_cur: int, n_prev: int, N_prev: int) -> tuple[int, float]:
    """Absolute change in calls and in share points between two equal-length periods."""
    share_cur = n_cur / N_cur if N_cur else 0.0
    share_prev = n_prev / N_prev if N_prev else 0.0
    return (n_cur - n_prev, (share_cur - share_prev) * 100.0)
