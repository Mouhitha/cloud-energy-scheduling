"""Energy accounting for constant-power task execution."""

import math


def energy_wh(power_w: float, runtime_seconds: float) -> float:
    """Return watt-hours assuming constant (or time-averaged) power in watts.

    Runtime is in seconds. Both inputs must be finite and non-negative.
    """
    if not math.isfinite(power_w) or power_w < 0:
        raise ValueError("power_w must be finite and non-negative")
    if not math.isfinite(runtime_seconds) or runtime_seconds < 0:
        raise ValueError("runtime_seconds must be finite and non-negative")
    return power_w * runtime_seconds / 3600.0
