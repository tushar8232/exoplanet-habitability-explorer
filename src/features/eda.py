import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cleaned_exoplanets.csv")

# 1. Planet radius distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["pl_rade"], bins=40, kde=True)
plt.title("Distribution of Exoplanet Radius")
plt.xlabel("Planet Radius (Earth Radii)")
plt.savefig("planet_radius.png")
plt.show()

# 2. Equilibrium temperature distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["pl_eqt"], bins=40, kde=True)
plt.title("Distribution of Equilibrium Temperature")
plt.xlabel("Temperature (Kelvin)")
plt.savefig("planet_temperature.png")
plt.show()

# 3. Planet radius vs temperature
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="pl_rade", y="pl_eqt", alpha=0.5)
plt.title("Planet Radius vs Equilibrium Temperature")
plt.savefig("radius_vs_temperature.png")
plt.show()

print("EDA completed!")