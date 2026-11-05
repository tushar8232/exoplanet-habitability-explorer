
import pandas as pd

df = pd.read_csv("final_candidate_summary.csv")

print("DATASET VALIDATION")
print("------------------")

# 1. Check total records
print("Total records:", len(df))

# 2. Check duplicate planet names
print("Duplicate planet names:", df["pl_name"].duplicated().sum())

# 3. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 4. Count small-radius candidates
small = df[df["pl_rade"] <= 1.6]

print("\nPlanets with radius <= 1.6 Earth radii:")
print(len(small))

print("\nSmall-radius candidates by category:")
print(small["final_hz_category"].value_counts())

# 5. Check radius range
print("\nPlanet radius statistics:")
print(df["pl_rade"].describe())

# 6. Save small-radius candidates
small.to_csv("small_radius_hz_candidates.csv", index=False)

print("\nSaved: small_radius_hz_candidates.csv")
