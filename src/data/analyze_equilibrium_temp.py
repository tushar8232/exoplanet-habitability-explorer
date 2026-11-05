
import pandas as pd

df = pd.read_csv("exoplanets_with_luminosity.csv")

print("Total planets:", len(df))
print("Available equilibrium temperatures:", df["pl_eqt"].notna().sum())
print("Missing equilibrium temperatures:", df["pl_eqt"].isna().sum())

print("\nTemperature statistics (Kelvin):")
print(df["pl_eqt"].describe())

print("\nFive planets with the lowest equilibrium temperatures:")
print(
    df[["pl_name", "pl_eqt"]]
    .dropna()
    .sort_values("pl_eqt")
    .head(5)
)

print("\nFive planets with the highest equilibrium temperatures:")
print(
    df[["pl_name", "pl_eqt"]]
    .dropna()
    .sort_values("pl_eqt", ascending=False)
    .head(5)
)
