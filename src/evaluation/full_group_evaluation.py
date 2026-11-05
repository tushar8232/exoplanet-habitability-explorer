import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score
)

df = pd.read_csv("labelled_exoplanets.csv")

features = [
    "pl_orbper", "pl_orbsmax", "pl_orbeccen",
    "st_teff", "st_rad", "st_mass", "st_met", "st_logg"
]

X = df[features]
y = df["potentially_habitable"]
groups = df["hostname"]

cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

all_predictions = pd.Series(index=y.index, dtype="int64")

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups), start=1
):

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]

    train_hosts = set(groups.iloc[train_idx])
    test_hosts = set(groups.iloc[test_idx])

    print(f"\nFold {fold}")
    print("Host overlap:", len(train_hosts & test_hosts))
    print("Training positives:", int(y_train.sum()))
    print("Testing positives:", int(y.iloc[test_idx].sum()))

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    all_predictions.iloc[test_idx] = model.predict(X_test)

print("\nFINAL FIVE-FOLD GROUP EVALUATION")

print(classification_report(
    y,
    all_predictions,
    zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(y, all_predictions))

print(
    "Balanced Accuracy:",
    balanced_accuracy_score(y, all_predictions)
)