-- ====================================================================
-- 2022 ICC Men's T20 World Cup: Advanced SQL Analytics Queries
-- Demonstrating CTEs, Window Functions (DENSE_RANK, PARTITION BY), 
-- Multi-Table JOINs, and Statistical Aggregations.
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Overall Tournament Batting Leaderboard with DENSE_RANK()
-- --------------------------------------------------------------------
WITH batting_stats AS (
    SELECT 
        b.player_id,
        p.name AS player_name,
        p.team,
        p.playingRole,
        COUNT(b.match_id) AS innings_played,
        SUM(b.runs) AS total_runs,
        SUM(b.balls) AS total_balls,
        SUM(b.is_out) AS times_out,
        SUM(b.fours) AS total_fours,
        SUM(b.sixes) AS total_sixes,
        SUM(b.boundary_runs) AS total_boundary_runs
    FROM fact_batting_summary b
    JOIN dim_players p ON b.player_id = p.player_id
    GROUP BY b.player_id, p.name, p.team, p.playingRole
)
SELECT 
    player_name,
    team,
    playingRole,
    total_runs,
    ROUND((total_runs * 100.0 / NULLIF(total_balls, 0)), 2) AS strike_rate,
    ROUND((total_runs * 1.0 / NULLIF(times_out, 0)), 2) AS batting_average,
    ROUND((total_boundary_runs * 100.0 / NULLIF(total_runs, 0)), 2) AS boundary_pct,
    DENSE_RANK() OVER (ORDER BY total_runs DESC) AS run_rank,
    DENSE_RANK() OVER (ORDER BY (total_runs * 100.0 / NULLIF(total_balls, 0)) DESC) AS sr_rank
FROM batting_stats
WHERE total_runs >= 100
ORDER BY total_runs DESC;


-- --------------------------------------------------------------------
-- QUERY 2: Powerplay Openers Selection (Anchor + Aggressor Combo)
-- Criteria: Minimum 100 runs, Strike Rate > 125, Avg > 30
-- --------------------------------------------------------------------
WITH opener_metrics AS (
    SELECT 
        p.name AS player_name,
        p.team,
        SUM(b.runs) AS total_runs,
        SUM(b.balls) AS balls_faced,
        SUM(b.is_out) AS outs,
        SUM(b.fours) AS fours,
        SUM(b.sixes) AS sixes,
        ROUND((SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0)), 2) AS strike_rate,
        ROUND((SUM(b.runs) * 1.0 / NULLIF(SUM(b.is_out), 0)), 2) AS batting_avg
    FROM fact_batting_summary b
    JOIN dim_players p ON b.player_id = p.player_id
    WHERE p.playingRole IN ('Opening Batter', 'Wicketkeeper Batter', 'Top-order Batter')
    GROUP BY p.player_id, p.name, p.team
)
SELECT 
    player_name,
    team,
    total_runs,
    strike_rate,
    batting_avg,
    (fours * 4 + sixes * 6) AS boundary_runs,
    ROUND(((fours * 4 + sixes * 6) * 100.0 / total_runs), 2) AS boundary_pct,
    ROW_NUMBER() OVER (ORDER BY total_runs * strike_rate DESC) AS opener_priority
FROM opener_metrics
WHERE total_runs >= 150 AND strike_rate >= 125
ORDER BY opener_priority ASC
LIMIT 2;


-- --------------------------------------------------------------------
-- QUERY 3: High-Impact Middle-Order Anchors & Finishers (No. 3 to 5)
-- Criteria: Strike Rate > 140 and Batting Average > 30
-- --------------------------------------------------------------------
WITH middle_order AS (
    SELECT 
        p.name AS player_name,
        p.team,
        p.playingRole,
        SUM(b.runs) AS total_runs,
        ROUND((SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0)), 2) AS strike_rate,
        ROUND((SUM(b.runs) * 1.0 / NULLIF(SUM(b.is_out), 0)), 2) AS batting_avg,
        SUM(b.sixes) AS total_sixes
    FROM fact_batting_summary b
    JOIN dim_players p ON b.player_id = p.player_id
    GROUP BY p.player_id, p.name, p.team, p.playingRole
)
SELECT 
    player_name,
    team,
    playingRole,
    total_runs,
    strike_rate,
    batting_avg,
    total_sixes,
    DENSE_RANK() OVER (ORDER BY strike_rate DESC) AS strike_rate_rank
FROM middle_order
WHERE total_runs >= 100 AND (strike_rate >= 140 OR batting_avg >= 40)
ORDER BY strike_rate DESC;


-- --------------------------------------------------------------------
-- QUERY 4: Elite Bowlers Benchmark (Wickets + Economy + Dot Ball %)
-- Criteria: Min 12 overs (72 balls bowled)
-- --------------------------------------------------------------------
WITH bowling_stats AS (
    SELECT 
        bw.player_id,
        p.name AS bowler_name,
        p.team,
        p.bowlingStyle,
        SUM(bw.balls_bowled) AS balls_bowled,
        SUM(bw.runs_conceded) AS runs_conceded,
        SUM(bw.wickets) AS total_wickets,
        SUM(bw.dot_balls) AS total_dots
    FROM fact_bowling_summary bw
    JOIN dim_players p ON bw.player_id = p.player_id
    GROUP BY bw.player_id, p.name, p.team, p.bowlingStyle
    HAVING SUM(bw.balls_bowled) >= 48
)
SELECT 
    bowler_name,
    team,
    bowlingStyle,
    total_wickets,
    ROUND((runs_conceded * 6.0 / balls_bowled), 2) AS economy_rate,
    ROUND((balls_bowled * 1.0 / NULLIF(total_wickets, 0)), 2) AS bowling_strike_rate,
    ROUND((total_dots * 100.0 / balls_bowled), 2) AS dot_ball_pct,
    DENSE_RANK() OVER (ORDER BY total_wickets DESC, (runs_conceded * 6.0 / balls_bowled) ASC) AS overall_bowler_rank
FROM bowling_stats
ORDER BY overall_bowler_rank ASC;


-- --------------------------------------------------------------------
-- QUERY 5: MVP All-Rounders (Dual-Threat Score)
-- Aggregates batting runs and bowling wickets in a single unified CTE
-- --------------------------------------------------------------------
WITH player_batting AS (
    SELECT 
        player_id,
        SUM(runs) AS bat_runs,
        ROUND((SUM(runs) * 100.0 / NULLIF(SUM(balls), 0)), 2) AS bat_sr
    FROM fact_batting_summary
    GROUP BY player_id
),
player_bowling AS (
    SELECT 
        player_id,
        SUM(wickets) AS bowl_wickets,
        ROUND((SUM(runs_conceded) * 6.0 / NULLIF(SUM(balls_bowled), 0)), 2) AS bowl_economy
    FROM fact_bowling_summary
    GROUP BY player_id
)
SELECT 
    p.name AS player_name,
    p.team,
    p.playingRole,
    COALESCE(b.bat_runs, 0) AS runs_scored,
    COALESCE(b.bat_sr, 0) AS bat_strike_rate,
    COALESCE(bw.bowl_wickets, 0) AS wickets_taken,
    COALESCE(bw.bowl_economy, 0) AS bowling_economy,
    ROUND((COALESCE(b.bat_runs, 0) * 1.0) + (COALESCE(bw.bowl_wickets, 0) * 25.0) - (COALESCE(bw.bowl_economy, 0) * 5.0), 2) AS allrounder_impact_score
FROM dim_players p
LEFT JOIN player_batting b ON p.player_id = b.player_id
LEFT JOIN player_bowling bw ON p.player_id = bw.player_id
WHERE (COALESCE(b.bat_runs, 0) > 40 AND COALESCE(bw.bowl_wickets, 0) >= 3)
   OR p.playingRole = 'Allrounder'
ORDER BY allrounder_impact_score DESC;
