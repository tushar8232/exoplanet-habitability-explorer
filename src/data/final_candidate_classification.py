
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_hz_comparison.csv")

orbit = df["pl_orbsmax"]

valid = (
    orbit.notna()
    & df["hz_recent_venus_au"].notna()
    & df["hz_early_mars_au"].notna()
)

conservative = df["conservative_hz"].fillna(False)
optimistic = df["optimistic_hz"].fillna(False)

df["final_hz_category"] = np.select(
    [
        ~valid,
        conservative,
        optimistic & ~conservative
    ],
    [
        "Insufficient data",
        "Conservative HZ",
        "Optimistic-only HZ"
    ],
    default="Outside optimistic HZ"
)

df["small_planet"] = df["pl_rade"] <= 1.6

print("Final HZ categories:")
print(df["final_hz_category"].value_counts())

print("\nSmall-planet candidates by category:")
print(
    df[df["small_planet"]]
    ["final_hz_category"]
    .value_counts()
)

print("\nFinal small-planet candidate list:")

candidates = df[
    df["small_planet"] &
    df["final_hz_category"].isin([
        "Conservative HZ",
        "Optimistic-only HZ"
    ])
]

print(
    candidates[[
        "pl_name",
        "hostname",
        "pl_rade",
        "pl_orbsmax",
        "final_hz_category"
    ]].sort_values(
        ["final_hz_category", "pl_rade"]
    ).to_string(index=False)
)

df.to_csv("final_exoplanet_screening.csv", index=False)

print("\nSaved: final_exoplanet_screening.csv")
