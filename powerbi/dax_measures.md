# Power BI DAX Measures & Data Model Specification

## 1. Data Model Relationships (Star Schema)
Configure relationships in Power BI Model view:
* **`dim_players[player_id]`** (1) $\rightarrow$ **`fact_batting_summary[player_id]`** (*) (Single direction)
* **`dim_players[player_id]`** (1) $\rightarrow$ **`fact_bowling_summary[player_id]`** (*) (Single direction)
* **`dim_matches[match_id]`** (1) $\rightarrow$ **`fact_batting_summary[match_id]`** (*) (Single direction)
* **`dim_matches[match_id]`** (1) $\rightarrow$ **`fact_bowling_summary[match_id]`** (*) (Single direction)

---

## 2. DAX Measure Library

### 2.1 Core Batting Measures

#### Total Runs
```dax
Total Runs = SUM(fact_batting_summary[runs])
```

#### Balls Faced
```dax
Total Balls Faced = SUM(fact_batting_summary[balls])
```

#### Batting Strike Rate
```dax
Batting Strike Rate = 
DIVIDE(
    [Total Runs],
    [Total Balls Faced],
    0
) * 100
```

#### Batting Average
```dax
Batting Average = 
VAR TotalRuns = [Total Runs]
VAR TotalDismissals = SUM(fact_batting_summary[is_out])
RETURN
DIVIDE(TotalRuns, TotalDismissals, BLANK())
```

#### Boundary Runs
```dax
Boundary Runs = 
(SUM(fact_batting_summary[fours]) * 4) + (SUM(fact_batting_summary[sixes]) * 6)
```

#### Boundary Run %
```dax
Boundary Run % = 
DIVIDE(
    [Boundary Runs],
    [Total Runs],
    0
) * 100
```

---

### 2.2 Core Bowling Measures

#### Total Wickets
```dax
Total Wickets = SUM(fact_bowling_summary[wickets])
```

#### Runs Conceded
```dax
Total Runs Conceded = SUM(fact_bowling_summary[runs_conceded])
```

#### Legal Balls Bowled
```dax
Total Balls Bowled = SUM(fact_bowling_summary[balls_bowled])
```

#### Overs Bowled
```dax
Total Overs Bowled = DIVIDE([Total Balls Bowled], 6, 0)
```

#### Bowling Economy Rate
```dax
Bowling Economy Rate = 
DIVIDE(
    [Total Runs Conceded],
    [Total Overs Bowled],
    0
)
```

#### Bowling Strike Rate (Balls per Wicket)
```dax
Bowling Strike Rate = 
DIVIDE(
    [Total Balls Bowled],
    [Total Wickets],
    BLANK()
)
```

#### Dot Ball Percentage
```dax
Dot Ball % = 
DIVIDE(
    SUM(fact_bowling_summary[dot_balls]),
    [Total Balls Bowled],
    0
) * 100
```

---

### 2.3 Advanced Analytical & Selection Measures

#### Player Selection Flag (Openers)
```dax
Is Eligible Opener = 
IF(
    [Total Runs] >= 150 && [Batting Strike Rate] >= 130 && [Batting Average] >= 35,
    "Selected",
    "Not Eligible"
)
```

#### Bowler Impact Score
```dax
Bowler Impact Score = 
VAR Wkts = [Total Wickets] * 25
VAR Dots = SUM(fact_bowling_summary[dot_balls]) * 1.5
VAR RunsPenalty = [Total Runs Conceded] * 1.0
RETURN
Wkts + Dots - RunsPenalty
```

#### Dynamic Metric Title
```dax
Dynamic Header = 
SELECTEDVALUE(dim_players[team], "All Teams") & " - Player Performance Summary"
```
