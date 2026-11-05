import pandas as pd
from sklearn.model_selection import train_test_split

# Load labelled dataset
df = pd.read_csv("labelled_exoplanets.csv")

# Select features that were NOT used to create labels
features = [
    "pl_orbper",
    "pl_orbsmax",
    "pl_orbeccen",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_met",
    "st_logg"
]

X = df[features]
y = df["potentially_habitable"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

print("\nTraining label distribution:")
print(y_train.value_counts())

print("\nTesting label distribution:")
print(y_test.value_counts())

print("\nData preparation completed!")