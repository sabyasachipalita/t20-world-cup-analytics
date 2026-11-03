"""
Exploratory Data Analysis (EDA) module for 2022 T20 World Cup.
Computes tournament summary KPIs, boundary distributions, bowling efficiency,
and exports statistical summaries.
"""
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def run_eda():
    df_matches = pd.read_csv(os.path.join(PROC_DIR, 'dim_matches.csv'))
    df_players = pd.read_csv(os.path.join(PROC_DIR, 'dim_players.csv'))
    df_batting = pd.read_csv(os.path.join(PROC_DIR, 'fact_batting_summary.csv'))
    df_bowling = pd.read_csv(os.path.join(PROC_DIR, 'fact_bowling_summary.csv'))

    print("=" * 60)
    print("       2022 ICC T20 WORLD CUP - EDA SUMMARY REPORT")
    print("=" * 60)

    # 1. High Level Tournament Aggregates
    total_matches = len(df_matches)
    total_runs = df_batting['runs'].sum()
    total_wickets = df_bowling['wickets'].sum()
    total_balls = df_batting['balls'].sum()
    total_sixes = df_batting['sixes'].sum()
    total_fours = df_batting['fours'].sum()
    overall_sr = (total_runs / total_balls * 100) if total_balls > 0 else 0

    print(f"\n[1] Overall Tournament Aggregates:")
    print(f" • Total Matches Recorded   : {total_matches}")
    print(f" • Total Runs Scored        : {total_runs:,}")
    print(f" • Total Balls Bowled       : {total_balls:,}")
    print(f" • Total Wickets Taken      : {total_wickets}")
    print(f" • Boundaries               : {total_fours} Fours | {total_sixes} Sixes")
    print(f" • Global Strike Rate       : {overall_sr:.2f}")

    # 2. Top 5 Leading Run-Scorers
    print("\n[2] Top 5 Tournament Batsmen (Aggregated):")
    bat_agg = df_batting.groupby(['player_name', 'team']).agg(
        total_runs=('runs', 'sum'),
        balls_faced=('balls', 'sum'),
        innings=('match_id', 'count'),
        outs=('is_out', 'sum'),
        fours=('fours', 'sum'),
        sixes=('sixes', 'sum')
    ).reset_index()

    bat_agg['strike_rate'] = ((bat_agg['total_runs'] / bat_agg['balls_faced']) * 100).round(2)
    bat_agg['batting_avg'] = np.where(bat_agg['outs'] > 0, 
                                      (bat_agg['total_runs'] / bat_agg['outs']).round(2), 
                                      bat_agg['total_runs'])
    bat_agg['boundary_pct'] = (((bat_agg['fours']*4 + bat_agg['sixes']*6) / bat_agg['total_runs']) * 100).round(2)

    top_batsmen = bat_agg.sort_values(by='total_runs', ascending=False).head(5)
    print(top_batsmen[['player_name', 'team', 'total_runs', 'strike_rate', 'batting_avg', 'boundary_pct']].to_string(index=False))

    # 3. Top 5 Leading Wicket-Takers
    print("\n[3] Top 5 Tournament Bowlers (Aggregated):")
    bowl_agg = df_bowling.groupby(['player_name', 'team']).agg(
        wickets=('wickets', 'sum'),
        runs_conceded=('runs_conceded', 'sum'),
        balls_bowled=('balls_bowled', 'sum'),
        dot_balls=('dot_balls', 'sum')
    ).reset_index()

    bowl_agg['economy_rate'] = ((bowl_agg['runs_conceded'] / bowl_agg['balls_bowled']) * 6.0).round(2)
    bowl_agg['bowling_sr'] = np.where(bowl_agg['wickets'] > 0, 
                                      (bowl_agg['balls_bowled'] / bowl_agg['wickets']).round(2), 
                                      np.nan)
    bowl_agg['dot_ball_pct'] = ((bowl_agg['dot_balls'] / bowl_agg['balls_bowled']) * 100.0).round(2)

    top_bowlers = bowl_agg.sort_values(by=['wickets', 'economy_rate'], ascending=[False, True]).head(5)
    print(top_bowlers[['player_name', 'team', 'wickets', 'economy_rate', 'bowling_sr', 'dot_ball_pct']].to_string(index=False))

    # 4. Correlation Analysis
    corr_runs_sr = df_batting[['runs', 'strike_rate', 'balls', 'boundary_runs']].corr().round(2)
    print("\n[4] Batting Metrics Correlation Matrix:")
    print(corr_runs_sr)

    print("\n" + "=" * 60)

if __name__ == '__main__':
    run_eda()
