
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_kopparapu_classified.csv")

# Optimistic HZ boundaries
optimistic_inner = df["hz_recent_venus_au"]
optimistic_outer = df["hz_early_mars_au"]
orbit = df["pl_orbsmax"]

df["optimistic_hz"] = (
    (orbit >= optimistic_inner) &
    (orbit <= optimistic_outer)
)

# Conservative HZ classification already exists
df["conservative_hz"] = (
    df["kopparapu_position"] == "Within conservative HZ"
)

# Small-planet screening
small_planet = df["pl_rade"] <= 1.6

print("All planets:")
print("Conservative HZ:", df["conservative_hz"].sum())
print("Optimistic HZ:", df["optimistic_hz"].sum())

print("\nSmall planets:")
print("Conservative HZ candidates:",
      (df["conservative_hz"] & small_planet).sum())

print("Optimistic HZ candidates:",
      (df["optimistic_hz"] & small_planet).sum())

print("\nSmall planets in optimistic HZ:")

candidates = df[df["optimistic_hz"] & small_planet]

print(
    candidates[[
        "pl_name",
        "pl_rade",
        "pl_orbsmax",
        "hz_recent_venus_au",
        "hz_runaway_greenhouse_au",
        "hz_maximum_greenhouse_au",
        "hz_early_mars_au"
    ]].round(4).to_string(index=False)
)

df.to_csv("exoplanets_hz_comparison.csv", index=False)

print("\nSaved: exoplanets_hz_comparison.csv")
