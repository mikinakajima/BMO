#!/usr/bin/env python3
"""
Plot full radial temperature profiles from an EVO-1D-SUPER-EARTH thermal.pkl file.

The profile is assembled from:
    1. core adiabat       : S.radius_core, S.T_core
    2. basal magma ocean  : S.radius_BMO_r_0_i, S.Ta_BMO_r_0_i
    3. solid mantle       : S.radius_mantle, Q.T_mantle

The BMO is plotted dashed, matching the earlier figure.
"""

import dill as pkl
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------
THERMAL_FILE = "Demo/thermal.pkl"

# Times to plot [yr]
times_to_plot = [0.0, 5.0e8, 1.5e9, 5.0e9]

SECONDS_PER_YEAR = 365.25 * 24.0 * 3600.0


# ----------------------------------------------------------------------
# Load thermal evolution
# ----------------------------------------------------------------------
with open(THERMAL_FILE, "rb") as f:
    Q = pkl.load(f)

t_yr = np.asarray(Q.t) / SECONDS_PER_YEAR


# ----------------------------------------------------------------------
# Plot
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))

# Colors chosen to reproduce the earlier plot.
colors = ["purple", "blue", "green", "orange"]

for target_time, color in zip(times_to_plot, colors):

    # Find simulation output closest to requested time.
    i = int(np.argmin(np.abs(t_yr - target_time)))
    S = Q.S[i]

    print(
        "requested = %.3e yr, actual = %.3e yr, index = %d"
        % (target_time, t_yr[i], i)
    )

    # --------------------------------------------------------------
    # CORE
    # --------------------------------------------------------------
    r_core = np.asarray(S.radius_core, dtype=float) / 1e3
    T_core = np.asarray(S.T_core, dtype=float)

    mask = np.isfinite(r_core) & np.isfinite(T_core)

    ax.plot(
        r_core[mask],
        T_core[mask],
        color=color,
        lw=2.5,
        label="t = %.2e yr" % target_time,
    )

    # --------------------------------------------------------------
    # BASAL MAGMA OCEAN
    #
    # The *_r_0_i arrays are the current BMO adiabat evaluated on the
    # reference silicate radial coordinate used by the thermal model.
    # Plot dashed so the molten layer is visually distinct.
    # --------------------------------------------------------------
    if hasattr(S, "radius_BMO_r_0_i") and hasattr(S, "Ta_BMO_r_0_i"):

        r_bmo = np.asarray(S.radius_BMO_r_0_i, dtype=float) / 1e3
        T_bmo = np.asarray(S.Ta_BMO_r_0_i, dtype=float)

        mask = np.isfinite(r_bmo) & np.isfinite(T_bmo)

        if np.count_nonzero(mask) > 1:
            ax.plot(
                r_bmo[mask],
                T_bmo[mask],
                color=color,
                lw=2.5,
                ls="--",
            )

    # --------------------------------------------------------------
    # SOLID MANTLE
    # --------------------------------------------------------------
    r_mantle = np.asarray(S.radius_mantle, dtype=float) / 1e3
    T_mantle = np.asarray(Q.T_mantle[i], dtype=float)

    mask = np.isfinite(r_mantle) & np.isfinite(T_mantle)

    ax.plot(
        r_mantle[mask],
        T_mantle[mask],
        color=color,
        lw=2.5,
    )


# ----------------------------------------------------------------------
# Formatting
# ----------------------------------------------------------------------
ax.set_xlabel(r"$r$ (km)", fontsize=18)
ax.set_ylabel(r"$T$ (K)", fontsize=18)

ax.tick_params(axis="both", labelsize=14)
ax.legend(fontsize=13, loc="lower left")
ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig("temperature_profiles.png", dpi=300)
plt.show()
