import dill as pkl
import numpy as np
import matplotlib.pyplot as plt

from functions import s2y

# ---------------------------------------------------------
# Load thermal evolution
# ---------------------------------------------------------

with open("Demo/thermal.pkl", "rb") as f:
    Q = pkl.load(f)

# ---------------------------------------------------------
# Times we want
# ---------------------------------------------------------

times_yr = [0.0, 5e8, 1.5e9, 5e9]
colors = ["purple", "blue", "green", "orange"]

t_yr = s2y(Q.t)

indices = [
    np.argmin(np.abs(t_yr - tt))
    for tt in times_yr
]

# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

for idx, color, target_time in zip(indices, colors, times_yr):

    S = Q.S[idx]

    # Core
    ax.plot(
        S.radius_core / 1e3,
        S.T_core,
        color=color,
        lw=1.8,
    )

    # BMO
    ax.plot(
        S.radius_BMO_r_0 / 1e3,
        S.Ta_BMO_r_0,
        color=color,
        lw=1.8,
    )

    # Mantle
    ax.plot(
        S.radius_mantle / 1e3,
        Q.T_mantle[idx],
        color=color,
        lw=1.8,
    )


# ---------------------------------------------------------
# Melting curves
# Use initial structure because these are basically
# pressure-dependent reference curves
# ---------------------------------------------------------

S0 = Q.S[0]

ax.plot(
    S0.radius_silicate / 1e3,
    S0.Tm_mantle,
    "--",
    color="purple",
    lw=1.5,
    label="Mantle liquidus",
)

ax.plot(
    S0.radius_core / 1e3,
    S0.Tm_core,
    "-.",
    color="purple",
    lw=1.5,
    label="Core liquidus",
)

# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------

ax.set_xlabel(r"$r$ (km)")
ax.set_ylabel(r"$T$ (K)")

ax.grid(alpha=0.25)

# Legend for times
time_handles = []

for c, tt in zip(colors, times_yr):
    time_handles.append(
        plt.Line2D(
            [0], [0],
            color=c,
            lw=2,
            label=f"t = {tt:.2e} yr"
        )
    )

ax.legend(
    handles=time_handles,
    loc="lower left",
)

plt.tight_layout()
plt.savefig("temperature_profiles.png", dpi=300)
plt.show()
