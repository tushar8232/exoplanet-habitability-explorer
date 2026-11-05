import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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

train_idx, test_idx = next(cv.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

train_hosts = set(groups.iloc[train_idx])
test_hosts = set(groups.iloc[test_idx])

print("Host overlap:", len(train_hosts.intersection(test_hosts)))
print("Training positives:", int(y_train.sum()))
print("Testing positives:", int(y_test.sum()))

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    ))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nGROUP-AWARE CLASSIFICATION REPORT")
print(classification_report(y_test, predictions, zero_division=0))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

train_idx, test_idx = next(cv.split(X, y, groups))