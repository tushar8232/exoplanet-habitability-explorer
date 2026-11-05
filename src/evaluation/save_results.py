import pandas as pd

results = {
    "Metric": [
        "Total Planets",
        "Positive Examples",
        "True Positives",
        "False Positives",
        "False Negatives",
        "Precision",
        "Recall",
        "F1 Score",
        "Balanced Accuracy"
    ],

    "Value": [
        5816,
        28,
        9,
        15,
        19,
        0.38,
        0.32,
        0.35,
        0.6594
    ]
}

df = pd.DataFrame(results)

df.to_csv("final_model_results.csv", index=False)

print("Final evaluation results saved!")
print(df)