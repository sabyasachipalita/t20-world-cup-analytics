-- ====================================================================
-- Relational Star Schema: 2022 ICC Men's T20 World Cup Analytics
-- ====================================================================

DROP TABLE IF EXISTS fact_bowling_summary;
DROP TABLE IF EXISTS fact_batting_summary;
DROP TABLE IF EXISTS dim_players;
DROP TABLE IF EXISTS dim_matches;

-- 1. Matches Dimension
CREATE TABLE dim_matches (
    match_id VARCHAR(20) PRIMARY KEY,
    team1 VARCHAR(50) NOT NULL,
    team2 VARCHAR(50) NOT NULL,
    winner VARCHAR(50),
    margin VARCHAR(50),
    ground VARCHAR(50),
    match_date DATE,
    stage VARCHAR(30)
);

-- 2. Players Dimension
CREATE TABLE dim_players (
    player_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    team VARCHAR(50) NOT NULL,
    battingStyle VARCHAR(50),
    bowlingStyle VARCHAR(50),
    playingRole VARCHAR(50)
);

-- 3. Batting Fact Table
CREATE TABLE fact_batting_summary (
    match_id VARCHAR(20),
    player_id VARCHAR(20),
    player_name VARCHAR(100),
    team VARCHAR(50),
    runs INTEGER,
    balls INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate REAL,
    boundary_runs INTEGER,
    boundary_pct REAL,
    is_out INTEGER,
    dismissal VARCHAR(100),
    FOREIGN KEY (match_id) REFERENCES dim_matches(match_id),
    FOREIGN KEY (player_id) REFERENCES dim_players(player_id)
);

-- 4. Bowling Fact Table
CREATE TABLE fact_bowling_summary (
    match_id VARCHAR(20),
    player_id VARCHAR(20),
    player_name VARCHAR(100),
    team VARCHAR(50),
    overs VARCHAR(10),
    balls_bowled INTEGER,
    maiden INTEGER,
    runs_conceded INTEGER,
    wickets INTEGER,
    economy_rate REAL,
    dot_balls INTEGER,
    fours_conceded INTEGER,
    sixes_conceded INTEGER,
    wides INTEGER,
    no_balls INTEGER,
    dot_ball_pct REAL,
    FOREIGN KEY (match_id) REFERENCES dim_matches(match_id),
    FOREIGN KEY (player_id) REFERENCES dim_players(player_id)
);

-- Indexes for query optimization
CREATE INDEX idx_batting_player ON fact_batting_summary(player_id);
CREATE INDEX idx_batting_match ON fact_batting_summary(match_id);
CREATE INDEX idx_bowling_player ON fact_bowling_summary(player_id);
CREATE INDEX idx_bowling_match ON fact_bowling_summary(match_id);
