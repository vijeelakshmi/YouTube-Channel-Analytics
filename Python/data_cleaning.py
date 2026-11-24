
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_DIR / "Dataset"
INPUT_FILE = DATASET_DIR / "youtube_videos.csv"
OUTPUT_FILE = DATASET_DIR / "cleaned_youtube_videos.csv"
REPORT_DIR = PROJECT_DIR / "Documentation"
REPORT_FILE = REPORT_DIR / "data_quality_report.csv"

REQUIRED_COLUMNS = [
    "Video_ID", "Channel_Name", "Video_Title", "Category", "Subcategory",
    "Published_Date", "Published_Time", "Published_Hour",
    "Duration_Minutes", "Views", "Likes", "Comments", "Subscribers"
]
NUMERIC_COLUMNS = [
    "Published_Hour", "Duration_Minutes", "Views",
    "Likes", "Comments", "Subscribers"
]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}\n"
            "youtube_videos.csv"
        )

    df = pd.read_csv(INPUT_FILE)
    original_rows = len(df)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Standardize text fields.
    text_columns = ["Video_ID", "Channel_Name", "Video_Title", "Category", "Subcategory"]
    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    # Convert dates, times and numeric fields.
    df["Published_Date"] = pd.to_datetime(df["Published_Date"], errors="coerce")
    df["Published_Time"] = pd.to_datetime(
        df["Published_Time"], format="%H:%M:%S", errors="coerce"
    ).dt.time

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove duplicate video identifiers, keeping the first record.
    duplicate_ids = int(df["Video_ID"].duplicated(keep="first").sum())
    df = df.drop_duplicates(subset=["Video_ID"], keep="first").copy()

    # Drop records missing essential identifiers or publication date.
    before_required_drop = len(df)
    df = df.dropna(subset=["Video_ID", "Channel_Name", "Video_Title", "Published_Date"])
    dropped_required = before_required_drop - len(df)

    # Fill descriptive missing values.
    for col in ["Category", "Subcategory"]:
        df[col] = df[col].fillna("Unknown")

    # Validate numerical ranges; invalid values become null before row-level handling.
    invalid_counts = {}
    rules = {
        "Published_Hour": (0, 23),
        "Duration_Minutes": (0.01, 1440),
        "Views": (0, None),
        "Likes": (0, None),
        "Comments": (0, None),
        "Subscribers": (0, None),
    }
    for col, (lower, upper) in rules.items():
        invalid = df[col].notna() & (df[col] < lower)
        if upper is not None:
            invalid |= df[col].notna() & (df[col] > upper)
        invalid_counts[col] = int(invalid.sum())
        df.loc[invalid, col] = pd.NA

    # Views, likes, comments and subscribers are needed for the core KPIs.
    # Missing metric values are retained as zero and flagged in the report.
    metric_cols = ["Views", "Likes", "Comments", "Subscribers"]
    missing_metrics = {col: int(df[col].isna().sum()) for col in metric_cols}
    df[metric_cols] = df[metric_cols].fillna(0)

    # Likes and comments should not exceed views in this practice dataset.
    likes_gt_views = int((df["Likes"] > df["Views"]).sum())
    comments_gt_views = int((df["Comments"] > df["Views"]).sum())
    df["Likes"] = df[["Likes", "Views"]].min(axis=1)
    df["Comments"] = df[["Comments", "Views"]].min(axis=1)

    # Recalculate publishing hour from the time field where available.
    time_hour = pd.to_datetime(
        df["Published_Time"].astype("string"), format="%H:%M:%S", errors="coerce"
    ).dt.hour
    df["Published_Hour"] = time_hour.fillna(df["Published_Hour"])
    df["Published_Hour"] = df["Published_Hour"].fillna(0).astype("int64")

    # Add useful analysis columns.
    df["Published_Year"] = df["Published_Date"].dt.year
    df["Published_Month"] = df["Published_Date"].dt.month
    df["Published_Month_Name"] = df["Published_Date"].dt.strftime("%b")
    df["Published_Year_Month"] = df["Published_Date"].dt.strftime("%Y-%m")
    df["Engagements"] = df["Likes"] + df["Comments"]
    df["Engagement_Rate"] = (
        df["Engagements"].div(df["Views"].replace(0, pd.NA)).fillna(0) * 100
    ).round(2)

    # Consistent output ordering.
    df = df.sort_values("Published_Date").reset_index(drop=True)

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d", encoding="utf-8-sig")

    report_rows = [
        ("Original row count", original_rows),
        ("Cleaned row count", len(df)),
        ("Duplicate Video_ID records removed", duplicate_ids),
        ("Rows removed for missing required fields", dropped_required),
        ("Rows where Likes exceeded Views (capped)", likes_gt_views),
        ("Rows where Comments exceeded Views (capped)", comments_gt_views),
    ]
    report_rows.extend((f"Invalid values set to null - {k}", v) for k, v in invalid_counts.items())
    report_rows.extend((f"Missing metric values filled with zero - {k}", v)
                       for k, v in missing_metrics.items())
    pd.DataFrame(report_rows, columns=["Check", "Count"]).to_csv(
        REPORT_FILE, index=False, encoding="utf-8-sig"
    )

    print(f"Cleaning complete. {len(df):,} rows saved to:\n{OUTPUT_FILE}")
    print(f"Quality report saved to:\n{REPORT_FILE}")


if __name__ == "__main__":
    main()
