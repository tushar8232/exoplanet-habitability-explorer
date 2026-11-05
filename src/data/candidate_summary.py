
import pandas as pd

df = pd.read_csv("final_exoplanet_screening.csv")

# Keep planets with measured radius and known HZ classification
candidates = df[
    df["pl_rade"].notna()
    & df["final_hz_category"].isin([
        "Conservative HZ",
        "Optimistic-only HZ"
    ])
].copy()

# Select useful columns
summary = candidates[[
    "pl_name",
    "hostname",
    "discoverymethod",
    "disc_year",
    "pl_rade",
    "pl_eqt",
    "pl_insol",
    "pl_orbsmax",
    "st_teff",
    "st_luminosity",
    "final_hz_category"
]].copy()

summary = summary.sort_values(
    ["final_hz_category", "pl_rade"]
)

print("Total candidates:", len(summary))

print("\nCandidates by category:")
print(summary["final_hz_category"].value_counts())

print("\nPreview:")
print(summary.head(10).to_string(index=False))

summary.to_csv("final_candidate_summary.csv", index=False)

print("\nSaved: final_candidate_summary.csv")
