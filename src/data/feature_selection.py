import pandas as pd

# Load NASA dataset
df = pd.read_csv("exoplanets.csv", comment="#")

# Select scientifically relevant columns
selected_columns = [
    "pl_name",
    "hostname",
    "pl_rade",
    "pl_orbper",
    "pl_orbsmax",
    "pl_orbeccen",
    "pl_insol",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_met",
    "st_logg"
]

# Create selected dataset
selected_df = df[selected_columns]

# Display selected features
print("Selected Dataset Shape:")
print(selected_df.shape)

print("\nSelected Columns:")
print(selected_df.columns.tolist())

# Save selected dataset
selected_df.to_csv("selected_exoplanet_features.csv", index=False)

print("\nFeature selection completed!")
import os

print("File saved:", os.path.exists("selected_exoplanet_features.csv"))