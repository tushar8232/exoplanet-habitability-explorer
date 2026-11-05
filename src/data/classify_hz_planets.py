
import pandas as pd
import numpy as np

df = pd.read_csv("exoplanets_with_hz.csv")

conditions = [
    df["pl_orbsmax"] < df["hz_inner_au"],
    (df["pl_orbsmax"] >= df["hz_inner_au"]) &
    (df["pl_orbsmax"] <= df["hz_outer_au"]),
    df["pl_orbsmax"] > df["hz_outer_au"]
]

choices = [
    "Inside inner boundary",
    "Within estimated HZ",
    "Outside outer boundary"
]

df["hz_position"] = np.select(
    conditions,
    choices,
    default="Insufficient data"
)

print("HZ classification counts:")
print(df["hz_position"].value_counts())

print("\nExample planets within estimated HZ:")

print(
    df[df["hz_position"] == "Within estimated HZ"][
        ["pl_name", "pl_rade", "pl_orbsmax",
         "hz_inner_au", "hz_outer_au"]
    ].head(15).round(4).to_string(index=False)
)

df.to_csv("exoplanets_hz_classified.csv", index=False)

print("\nSaved: exoplanets_hz_classified.csv")
