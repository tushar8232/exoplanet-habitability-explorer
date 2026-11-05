import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("labelled_exoplanets.csv")

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
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Handle class imbalance
negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", XGBClassifier(
        n_estimators=100,
        max_depth=2,
        learning_rate=0.05,
        scale_pos_weight=negative / positive,
        eval_metric="logloss",
        random_state=42
    ))
])

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("XGBoost Classification Report:")
print(classification_report(
    y_test, y_pred, zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nXGBoost training completed!")