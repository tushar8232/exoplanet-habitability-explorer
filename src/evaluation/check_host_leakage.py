import pandas as pd

from sklearn.model_selection import train_test_split

df = pd.read_csv("labelled_exoplanets.csv")

features = [
    "pl_orbper", "pl_orbsmax", "pl_orbeccen",
    "st_teff", "st_rad", "st_mass", "st_met", "st_logg"
]

X = df[features]
y = df["potentially_habitable"]
groups = df["hostname"]

X_train, X_test, y_train, y_test, groups_train, groups_test = (
    train_test_split(
        X, y, groups,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
)

train_hosts = set(groups_train)
test_hosts = set(groups_test)

overlap = train_hosts.intersection(test_hosts)

print("Unique training host stars:", len(train_hosts))
print("Unique testing host stars:", len(test_hosts))
print("Host stars appearing in both:", len(overlap))

print("\nPositive examples in training:", int(y_train.sum()))
print("Positive examples in testing:", int(y_test.sum()))