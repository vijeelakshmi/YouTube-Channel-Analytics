# YouTube Channel Analytics

An end-to-end analytics portfolio project exploring YouTube video performance, audience engagement, publishing patterns, and content performance using Python, SQL, and Power BI.

**Business question:** What drives engagement on YouTube videos?

## Tools
- Python (Pandas, NumPy, Matplotlib) — cleaning and exploratory analysis
- SQL — KPI calculations, comparisons, trends, and data-quality checks
- Power BI / DAX — interactive dashboard and metrics
- CSV / Excel — data and validation

## Dataset
The practice dataset contains **12,000 simulated video records** with Video_ID, Channel_Name, Video_Title, Category, Subcategory, Published_Date, Published_Time, Published_Hour, Duration_Minutes, Views, Likes, Comments, and Subscribers.

> **Data provenance:** This dataset is simulated for practice. It was not collected from YouTube or the YouTube API. Do not present the results as actual channel performance.

## Workflow
1. Review and clean the raw dataset.
2. Use Python to standardize fields, convert types, remove duplicate video IDs, validate numeric ranges, handle missing metrics, and create analysis fields.
3. Explore distributions, missingness, category performance, monthly trends, publishing times, duration, and top videos.
4. Use SQL to calculate KPIs, compare segments, rank videos, analyze trends, and check data quality.
5. Build an interactive Power BI report.
6. Quantify findings and recommend actions supported by the dataset.

## Dashboard Pages

### 1. Executive Overview
- Total Views, Total Likes, Average Views per Video, Engagement Rate, Total Videos
- Monthly Views Trend
- Category Performance
- Top 10 Videos by Views
- Key Insights panel
- Date, Category, Channel, and Segment slicers

### 2. Drivers & Segments
- Engagement by Category
- Engagement by Video Duration
- Views by Publishing Hour / Time Slot
- Likes vs. Views
- Category and Duration comparisons

### 3. Detailed Records & Exceptions
- Video-level details and performance metrics
- Engagement rate
- Data-quality checks and exceptions

## Key Metrics
- **Total Views:** Sum of views
- **Total Likes:** Sum of likes
- **Total Comments:** Sum of comments
- **Total Videos:** Distinct video IDs
- **Average Views per Video:** Total views / distinct videos
- **Engagement Rate:** (Likes + Comments) / Views
- **Like Rate:** Likes / Views
- **Comment Rate:** Comments / Views
- **Upload Cadence:** Videos published over time

## Python Scripts
- `data_cleaning.py`: text cleanup, type conversion, duplicate removal, range validation, missing metric handling, derived columns, cleaned dataset, and data-quality report.
- `exploratory_analysis.py`: KPI summary, missing-value and numeric summaries, monthly trend, category analysis, top 10 videos, publishing-hour analysis, and duration analysis.

## How to Run
1. Clone/download the repository.
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib
   ```
3. Put the raw CSV in `Dataset/youtube_channel_analytics_12000_rows.csv`.
4. Run cleaning:
   ```bash
   python Python/data_cleaning.py
   ```
   Outputs: `Dataset/cleaned_youtube_videos.csv` and `Documentation/data_quality_report.csv`.
5. Run EDA:
   ```bash
   python Python/exploratory_analysis.py
   ```
   Summary tables and charts are saved in `Documentation/`.
6. Open `PowerBI/youtube_analytics.pbix` in Power BI Desktop. Update the data source path if needed.

## Repository Structure
```text
YouTube-Channel-Analytics/
├── Dataset/
│   ├── youtube_videos.csv
│   └── cleaned_youtube_videos.csv
├── Python/
│   ├── data_cleaning.py
│   └── exploratory_analysis.py
├── SQL/
│   ├── create_tables.sql
│   └── analysis_queries.sql
├── PowerBI/
│   └── youtube_analytics.pbix
├── Dashboard_Images/
│   ├── overview.png
│   ├── drivers_segments.png
│   └── detailed_records.png
├── Documentation/
│   ├── data_dictionary.xlsx
│   ├── data_quality_report.csv
│   └── business_insights.pdf
└── README.md
```

## Business Questions
- Which categories generate the most views and engagement?
- Does video duration relate to engagement?
- Which publishing time slots perform best?
- Which videos are top and bottom performers?
- How does performance change month by month?
- Which content segments should the media team prioritize?

## Insights & Recommendations
Replace these placeholders with findings calculated from the dataset:
1. **Category:** `[Category]` leads `[metric]` with `[value]` versus `[benchmark]`.
2. **Duration:** `[Duration group]` has the highest average engagement rate of `[value]`.
3. **Publishing time:** `[Time slot]` produces `[value]` average views per video.

Recommendations should be supported by measured results. Patterns are hypotheses to test, not proof of causation.

## Limitations
- The data is simulated and does not represent real YouTube channel activity.
- Watch time, impressions, click-through rate, retention, and traffic sources are not included.
- Performance may be affected by factors not captured in the dataset.
- Correlations do not establish causation.

## Portfolio Deliverables
Cleaned dataset, Python scripts, SQL files, Power BI report, screenshots, data dictionary, and business insights report.

## Author
**Vijayalakshmi R** — Data Analytics Portfolio Project
