import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score
)

df = pd.read_csv("labelled_exoplanets.csv")

features = [
    "pl_orbper", "pl_orbsmax", "pl_orbeccen",
    "st_teff", "st_rad", "st_mass", "st_met", "st_logg"
]

X = df[features]
y = df["potentially_habitable"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=2,
        learning_rate=0.05,
        scale_pos_weight=negative / positive,
        eval_metric="logloss",
        random_state=42
    )
}

results = []

for name, classifier in models.items():
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", classifier)
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    results.append({
        "Model": name,
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1 Score": f1_score(y_test, predictions, zero_division=0),
        "Balanced Accuracy": balanced_accuracy_score(y_test, predictions)
    })

comparison = pd.DataFrame(results)

print("\nMODEL COMPARISON")
print(comparison.to_string(index=False))