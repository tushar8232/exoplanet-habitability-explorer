
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_with_luminosity.csv")

# Simplified preliminary habitable-zone boundaries
inner_flux = 1.5
outer_flux = 0.35

df["hz_inner_au"] = np.sqrt(
    df["st_luminosity"] / inner_flux
)

df["hz_outer_au"] = np.sqrt(
    df["st_luminosity"] / outer_flux
)

print("Available inner HZ distances:", df["hz_inner_au"].notna().sum())
print("Available outer HZ distances:", df["hz_outer_au"].notna().sum())

print("\nSample results:")

print(
    df[[
        "pl_name",
        "st_luminosity",
        "hz_inner_au",
        "hz_outer_au",
        "pl_orbsmax"
    ]].dropna().head(10).round(4)
)

df.to_csv("exoplanets_with_hz.csv", index=False)

print("\nSaved: exoplanets_with_hz.csv")
