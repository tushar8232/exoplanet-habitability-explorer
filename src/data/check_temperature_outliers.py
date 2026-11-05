
import pandas as pd

df = pd.read_csv("exoplanets_with_luminosity.csv")

print("Temperatures below 50 K:")
low = df[df["pl_eqt"] < 50]

print("Count:", len(low))

columns = [
    "pl_name",
    "pl_eqt",
    "pl_insol",
    "pl_orbsmax",
    "st_teff",
    "st_rad",
    "discoverymethod"
]

print(low[columns].sort_values("pl_eqt").to_string(index=False))

print("\nInvalid or non-positive temperatures:")
print((df["pl_eqt"] <= 0).sum())

print("\nTemperature distribution:")
print("Below 100 K:", (df["pl_eqt"] < 100).sum())
print("Below 200 K:", (df["pl_eqt"] < 200).sum())
