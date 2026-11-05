
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_kopparapu_hz.csv")

inner = df["hz_runaway_greenhouse_au"]
outer = df["hz_maximum_greenhouse_au"]
orbit = df["pl_orbsmax"]

conditions = [
    orbit < inner,
    (orbit >= inner) & (orbit <= outer),
    orbit > outer
]

choices = [
    "Inside conservative HZ",
    "Within conservative HZ",
    "Outside conservative HZ"
]

df["kopparapu_position"] = np.select(
    conditions,
    choices,
    default="Insufficient data"
)

print("Kopparapu classification:")
print(df["kopparapu_position"].value_counts())

print("\nSmall planets within conservative HZ:")

candidates = df[
    (df["kopparapu_position"] == "Within conservative HZ") &
    (df["pl_rade"] <= 1.6)
]

print("Candidate count:", len(candidates))

print(
    candidates[[
        "pl_name",
        "pl_rade",
        "pl_orbsmax",
        "hz_runaway_greenhouse_au",
        "hz_maximum_greenhouse_au"
    ]].to_string(index=False)
)

df.to_csv("exoplanets_kopparapu_classified.csv", index=False)

print("\nSaved: exoplanets_kopparapu_classified.csv")
