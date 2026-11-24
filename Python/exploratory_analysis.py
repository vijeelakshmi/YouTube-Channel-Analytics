"""
YouTube Channel Analytics - Exploratory Data Analysis
Input : ../Dataset/cleaned_youtube_videos.csv
Output: ../Documentation/eda_summary.csv
        ../Documentation/charts/*.png

Run:
    python exploratory_analysis.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = PROJECT_DIR / "Dataset" / "cleaned_youtube_videos.csv"
OUTPUT_DIR = PROJECT_DIR / "Documentation"
CHART_DIR = OUTPUT_DIR / "charts"


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close()


def main():
    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {DATASET_FILE}\n"
            "Run data_cleaning.py first."
        )

    df = pd.read_csv(DATASET_FILE, parse_dates=["Published_Date"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    # Overall KPI summary.
    total_videos = df["Video_ID"].nunique()
    total_views = df["Views"].sum()
    total_likes = df["Likes"].sum()
    total_comments = df["Comments"].sum()
    avg_views = df["Views"].mean()
    overall_engagement = (
        (total_likes + total_comments) / total_views * 100 if total_views else 0
    )

    summary = pd.DataFrame({
        "Metric": [
            "Unique Videos", "Total Views", "Total Likes", "Total Comments",
            "Average Views per Video", "Overall Engagement Rate (%)"
        ],
        "Value": [
            total_videos, total_views, total_likes, total_comments,
            round(avg_views, 2), round(overall_engagement, 2)
        ]
    })
    summary.to_csv(OUTPUT_DIR / "eda_summary.csv", index=False)

    # Missing values and distribution summaries.
    missing = df.isna().sum().rename("Missing_Count").reset_index()
    missing.columns = ["Column", "Missing_Count"]
    missing.to_csv(OUTPUT_DIR / "missing_values_summary.csv", index=False)

    numeric_cols = ["Duration_Minutes", "Views", "Likes", "Comments", "Subscribers", "Engagement_Rate"]
    df[numeric_cols].describe().T.to_csv(OUTPUT_DIR / "numeric_distribution_summary.csv")

    # Monthly trend.
    monthly = (
        df.groupby("Published_Year_Month", as_index=False)
          .agg(Views=("Views", "sum"), Videos=("Video_ID", "nunique"),
               Likes=("Likes", "sum"), Comments=("Comments", "sum"))
          .sort_values("Published_Year_Month")
    )
    monthly.to_csv(OUTPUT_DIR / "monthly_performance.csv", index=False)

    plt.figure(figsize=(12, 5))
    plt.plot(monthly["Published_Year_Month"], monthly["Views"], marker="o")
    plt.title("Monthly YouTube Views")
    plt.xlabel("Month")
    plt.ylabel("Views")
    plt.xticks(rotation=60, ha="right")
    save_chart("monthly_views_trend.png")

    # Category comparison.
    category = (
        df.groupby("Category", as_index=False)
          .agg(Views=("Views", "sum"), Likes=("Likes", "sum"),
               Comments=("Comments", "sum"), Videos=("Video_ID", "nunique"))
    )
    category["Engagement_Rate"] = (
        (category["Likes"] + category["Comments"]) /
        category["Views"].replace(0, pd.NA) * 100
    ).fillna(0)
    category.to_csv(OUTPUT_DIR / "category_performance.csv", index=False)

    category_sorted = category.sort_values("Views", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(category_sorted["Category"], category_sorted["Views"])
    plt.title("Total Views by Category")
    plt.xlabel("Views")
    save_chart("views_by_category.png")

    # Top 10 videos by views.
    top10 = df.nlargest(10, "Views")[
        ["Video_ID", "Video_Title", "Channel_Name", "Category", "Views", "Likes", "Comments", "Engagement_Rate"]
    ]
    top10.to_csv(OUTPUT_DIR / "top_10_videos.csv", index=False)

    plt.figure(figsize=(10, 6))
    plot_data = top10.sort_values("Views", ascending=True)
    plt.barh(plot_data["Video_Title"], plot_data["Views"])
    plt.title("Top 10 Videos by Views")
    plt.xlabel("Views")
    save_chart("top_10_videos.png")

    # Publishing hour comparison.
    hourly = (
        df.groupby("Published_Hour", as_index=False)
          .agg(Views=("Views", "sum"), Video_Count=("Video_ID", "nunique"))
    )
    hourly["Average_Views_Per_Video"] = hourly["Views"] / hourly["Video_Count"].replace(0, 1)
    hourly.to_csv(OUTPUT_DIR / "publishing_hour_performance.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.bar(hourly["Published_Hour"], hourly["Average_Views_Per_Video"])
    plt.title("Average Views per Video by Publishing Hour")
    plt.xlabel("Publishing Hour (24-hour clock)")
    plt.ylabel("Average Views per Video")
    plt.xticks(range(0, 24))
    save_chart("views_by_publishing_hour.png")

    # Duration bands and engagement comparison.
    bins = [0, 3, 8, 15, 30, 60, float("inf")]
    labels = ["0-3 min", "3-8 min", "8-15 min", "15-30 min", "30-60 min", "60+ min"]
    df["Duration_Band"] = pd.cut(df["Duration_Minutes"], bins=bins, labels=labels, right=False)
    duration = (
        df.groupby("Duration_Band", observed=False, as_index=False)
          .agg(Video_Count=("Video_ID", "nunique"),
               Avg_Views=("Views", "mean"),
               Avg_Engagement_Rate=("Engagement_Rate", "mean"))
    )
    duration.to_csv(OUTPUT_DIR / "duration_analysis.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.bar(duration["Duration_Band"].astype(str), duration["Avg_Engagement_Rate"])
    plt.title("Average Engagement Rate by Video Duration")
    plt.xlabel("Video Duration")
    plt.ylabel("Average Engagement Rate (%)")
    save_chart("engagement_by_duration.png")

    print("EDA complete.")
    print(f"Summary tables and charts saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
