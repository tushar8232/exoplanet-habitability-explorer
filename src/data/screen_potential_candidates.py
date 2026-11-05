
import pandas as pd

df = pd.read_csv("exoplanets_hz_classified.csv")

# Small planets within the estimated HZ
candidates = df[
    (df["hz_position"] == "Within estimated HZ") &
    (df["pl_rade"] <= 1.6)
].copy()

print("Total planets within estimated HZ:",
      (df["hz_position"] == "Within estimated HZ").sum())

print("Small planets within estimated HZ:", len(candidates))

print("\nPotential screening candidates:")

columns = [
    "pl_name",
    "hostname",
    "pl_rade",
    "pl_orbsmax",
    "hz_inner_au",
    "hz_outer_au",
    "st_teff",
    "st_luminosity"
]

print(
    candidates[columns]
    .sort_values("pl_rade")
    .to_string(index=False)
)

candidates.to_csv("potential_hz_candidates.csv", index=False)

print("\nSaved: potential_hz_candidates.csv")
