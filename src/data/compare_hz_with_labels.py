
import pandas as pd

hz = pd.read_csv("exoplanets_hz_classified.csv")
labels = pd.read_csv("labelled_exoplanets.csv")

# Keep the original target labels
comparison = hz.merge(
    labels[["pl_name", "potentially_habitable"]],
    on="pl_name",
    how="inner"
)

# Recreate the HZ + small-radius screening result
comparison["hz_candidate"] = (
    (comparison["hz_position"] == "Within estimated HZ") &
    (comparison["pl_rade"] <= 1.6)
)

print("Planets compared:", len(comparison))

print("\nOriginal label counts:")
print(comparison["potentially_habitable"].value_counts())

print("\nHZ candidate counts:")
print(comparison["hz_candidate"].value_counts())

print("\nComparison table:")
print(
    pd.crosstab(
        comparison["potentially_habitable"],
        comparison["hz_candidate"],
        rownames=["Original label"],
        colnames=["HZ candidate"]
    )
)

print("\nDisagreement cases:")

disagreements = comparison[
    comparison["potentially_habitable"] !=
    comparison["hz_candidate"]
]

print("Number of disagreements:", len(disagreements))

print(
    disagreements[[
        "pl_name",
        "pl_rade",
        "pl_insol",
        "pl_orbsmax",
        "st_luminosity",
        "hz_position",
        "potentially_habitable",
        "hz_candidate"
    ]].to_string(index=False)
)

comparison.to_csv("hz_label_comparison.csv", index=False)

print("\nSaved: hz_label_comparison.csv")
