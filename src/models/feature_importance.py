import pandas as pd
import matplotlib.pyplot as plt
import shap
import os

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

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

imputer = SimpleImputer(strategy="median")
X_train_clean = pd.DataFrame(
    imputer.fit_transform(X_train),
    columns=features
)
X_test_clean = pd.DataFrame(
    imputer.transform(X_test),
    columns=features
)

model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_clean, y_train)

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X_test_clean)

# Select the positive class (class 1)
if isinstance(shap_values, list):
    shap_values = shap_values[1]
elif len(shap_values.shape) == 3:
    shap_values = shap_values[:, :, 1]

print("SHAP values shape:", shap_values.shape)

shap.summary_plot(
    shap_values,
    X_test_clean,
    show=False
)

save_path = os.path.join(os.getcwd(), "shap_summary.png")

importance = pd.DataFrame({
    "Feature": features,
    "Mean_SHAP_Importance": abs(shap_values).mean(axis=0)
})

importance = importance.sort_values(
    by="Mean_SHAP_Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE RANKING")
print(importance.to_string(index=False))

importance.to_csv("feature_importance.csv", index=False)

plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()

print("SHAP plot saved:", save_path)

