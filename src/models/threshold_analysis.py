import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score

from xgboost import XGBClassifier

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

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)[:, 1]

for threshold in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    predictions = (probabilities >= threshold).astype(int)

    print(f"\nThreshold: {threshold}")
    print("Precision:", round(
        precision_score(y_test, predictions, zero_division=0), 3
    ))
    print("Recall:", round(
        recall_score(y_test, predictions, zero_division=0), 3
    ))
    print("F1 Score:", round(
        f1_score(y_test, predictions, zero_division=0), 3
    ))