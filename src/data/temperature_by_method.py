
import pandas as pd

df = pd.read_csv("exoplanets_with_luminosity.csv")

summary = (
    df.groupby("discoverymethod")["pl_eqt"]
    .agg(["count", "mean", "median", "min", "max"])
    .sort_values("count", ascending=False)
)

print("Equilibrium temperature by discovery method:")
print(summary.round(2))

print("\nNumber of planets below 50 K by discovery method:")

low_temp = df[df["pl_eqt"] < 50]

print(
    low_temp.groupby("discoverymethod")
    .size()
    .sort_values(ascending=False)
)
