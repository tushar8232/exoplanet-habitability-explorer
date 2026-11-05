
import pandas as pd

df = pd.read_csv("expanded_exoplanet_features.csv")

# Solar effective temperature in Kelvin
SUN_TEMPERATURE = 5772

# Calculate luminosity relative to the Sun
df["st_luminosity"] = (
    df["st_rad"] ** 2
    * (df["st_teff"] / SUN_TEMPERATURE) ** 4
)

# Invalid or unavailable measurements remain missing
df.loc[
    (df["st_rad"] <= 0) | (df["st_teff"] <= 0),
    "st_luminosity"
] = float("nan")

print("Luminosity calculation complete!")
print("Available luminosity values:", df["st_luminosity"].notna().sum())
print("Missing luminosity values:", df["st_luminosity"].isna().sum())

print("\nSample results:")
print(df[["hostname", "st_rad", "st_teff", "st_luminosity"]].head(10))

df.to_csv("exoplanets_with_luminosity.csv", index=False)

print("\nSaved: exoplanets_with_luminosity.csv")
