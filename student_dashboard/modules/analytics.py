import pandas as pd
from sklearn.cluster import KMeans

def total_marks(df):
    return df.groupby("student_id")["marks"].sum().reset_index(name="total")

def average_marks(df):
    return df.groupby("student_id")["marks"].mean().reset_index(name="avg")

def calculate_rank(df):
    total = total_marks(df)
    total["rank"] = total["total"].rank(ascending=False, method="dense")
    return total.sort_values("rank")

def student_growth(df):
    growth = []

    for sid, group in df.groupby("student_id"):
        marks = group["marks"].values
        if len(marks) > 1:
            change = marks[-1] - marks[0]
        else:
            change = 0
        growth.append((sid, change))

    return pd.DataFrame(growth, columns=["student_id", "growth"])

def pass_fail_rate(df):
    df = df.copy()

    df["result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

    summary = df["result"].value_counts().reset_index()
    summary.columns = ["Result", "Count"]

    total = summary["Count"].sum()
    summary["Percentage"] = (summary["Count"] / total) * 100

    return summary

def detect_outliers(df):
    mean = df["marks"].mean()
    std = df["marks"].std()

    df["outlier"] = df["marks"].apply(
        lambda x: "Yes" if abs(x - mean) > 2 * std else "No"
    )
    return df

def student_segmentation(df):
    features = df.groupby("student_id")["marks"].agg(["mean", "sum"]).reset_index()

    kmeans = KMeans(n_clusters=3, random_state=42)
    features["cluster"] = kmeans.fit_predict(features[["mean", "sum"]])

    return features

def subject_difficulty_index(df):
    difficulty = df.groupby("subject")["marks"].mean().reset_index()
    difficulty["difficulty"] = difficulty["marks"].apply(
        lambda x: "Hard" if x < 50 else ("Medium" if x < 70 else "Easy")
    )
    return difficulty

def top_performers(df, top_n=10):
    total = total_marks(df)
    top = total.sort_values("total", ascending=False).head(top_n)
    return top.merge(df[["student_id", "marks"]], on="student_id", how="left").drop_duplicates("student_id")        

def class_level_analysis(df):
    analysis = df.groupby("student_id")["marks"].agg(["mean", "sum", "count"]).reset_index()
    analysis.columns = ["student_id", "avg_marks", "total_marks", "num_subjects"]
    return analysis

def behavioral_analysis(df):
    behavior = df.groupby("student_id")["marks"].agg(["mean", "std"]).reset_index()
    behavior.columns = ["student_id", "avg_marks", "std_dev"]
    return behavior
