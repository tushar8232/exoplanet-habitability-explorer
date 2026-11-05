
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_with_luminosity.csv")

# Kopparapu et al. (2014), 1 Earth-mass coefficients
coefficients = {
    "recent_venus": (1.776, 2.136e-4, 2.533e-8, -1.332e-11, -3.097e-15),
    "runaway_greenhouse": (1.107, 1.332e-4, 1.580e-8, -8.308e-12, -1.931e-15),
    "maximum_greenhouse": (0.356, 6.171e-5, 1.698e-9, -3.198e-12, -5.575e-16),
    "early_mars": (0.320, 5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16)
}

# Only calculate inside the published temperature range
valid = (
    df["st_teff"].between(2600, 7200) &
    df["st_luminosity"].gt(0)
)

delta_t = df["st_teff"] - 5780

for name, (s0, a, b, c, d) in coefficients.items():

    s_eff = (
        s0
        + a * delta_t
        + b * delta_t**2
        + c * delta_t**3
        + d * delta_t**4
    )

    df[f"hz_{name}_au"] = np.nan

    df.loc[valid, f"hz_{name}_au"] = np.sqrt(
        df.loc[valid, "st_luminosity"] /
        s_eff.loc[valid]
    )

print("Total planets:", len(df))
print("Valid stellar temperatures:", valid.sum())

print("\nKopparapu HZ sample:")

columns = [
    "pl_name",
    "st_teff",
    "st_luminosity",
    "hz_recent_venus_au",
    "hz_runaway_greenhouse_au",
    "hz_maximum_greenhouse_au",
    "hz_early_mars_au"
]

print(df[columns].dropna().head(10).round(4).to_string(index=False))

df.to_csv("exoplanets_kopparapu_hz.csv", index=False)

print("\nSaved: exoplanets_kopparapu_hz.csv")
