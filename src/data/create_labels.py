import pandas as pd

# Load selected dataset (before median imputation)
df = pd.read_csv("selected_exoplanet_features.csv")

# Keep planets with actual radius and insolation measurements
df = df.dropna(subset=["pl_rade", "pl_insol"]).copy()

# Define potential habitability screening label
df["potentially_habitable"] = (
    (df["pl_rade"] <= 1.6) &
    (df["pl_insol"] >= 0.35) &
    (df["pl_insol"] <= 1.5)
).astype(int)

# Display label distribution
print("Habitability Label Distribution:")
print(df["potentially_habitable"].value_counts())

print("\nLabel percentages:")
print(df["potentially_habitable"].value_counts(normalize=True) * 100)

# Save labelled dataset
df.to_csv("labelled_exoplanets.csv", index=False)

print("\nLabelled dataset shape:", df.shape)
print("\nHabitability labels created successfully!")