"""
ETL & Data Cleaning Pipeline for 2022 T20 Cricket World Cup.
Cleans raw match, batting, and bowling datasets and transforms them
into a relational Star Schema (Dimension & Fact tables).
"""
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(PROC_DIR, exist_ok=True)

def parse_overs_to_balls(over_val) -> int:
    """
    Converts cricket fractional over notation into integer ball counts.
    e.g., 3.4 overs -> (3 * 6) + 4 = 22 balls.
    """
    if pd.isna(over_val):
        return 0
    parts = str(over_val).strip().split('.')
    completed_overs = int(parts[0])
    partial_balls = int(parts[1]) if len(parts) > 1 else 0
    return (completed_overs * 6) + partial_balls

def clean_matches():
    print("Processing dim_matches...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'matches_raw.csv'))
    df['match_date'] = pd.to_datetime(df['match_date'])
    df.to_csv(os.path.join(PROC_DIR, 'dim_matches.csv'), index=False)
    print(f" Saved dim_matches ({len(df)} rows)")
    return df

def clean_players():
    print("Processing dim_players...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'players_raw.csv'))
    df['name'] = df['name'].str.strip()
    df.to_csv(os.path.join(PROC_DIR, 'dim_players.csv'), index=False)
    print(f" Saved dim_players ({len(df)} rows)")
    return df

def clean_batting(df_players):
    print("Processing fact_batting_summary...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'batting_raw.csv'))
    
    # 1. Clean player name & link to player_id
    df['batsmanName'] = df['batsmanName'].str.strip()
    player_id_map = dict(zip(df_players['name'], df_players['player_id']))
    df['player_id'] = df['batsmanName'].map(player_id_map)
    
    # 2. Derive out status
    df['is_out'] = df['dismissal'].apply(
        lambda x: 0 if str(x).strip().lower() in ['not out', 'dnb', 'nan', ''] else 1
    )
    
    # 3. Numeric type conversion
    for col in ['runs', 'balls', '4s', '6s']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    df['strike_rate'] = np.where(
        df['balls'] > 0,
        ((df['runs'] / df['balls']) * 100.0).round(2),
        0.0
    )
    
    # 4. Feature engineering: Boundary runs & boundary %
    df['boundary_runs'] = (df['4s'] * 4) + (df['6s'] * 6)
    df['boundary_pct'] = np.where(
        df['runs'] > 0,
        ((df['boundary_runs'] / df['runs']) * 100.0).round(2),
        0.0
    )
    
    # Select & order schema columns
    schema_cols = [
        'match_id', 'player_id', 'batsmanName', 'teamInnings',
        'runs', 'balls', '4s', '6s', 'strike_rate',
        'boundary_runs', 'boundary_pct', 'is_out', 'dismissal'
    ]
    df = df[schema_cols].rename(columns={
        'batsmanName': 'player_name',
        'teamInnings': 'team',
        '4s': 'fours',
        '6s': 'sixes'
    })
    
    df.to_csv(os.path.join(PROC_DIR, 'fact_batting_summary.csv'), index=False)
    print(f" Saved fact_batting_summary ({len(df)} rows)")
    return df

def clean_bowling(df_players):
    print("Processing fact_bowling_summary...")
    df = pd.read_csv(os.path.join(RAW_DIR, 'bowling_raw.csv'))
    
    df['bowlerName'] = df['bowlerName'].str.strip()
    player_id_map = dict(zip(df_players['name'], df_players['player_id']))
    df['player_id'] = df['bowlerName'].map(player_id_map)
    
    # Convert overs to exact legal ball count
    df['balls_bowled'] = df['overs'].apply(parse_overs_to_balls)
    
    for col in ['maiden', 'runs', 'wickets', '0s', '4s', '6s', 'wdes', 'noballs']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # True economy: (runs / total balls) * 6
    df['economy_rate'] = np.where(
        df['balls_bowled'] > 0,
        ((df['runs'] / df['balls_bowled']) * 6.0).round(2),
        0.0
    )
    
    # Dot ball %
    df['dot_ball_pct'] = np.where(
        df['balls_bowled'] > 0,
        ((df['0s'] / df['balls_bowled']) * 100.0).round(2),
        0.0
    )
    
    schema_cols = [
        'match_id', 'player_id', 'bowlerName', 'bowlingTeam',
        'overs', 'balls_bowled', 'maiden', 'runs', 'wickets',
        'economy_rate', '0s', '4s', '6s', 'wdes', 'noballs', 'dot_ball_pct'
    ]
    df = df[schema_cols].rename(columns={
        'bowlerName': 'player_name',
        'bowlingTeam': 'team',
        'runs': 'runs_conceded',
        '0s': 'dot_balls',
        '4s': 'fours_conceded',
        '6s': 'sixes_conceded',
        'wdes': 'wides',
        'noballs': 'no_balls'
    })
    
    df.to_csv(os.path.join(PROC_DIR, 'fact_bowling_summary.csv'), index=False)
    print(f" Saved fact_bowling_summary ({len(df)} rows)")
    return df

def main():
    print("=== Starting Data Cleaning Pipeline ===")
    df_matches = clean_matches()
    df_players = clean_players()
    df_batting = clean_batting(df_players)
    df_bowling = clean_bowling(df_players)
    print("=== Pipeline Execution Finished Successfully! ===")

if __name__ == '__main__':
    main()
