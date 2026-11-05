import pandas as pd

df = pd.read_csv("exoplanets.csv", comment="#")

new_columns = [
    "pl_name",
    "hostname",
    "discoverymethod",
    "disc_facility",
    "disc_year",

    # Planetary parameters
    "pl_rade",
    "pl_eqt",
    "pl_insol",
    "pl_orbper",
    "pl_orbsmax",
    "pl_orbeccen",

    # Stellar parameters
    "st_teff",
    "st_rad",
    "st_mass",
    "st_lum",
    "st_met",
    "st_logg"
]

available_columns = [
    col for col in new_columns if col in df.columns
]

expanded_df = df[available_columns].copy()

print("Expanded dataset shape:", expanded_df.shape)

print("\nAvailable features:")
print(expanded_df.columns.tolist())

print("\nMissing values:")
print(expanded_df.isnull().sum())

expanded_df.to_csv(
    "expanded_exoplanet_features.csv",
    index=False
)

print("\nExpanded dataset saved!")