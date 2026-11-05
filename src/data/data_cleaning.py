import pandas as pd

# Load selected dataset
df = pd.read_csv("selected_exoplanet_features.csv")

# Check missing values
print("Missing values before cleaning:")
print(df.isnull().sum())

# Check total missing values
print("\nTotal missing values:")
print(df.isnull().sum().sum())

# Remove rows with missing planet radius
df = df.dropna(subset=["pl_rade"])

# Fill missing numerical values with median
numerical_columns = df.select_dtypes(include=["number"]).columns

for column in numerical_columns:
    df[column] = df[column].fillna(df[column].median())

# Save cleaned dataset
df.to_csv("cleaned_exoplanets.csv", index=False)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset shape:")
print(df.shape)

print("\nData cleaning completed!")