# 🏏 2022 ICC Men's T20 World Cup Analytics: End-to-End BI & Data Engineering Project

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-150458.svg)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20Postgres-CC292B.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-DAX-F2C811.svg)](https://powerbi.microsoft.com/)

An end-to-end data analytics and business intelligence project evaluating player performance, match strategies, and team dynamics during the **2022 ICC Men's T20 World Cup** held in Australia.

---

## 📌 1. Project Overview & Business Value
T20 cricket is won in the margins—boundary percentages, dot ball rates, and phase-specific strike rates. This project converts disparate raw match data into a structured relational **Star Schema**, applies complex **SQL window functions and CTEs** to extract actionable metrics, and structures dynamic **Power BI DAX measures** to assemble a mathematically optimized **"World Cup Best XI"**.

---

## 🏗️ 2. Repository Architecture

```
t20-world-cup-analytics/
├── data/
│   ├── raw/                           # Raw match scorecards & player telemetry
│   │   ├── matches_raw.csv
│   │   ├── players_raw.csv
│   │   ├── batting_raw.csv
│   │   └── bowling_raw.csv
│   └── processed/                     # Star-schema cleaned CSV datasets
│       ├── dim_matches.csv
│       ├── dim_players.csv
│       ├── fact_batting_summary.csv
│       └── fact_bowling_summary.csv
├── sql/
│   ├── schema.sql                     # DDL table schemas, primary & foreign keys, indexes
│   ├── analysis_queries.sql           # CTEs, Window functions, rankings & Best XI queries
│   └── execute_queries.py             # SQLite query execution and tabular reporter
├── powerbi/
│   ├── dax_measures.md                # Full DAX code repository for calculated measures
│   └── dashboard_spec.md              # 4-page Power BI dashboard design specification
├── src/
│   ├── generate_raw_data.py           # Synthetic raw dataset generator (based on real 2022 stats)
│   ├── clean_data.py                  # ETL pipeline (Overs-to-balls, boundary %, null handling)
│   ├── eda_analysis.py                # Exploratory Data Analysis script
│   └── db_loader.py                   # Loads processed CSVs into SQLite database
├── cricket_world_cup.db               # Auto-generated SQLite relational database
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation and interview guide
```

---

## ⚙️ 3. Quickstart & How to Run

### Step 1: Navigate to Project Directory
```powershell
cd t20-world-cup-analytics
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Complete Data Pipeline
```powershell
# 1. Generate & clean raw datasets into Star-Schema tables
python src/generate_raw_data.py
python src/clean_data.py

# 2. Run Exploratory Data Analysis
python src/eda_analysis.py

# 3. Create relational database and load tables
python src/db_loader.py

# 4. Execute analytical SQL queries
python sql/execute_queries.py
```

---

## 📊 4. Data Cleaning & Feature Engineering Highlights (`clean_data.py`)

1. **Fractional Overs to Legal Balls Bowled:**
   * In cricket notation, `3.4` overs means 3 completed overs plus 4 balls ($3 \times 6 + 4 = 22$ balls). If analyzed as decimals, standard division yields mathematical errors ($0.4 \ne 4/6$).
   * Created custom function `parse_overs_to_balls()` to accurately calculate **True Economy Rate** ($Runs / Balls \times 6$).
2. **Dismissal Parsing:**
   * Derived binary `is_out` flags by cleaning string literals like `"not out"`, `"dnb"`, and `"run out"`, ensuring accurate Batting Average calculations ($Runs / Total Dismissals$).
3. **Boundary Run Contribution:**
   * Extracted `boundary_runs = (4s * 4) + (6s * 6)` and engineered `boundary_pct` to isolate boundary hitters from strike rotators.

---

## 🔍 5. Advanced SQL Analytics Showcase (`sql/analysis_queries.sql`)

### Highlight 1: Leaderboard with `DENSE_RANK()`
```sql
WITH batting_stats AS (
    SELECT 
        b.player_id, p.name AS player_name, p.team,
        SUM(b.runs) AS total_runs,
        SUM(b.balls) AS total_balls,
        SUM(b.is_out) AS times_out,
        SUM(b.boundary_runs) AS boundary_runs
    FROM fact_batting_summary b
    JOIN dim_players p ON b.player_id = p.player_id
    GROUP BY b.player_id, p.name, p.team
)
SELECT 
    player_name, team, total_runs,
    ROUND((total_runs * 100.0 / NULLIF(total_balls, 0)), 2) AS strike_rate,
    ROUND((total_runs * 1.0 / NULLIF(times_out, 0)), 2) AS batting_average,
    ROUND((boundary_runs * 100.0 / NULLIF(total_runs, 0)), 2) AS boundary_pct,
    DENSE_RANK() OVER (ORDER BY total_runs DESC) AS run_rank,
    DENSE_RANK() OVER (ORDER BY (total_runs * 100.0 / NULLIF(total_balls, 0)) DESC) AS sr_rank
FROM batting_stats
WHERE total_runs >= 100;
```

### Highlight 2: Bowling Impact Index
Combines wicket-taking threat with boundary denial:
```sql
SELECT 
    p.name AS bowler_name,
    p.team,
    SUM(bw.wickets) AS total_wickets,
    ROUND((SUM(bw.runs_conceded) * 6.0 / SUM(bw.balls_bowled)), 2) AS economy_rate,
    ROUND((SUM(bw.dot_balls) * 100.0 / SUM(bw.balls_bowled)), 2) AS dot_ball_pct,
    DENSE_RANK() OVER (ORDER BY SUM(bw.wickets) DESC, (SUM(bw.runs_conceded) * 6.0 / SUM(bw.balls_bowled)) ASC) AS rank
FROM fact_bowling_summary bw
JOIN dim_players p ON bw.player_id = p.player_id
GROUP BY bw.player_id, p.name, p.team
HAVING SUM(bw.balls_bowled) >= 48;
```

---

## 📈 6. Power BI Modeling & DAX Measures

### Star Schema Architecture:
* **Dimensions:** `dim_players`, `dim_matches`
* **Facts:** `fact_batting_summary`, `fact_bowling_summary`
* **Cardinality:** 1-to-many, single direction filtering.

### Key DAX Measures (`powerbi/dax_measures.md`):
* **Batting Strike Rate:**
  ```dax
  Batting Strike Rate = DIVIDE(SUM(fact_batting_summary[runs]), SUM(fact_batting_summary[balls]), 0) * 100
  ```
* **Bowling Economy Rate:**
  ```dax
  Bowling Economy Rate = DIVIDE(SUM(fact_bowling_summary[runs_conceded]), DIVIDE(SUM(fact_bowling_summary[balls_bowled]), 6, 0), 0)
  ```
* **Dot Ball %:**
  ```dax
  Dot Ball % = DIVIDE(SUM(fact_bowling_summary[dot_balls]), SUM(fact_bowling_summary[balls_bowled]), 0) * 100
  ```

---

## 🏆 7. Final Selected "World Cup Best XI"

Based strictly on mathematical optimization rules (Boundary % > 50%, Econ < 7.5, Dot % > 45%):

| Pos | Player | Team | Role | Primary Metric |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Jos Buttler (C/WK)** | England | Opener / Keeper | 225 Runs, SR 144.23 |
| **2** | **Alex Hales** | England | Explosive Opener | 205 Runs, SR 147.48, Boundary 63.4% |
| **3** | **Virat Kohli** | India | Anchor | 296 Runs, Avg 98.67, Top Scorer |
| **4** | **Suryakumar Yadav**| India | 360° Finisher | 239 Runs, SR 189.68 |
| **5** | **Glenn Phillips** | New Zealand | Middle Order | 178 Runs, SR 161.82, 1 Century |
| **6** | **Shadab Khan** | Pakistan | Spin Allrounder | 8 Wickets (Econ 6.11) + 52 Runs (SR 236.4) |
| **7** | **Sam Curran (POTS)**| England | Death Allrounder | 13 Wickets, Econ 6.53, POTS |
| **8** | **Wanindu Hasaranga**| Sri Lanka | Lead Leg-Spinner| 15 Wickets, Dot % 48% |
| **9** | **Shaheen Afridi** | Pakistan | Left-Arm Pacer | 10 Wickets, Econ 6.43 |
| **10**| **Anrich Nortje** | South Africa| Express Pacer | 10 Wickets, Econ 5.42, Dot % 59.1% |
| **11**| **Arshdeep Singh** | India | Death Specialist| 10 Wickets, SR 12.60 |

---

