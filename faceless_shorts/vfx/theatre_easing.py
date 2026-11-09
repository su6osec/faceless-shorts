"""
Theatre.js Inspired Cinematic Easing & Motion Curve Physics.
Provides non-linear bezier, elastic spring, and velocity curves for Ken Burns cameras.
Inspired by https://github.com/theatre-js/theatre
"""

import math
from typing import Dict, Tuple

def get_theatre_motion_expr(
    motion_type: str,
    total_frames: int
) -> Tuple[str, str, str]:
    """
    Returns (zoom_expr, x_expr, y_expr) for FFmpeg zoompan filter
    using Theatre.js-style physical easing and non-linear momentum.
    """
    # Normalized progress p = on / total_frames (0.0 to 1.0)
    p = f"(on/{total_frames})"

    if motion_type == "theatre_spring_zoom":
        # Elastic spring zoom: starts fast, overshoots to 1.38x, and rebounds to 1.32x
        # f(p) = 1.0 + 0.35 * (1 - exp(-4*p) * cos(6*p))
        z_expr = f"min(1.0 + 0.35 * (1 - exp(-4.5*{p}) * cos(6.0*{p})), 1.40)"
        x_expr = "iw/2-(iw/zoom/2)"
        y_expr = "ih/2-(ih/zoom/2)"

    elif motion_type == "theatre_whip_pan":
        # Cinematic whip tracking with exponential acceleration
        z_expr = "1.28"
        x_expr = f"min((iw-iw/zoom)*(pow({p}, 1.8)), iw-iw/zoom)"
        y_expr = f"ih/2-(ih/zoom/2) + sin({p} * 3.14159) * 20"

    elif motion_type == "theatre_cinematic_drift":
        # Slow floating camera with subtle breathing float
        z_expr = f"1.05 + 0.18 * sin({p} * 1.57)"
        x_expr = f"iw/2-(iw/zoom/2) + sin(on * 0.04) * 25"
        y_expr = f"ih/2-(ih/zoom/2) + cos(on * 0.03) * 18"

    elif motion_type == "theatre_elastic_reveal":
        # Starts zoomed close (1.35x) and pulls back with damped harmonic oscillation
        z_expr = f"max(1.02 + 0.33 * exp(-3.5*{p}), 1.02)"
        x_expr = f"iw/2-(iw/zoom/2) + sin({p} * 6.28) * 15"
        y_expr = "ih/2-(ih/zoom/2)"

    else: # Default smooth cubic ease-in-out
        z_expr = f"min(1.0 + 0.36 * (3*pow({p},2) - 2*pow({p},3)), 1.38)"
        x_expr = "iw/2-(iw/zoom/2)"
        y_expr = "ih/2-(ih/zoom/2)"

    return z_expr, x_expr, y_expr
