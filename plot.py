import dill as pkl
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Load thermal evolution
# ------------------------------------------------------------

with open("Demo/thermal.pkl", "rb") as f:
    Q = pkl.load(f)

seconds_per_year = 365.25 * 24.0 * 3600.0
t_Gyr = np.asarray(Q.t) / seconds_per_year / 1.0e9


# ------------------------------------------------------------
# Load magnetic evolution
# ------------------------------------------------------------

with open("Demo/magnetic_nominal.pkl", "rb") as f:
    M = pkl.load(f)


# ------------------------------------------------------------
# Print ranges
# ------------------------------------------------------------

print("BMO surface field [uT]:",
      np.nanmin(M.BS_S_BMO_cst * 1e6),
      np.nanmax(M.BS_S_BMO_cst * 1e6))

print("Core surface field [uT]:",
      np.nanmin(M.BS_S_core_cst * 1e6),
      np.nanmax(M.BS_S_core_cst * 1e6))


# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(
    t_Gyr,
    M.BS_S_BMO_cst * 1e6,
    linewidth=2,
    label="BMO",
)

ax.plot(
    t_Gyr,
    M.BS_S_core_cst * 1e6,
    linewidth=2,
    label="Core",
)

ax.set_xlabel("Time (Gyr)", fontsize=14)
ax.set_ylabel("Surface magnetic field ($\\mu$T)", fontsize=14)

ax.set_xlim(0, 10)

ax.legend(fontsize=11)
ax.grid(alpha=0.2)

plt.tight_layout()
plt.show()