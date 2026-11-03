"""
Script to generate realistic, detailed 2022 T20 World Cup datasets.
Includes match summaries, players metadata, batting scorecards, and bowling records.
"""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

# 1. Matches Data
matches = [
    {"match_id": "T20I_01", "team1": "Namibia", "team2": "Sri Lanka", "winner": "Namibia", "margin": "55 runs", "ground": "Geelong", "match_date": "2022-10-16", "stage": "Group Stage"},
    {"match_id": "T20I_02", "team1": "Netherlands", "team2": "UAE", "winner": "Netherlands", "margin": "3 wickets", "ground": "Geelong", "match_date": "2022-10-16", "stage": "Group Stage"},
    {"match_id": "T20I_03", "team1": "Scotland", "team2": "West Indies", "winner": "Scotland", "margin": "42 runs", "ground": "Hobart", "match_date": "2022-10-17", "stage": "Group Stage"},
    {"match_id": "T20I_04", "team1": "Zimbabwe", "team2": "Ireland", "winner": "Zimbabwe", "margin": "31 runs", "ground": "Hobart", "match_date": "2022-10-17", "stage": "Group Stage"},
    {"match_id": "T20I_05", "team1": "Australia", "team2": "New Zealand", "winner": "New Zealand", "margin": "89 runs", "ground": "Sydney", "match_date": "2022-10-22", "stage": "Super 12"},
    {"match_id": "T20I_06", "team1": "England", "team2": "Afghanistan", "winner": "England", "margin": "5 wickets", "ground": "Perth", "match_date": "2022-10-22", "stage": "Super 12"},
    {"match_id": "T20I_07", "team1": "India", "team2": "Pakistan", "winner": "India", "margin": "4 wickets", "ground": "Melbourne", "match_date": "2022-10-23", "stage": "Super 12"},
    {"match_id": "T20I_08", "team1": "Bangladesh", "team2": "Netherlands", "winner": "Bangladesh", "margin": "9 runs", "ground": "Hobart", "match_date": "2022-10-24", "stage": "Super 12"},
    {"match_id": "T20I_09", "team1": "South Africa", "team2": "Zimbabwe", "winner": "No Result", "margin": "Rain", "ground": "Hobart", "match_date": "2022-10-24", "stage": "Super 12"},
    {"match_id": "T20I_10", "team1": "Australia", "team2": "Sri Lanka", "winner": "Australia", "margin": "7 wickets", "ground": "Perth", "match_date": "2022-10-25", "stage": "Super 12"},
    {"match_id": "T20I_11", "team1": "England", "team2": "Ireland", "winner": "Ireland", "margin": "5 runs (DLS)", "ground": "Melbourne", "match_date": "2022-10-26", "stage": "Super 12"},
    {"match_id": "T20I_12", "team1": "South Africa", "team2": "Bangladesh", "winner": "South Africa", "margin": "104 runs", "ground": "Sydney", "match_date": "2022-10-27", "stage": "Super 12"},
    {"match_id": "T20I_13", "team1": "India", "team2": "Netherlands", "winner": "India", "margin": "56 runs", "ground": "Sydney", "match_date": "2022-10-27", "stage": "Super 12"},
    {"match_id": "T20I_14", "team1": "Pakistan", "team2": "Zimbabwe", "winner": "Zimbabwe", "margin": "1 run", "ground": "Perth", "match_date": "2022-10-27", "stage": "Super 12"},
    {"match_id": "T20I_15", "team1": "New Zealand", "team2": "Sri Lanka", "winner": "New Zealand", "margin": "65 runs", "ground": "Sydney", "match_date": "2022-10-29", "stage": "Super 12"},
    {"match_id": "T20I_16", "team1": "India", "team2": "South Africa", "winner": "South Africa", "margin": "5 wickets", "ground": "Perth", "match_date": "2022-10-30", "stage": "Super 12"},
    {"match_id": "T20I_17", "team1": "England", "team2": "New Zealand", "winner": "England", "margin": "20 runs", "ground": "Brisbane", "match_date": "2022-11-01", "stage": "Super 12"},
    {"match_id": "T20I_18", "team1": "India", "team2": "Bangladesh", "winner": "India", "margin": "5 runs (DLS)", "ground": "Adelaide", "match_date": "2022-11-02", "stage": "Super 12"},
    {"match_id": "T20I_19", "team1": "Pakistan", "team2": "South Africa", "winner": "Pakistan", "margin": "33 runs (DLS)", "ground": "Sydney", "match_date": "2022-11-03", "stage": "Super 12"},
    {"match_id": "T20I_20", "team1": "Australia", "team2": "Afghanistan", "winner": "Australia", "margin": "4 runs", "ground": "Adelaide", "match_date": "2022-11-04", "stage": "Super 12"},
    {"match_id": "T20I_21", "team1": "England", "team2": "Sri Lanka", "winner": "England", "margin": "4 wickets", "ground": "Sydney", "match_date": "2022-11-05", "stage": "Super 12"},
    {"match_id": "T20I_22", "team1": "South Africa", "team2": "Netherlands", "winner": "Netherlands", "margin": "13 runs", "ground": "Adelaide", "match_date": "2022-11-06", "stage": "Super 12"},
    {"match_id": "T20I_23", "team1": "Pakistan", "team2": "Bangladesh", "winner": "Pakistan", "margin": "5 wickets", "ground": "Adelaide", "match_date": "2022-11-06", "stage": "Super 12"},
    {"match_id": "T20I_24", "team1": "India", "team2": "Zimbabwe", "winner": "India", "margin": "71 runs", "ground": "Melbourne", "match_date": "2022-11-06", "stage": "Super 12"},
    {"match_id": "T20I_25", "team1": "New Zealand", "team2": "Pakistan", "winner": "Pakistan", "margin": "7 wickets", "ground": "Sydney", "match_date": "2022-11-09", "stage": "Semi Final"},
    {"match_id": "T20I_26", "team1": "India", "team2": "England", "winner": "England", "margin": "10 wickets", "ground": "Adelaide", "match_date": "2022-11-10", "stage": "Semi Final"},
    {"match_id": "T20I_27", "team1": "Pakistan", "team2": "England", "winner": "England", "margin": "5 wickets", "ground": "Melbourne", "match_date": "2022-11-13", "stage": "Final"}
]
df_matches = pd.DataFrame(matches)
df_matches.to_csv(os.path.join(RAW_DIR, 'matches_raw.csv'), index=False)

# 2. Players Metadata
players = [
    {"player_id": "P01", "name": "Virat Kohli", "team": "India", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium", "playingRole": "Top-order Batter"},
    {"player_id": "P02", "name": "Suryakumar Yadav", "team": "India", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium", "playingRole": "Middle-order Batter"},
    {"player_id": "P03", "name": "Rohit Sharma", "team": "India", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Opening Batter"},
    {"player_id": "P04", "name": "Hardik Pandya", "team": "India", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Fast Medium", "playingRole": "Allrounder"},
    {"player_id": "P05", "name": "Arshdeep Singh", "team": "India", "battingStyle": "Left Hand Bat", "bowlingStyle": "Left Arm Fast Medium", "playingRole": "Bowler"},
    {"player_id": "P06", "name": "Bhuvneshwar Kumar", "team": "India", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium Fast", "playingRole": "Bowler"},
    {"player_id": "P07", "name": "Jos Buttler", "team": "England", "battingStyle": "Right Hand Bat", "bowlingStyle": "None", "playingRole": "Wicketkeeper Batter"},
    {"player_id": "P08", "name": "Alex Hales", "team": "England", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium", "playingRole": "Opening Batter"},
    {"player_id": "P09", "name": "Ben Stokes", "team": "England", "battingStyle": "Left Hand Bat", "bowlingStyle": "Right Arm Fast Medium", "playingRole": "Allrounder"},
    {"player_id": "P10", "name": "Sam Curran", "team": "England", "battingStyle": "Left Hand Bat", "bowlingStyle": "Left Arm Medium Fast", "playingRole": "Allrounder"},
    {"player_id": "P11", "name": "Mark Wood", "team": "England", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Fast", "playingRole": "Bowler"},
    {"player_id": "P12", "name": "Babar Azam", "team": "Pakistan", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Opening Batter"},
    {"player_id": "P13", "name": "Mohammad Rizwan", "team": "Pakistan", "battingStyle": "Right Hand Bat", "bowlingStyle": "None", "playingRole": "Wicketkeeper Batter"},
    {"player_id": "P14", "name": "Shan Masood", "team": "Pakistan", "battingStyle": "Left Hand Bat", "bowlingStyle": "Right Arm Medium Fast", "playingRole": "Top-order Batter"},
    {"player_id": "P15", "name": "Shadab Khan", "team": "Pakistan", "battingStyle": "Right Hand Bat", "bowlingStyle": "Legbreak", "playingRole": "Allrounder"},
    {"player_id": "P16", "name": "Shaheen Shah Afridi", "team": "Pakistan", "battingStyle": "Left Hand Bat", "bowlingStyle": "Left Arm Fast", "playingRole": "Bowler"},
    {"player_id": "P17", "name": "Haris Rauf", "team": "Pakistan", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Fast", "playingRole": "Bowler"},
    {"player_id": "P18", "name": "Glenn Phillips", "team": "New Zealand", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Middle-order Batter"},
    {"player_id": "P19", "name": "Devon Conway", "team": "New Zealand", "battingStyle": "Left Hand Bat", "bowlingStyle": "Right Arm Medium", "playingRole": "Wicketkeeper Batter"},
    {"player_id": "P20", "name": "Tim Southee", "team": "New Zealand", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium Fast", "playingRole": "Bowler"},
    {"player_id": "P21", "name": "Trent Boult", "team": "New Zealand", "battingStyle": "Right Hand Bat", "bowlingStyle": "Left Arm Fast Medium", "playingRole": "Bowler"},
    {"player_id": "P22", "name": "Sikandar Raza", "team": "Zimbabwe", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Allrounder"},
    {"player_id": "P23", "name": "Wanindu Hasaranga", "team": "Sri Lanka", "battingStyle": "Right Hand Bat", "bowlingStyle": "Legbreak", "playingRole": "Allrounder"},
    {"player_id": "P24", "name": "Anrich Nortje", "team": "South Africa", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Fast", "playingRole": "Bowler"},
    {"player_id": "P25", "name": "Quinton de Kock", "team": "South Africa", "battingStyle": "Left Hand Bat", "bowlingStyle": "None", "playingRole": "Wicketkeeper Batter"},
    {"player_id": "P26", "name": "Rilee Rossouw", "team": "South Africa", "battingStyle": "Left Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Top-order Batter"},
    {"player_id": "P27", "name": "Marcus Stoinis", "team": "Australia", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Medium", "playingRole": "Allrounder"},
    {"player_id": "P28", "name": "Glenn Maxwell", "team": "Australia", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Offbreak", "playingRole": "Allrounder"},
    {"player_id": "P29", "name": "Josh Hazlewood", "team": "Australia", "battingStyle": "Left Hand Bat", "bowlingStyle": "Right Arm Fast Medium", "playingRole": "Bowler"},
    {"player_id": "P30", "name": "Max O'Dowd", "team": "Netherlands", "battingStyle": "Right Hand Bat", "bowlingStyle": "Right Arm Legbreak", "playingRole": "Opening Batter"}
]
df_players = pd.DataFrame(players)
df_players.to_csv(os.path.join(RAW_DIR, 'players_raw.csv'), index=False)

# 3. Batting Raw Data (Selected representative tournament innings)
batting_records = [
    # Virat Kohli (Top tournament run getter: 296 runs)
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "not out", "runs": "82", "balls": "53", "4s": "6", "6s": "4", "SR": "154.72"},
    {"match_id": "T20I_13", "match": "India Vs Netherlands", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "not out", "runs": "62", "balls": "44", "4s": "3", "6s": "2", "SR": "140.91"},
    {"match_id": "T20I_16", "match": "India Vs South Africa", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "c Rabada b Ngidi", "runs": "12", "balls": "11", "4s": "2", "6s": "0", "SR": "109.09"},
    {"match_id": "T20I_18", "match": "India Vs Bangladesh", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "not out", "runs": "64", "balls": "44", "4s": "8", "6s": "1", "SR": "145.45"},
    {"match_id": "T20I_24", "match": "India Vs Zimbabwe", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "c Burl b Williams", "runs": "26", "balls": "25", "4s": "2", "6s": "0", "SR": "104.00"},
    {"match_id": "T20I_26", "match": "India Vs England", "teamInnings": "India", "batsmanName": "Virat Kohli", "dismissal": "c Rashid b Jordan", "runs": "50", "balls": "40", "4s": "4", "6s": "1", "SR": "125.00"},

    # Suryakumar Yadav (239 runs, SR 189.68)
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "c Rizwan b Rauf", "runs": "15", "balls": "10", "4s": "2", "6s": "0", "SR": "150.00"},
    {"match_id": "T20I_13", "match": "India Vs Netherlands", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "not out", "runs": "51", "balls": "25", "4s": "7", "6s": "1", "SR": "204.00"},
    {"match_id": "T20I_16", "match": "India Vs South Africa", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "c Maharaj b Parnell", "runs": "68", "balls": "40", "4s": "6", "6s": "3", "SR": "170.00"},
    {"match_id": "T20I_18", "match": "India Vs Bangladesh", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "b Shakib", "runs": "30", "balls": "16", "4s": "4", "6s": "0", "SR": "187.50"},
    {"match_id": "T20I_24", "match": "India Vs Zimbabwe", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "not out", "runs": "61", "balls": "25", "4s": "6", "6s": "4", "SR": "244.00"},
    {"match_id": "T20I_26", "match": "India Vs England", "teamInnings": "India", "batsmanName": "Suryakumar Yadav", "dismissal": "c Salt b Rashid", "runs": "14", "balls": "10", "4s": "1", "6s": "1", "SR": "140.00"},

    # Hardik Pandya
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "India", "batsmanName": "Hardik Pandya", "dismissal": "c Babar b Nawaz", "runs": "40", "balls": "37", "4s": "1", "6s": "2", "SR": "108.11"},
    {"match_id": "T20I_26", "match": "India Vs England", "teamInnings": "India", "batsmanName": "Hardik Pandya", "dismissal": "hit wicket b Jordan", "runs": "63", "balls": "33", "4s": "4", "6s": "5", "SR": "190.91"},

    # Jos Buttler (225 runs, Captain of Champions)
    {"match_id": "T20I_06", "match": "England Vs Afghanistan", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "c Mujeeb b Fazalhaq", "runs": "18", "balls": "18", "4s": "2", "6s": "0", "SR": "100.00"},
    {"match_id": "T20I_11", "match": "England Vs Ireland", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "c Tucker b Fionn Hand", "runs": "0", "balls": "2", "4s": "0", "6s": "0", "SR": "0.00"},
    {"match_id": "T20I_17", "match": "England Vs New Zealand", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "run out (Williamson)", "runs": "73", "balls": "47", "4s": "7", "6s": "2", "SR": "155.32"},
    {"match_id": "T20I_21", "match": "England Vs Sri Lanka", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "c Karunaratne b Hasaranga", "runs": "28", "balls": "23", "4s": "2", "6s": "1", "SR": "121.74"},
    {"match_id": "T20I_26", "match": "India Vs England", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "not out", "runs": "80", "balls": "49", "4s": "9", "6s": "3", "SR": "163.27"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "teamInnings": "England", "batsmanName": "Jos Buttler", "dismissal": "c Rizwan b Haris Rauf", "runs": "26", "balls": "17", "4s": "3", "6s": "1", "SR": "152.94"},

    # Alex Hales (212 runs)
    {"match_id": "T20I_06", "match": "England Vs Afghanistan", "teamInnings": "England", "batsmanName": "Alex Hales", "dismissal": "c Fazalhaq b Stokes", "runs": "19", "balls": "20", "4s": "1", "6s": "0", "SR": "95.00"},
    {"match_id": "T20I_17", "match": "England Vs New Zealand", "teamInnings": "England", "batsmanName": "Alex Hales", "dismissal": "c Mitchell b Santner", "runs": "52", "balls": "40", "4s": "7", "6s": "1", "SR": "130.00"},
    {"match_id": "T20I_21", "match": "England Vs Sri Lanka", "teamInnings": "England", "batsmanName": "Alex Hales", "dismissal": "c & b Hasaranga", "runs": "47", "balls": "30", "4s": "7", "6s": "1", "SR": "156.67"},
    {"match_id": "T20I_26", "match": "India Vs England", "teamInnings": "England", "batsmanName": "Alex Hales", "dismissal": "not out", "runs": "86", "balls": "47", "4s": "4", "6s": "7", "SR": "182.98"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "teamInnings": "England", "batsmanName": "Alex Hales", "dismissal": "b Shaheen Afridi", "runs": "1", "balls": "2", "4s": "0", "6s": "0", "SR": "50.00"},

    # Ben Stokes
    {"match_id": "T20I_21", "match": "England Vs Sri Lanka", "teamInnings": "England", "batsmanName": "Ben Stokes", "dismissal": "not out", "runs": "42", "balls": "36", "4s": "2", "6s": "0", "SR": "116.67"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "teamInnings": "England", "batsmanName": "Ben Stokes", "dismissal": "not out", "runs": "52", "balls": "49", "4s": "5", "6s": "1", "SR": "106.12"},

    # Babar Azam & Mohammad Rizwan
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "Pakistan", "batsmanName": "Babar Azam", "dismissal": "lbw b Arshdeep", "runs": "0", "balls": "1", "4s": "0", "6s": "0", "SR": "0.00"},
    {"match_id": "T20I_25", "match": "New Zealand Vs Pakistan", "teamInnings": "Pakistan", "batsmanName": "Babar Azam", "dismissal": "c Mitchell b Boult", "runs": "53", "balls": "42", "4s": "7", "6s": "0", "SR": "126.19"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "teamInnings": "Pakistan", "batsmanName": "Babar Azam", "dismissal": "c & b Rashid", "runs": "32", "balls": "28", "4s": "2", "6s": "0", "SR": "114.29"},
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "Pakistan", "batsmanName": "Mohammad Rizwan", "dismissal": "c Bhuvneshwar b Arshdeep", "runs": "4", "balls": "12", "4s": "1", "6s": "0", "SR": "33.33"},
    {"match_id": "T20I_25", "match": "New Zealand Vs Pakistan", "teamInnings": "Pakistan", "batsmanName": "Mohammad Rizwan", "dismissal": "c Phillips b Boult", "runs": "57", "balls": "43", "4s": "5", "6s": "0", "SR": "132.56"},

    # Shan Masood & Shadab Khan
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "teamInnings": "Pakistan", "batsmanName": "Shan Masood", "dismissal": "not out", "runs": "52", "balls": "42", "4s": "5", "6s": "0", "SR": "123.81"},
    {"match_id": "T20I_19", "match": "Pakistan Vs South Africa", "teamInnings": "Pakistan", "batsmanName": "Shadab Khan", "dismissal": "c Stubbs b Nortje", "runs": "52", "balls": "22", "4s": "3", "6s": "4", "SR": "236.36"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "teamInnings": "Pakistan", "batsmanName": "Shan Masood", "dismissal": "c Livingstone b Curran", "runs": "38", "balls": "28", "4s": "2", "6s": "1", "SR": "135.71"},

    # Glenn Phillips (201 runs, 1 century)
    {"match_id": "T20I_05", "match": "Australia Vs New Zealand", "teamInnings": "New Zealand", "batsmanName": "Glenn Phillips", "dismissal": "c & b Hazlewood", "runs": "12", "balls": "10", "4s": "2", "6s": "0", "SR": "120.00"},
    {"match_id": "T20I_15", "match": "New Zealand Vs Sri Lanka", "teamInnings": "New Zealand", "batsmanName": "Glenn Phillips", "dismissal": "c Shanaka b Kumara", "runs": "104", "balls": "64", "4s": "10", "6s": "4", "SR": "162.50"},
    {"match_id": "T20I_17", "match": "England Vs New Zealand", "teamInnings": "New Zealand", "batsmanName": "Glenn Phillips", "dismissal": "c Substitue b Curran", "runs": "62", "balls": "36", "4s": "4", "6s": "3", "SR": "172.22"},

    # Marcus Stoinis & Glenn Maxwell
    {"match_id": "T20I_10", "match": "Australia Vs Sri Lanka", "teamInnings": "Australia", "batsmanName": "Marcus Stoinis", "dismissal": "not out", "runs": "59", "balls": "18", "4s": "4", "6s": "6", "SR": "327.78"},
    {"match_id": "T20I_20", "match": "Australia Vs Afghanistan", "teamInnings": "Australia", "batsmanName": "Glenn Maxwell", "dismissal": "not out", "runs": "54", "balls": "32", "4s": "6", "6s": "2", "SR": "168.75"},

    # Rilee Rossouw & Quinton de Kock
    {"match_id": "T20I_12", "match": "South Africa Vs Bangladesh", "teamInnings": "South Africa", "batsmanName": "Rilee Rossouw", "dismissal": "c Litton b Shakib", "runs": "109", "balls": "56", "4s": "7", "6s": "8", "SR": "194.64"},
    {"match_id": "T20I_12", "match": "South Africa Vs Bangladesh", "teamInnings": "South Africa", "batsmanName": "Quinton de Kock", "dismissal": "c Soumya b Afif", "runs": "63", "balls": "38", "4s": "7", "6s": "3", "SR": "165.79"},

    # Sikandar Raza
    {"match_id": "T20I_04", "match": "Zimbabwe Vs Ireland", "teamInnings": "Zimbabwe", "batsmanName": "Sikandar Raza", "dismissal": "b Little", "runs": "82", "balls": "48", "4s": "5", "6s": "5", "SR": "170.83"},
    {"match_id": "T20I_14", "match": "Pakistan Vs Zimbabwe", "teamInnings": "Zimbabwe", "batsmanName": "Sikandar Raza", "dismissal": "c Babar b Wasim", "runs": "9", "balls": "16", "4s": "1", "6s": "0", "SR": "56.25"},

    # Max O'Dowd
    {"match_id": "T20I_02", "match": "Netherlands Vs UAE", "teamInnings": "Netherlands", "batsmanName": "Max O'Dowd", "dismissal": "b Junaid Siddique", "runs": "23", "balls": "18", "4s": "3", "6s": "1", "SR": "127.78"},
    {"match_id": "T20I_22", "match": "South Africa Vs Netherlands", "teamInnings": "Netherlands", "batsmanName": "Max O'Dowd", "dismissal": "c Maharaj b Shamsi", "runs": "29", "balls": "31", "4s": "1", "6s": "1", "SR": "93.55"}
]
df_batting = pd.DataFrame(batting_records)
df_batting.to_csv(os.path.join(RAW_DIR, 'batting_raw.csv'), index=False)

# 4. Bowling Raw Data
bowling_records = [
    # Sam Curran (Player of the Tournament - 13 wickets)
    {"match_id": "T20I_06", "match": "England Vs Afghanistan", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "3.4", "maiden": "0", "runs": "10", "wickets": "5", "economy": "2.73", "0s": "12", "4s": "1", "6s": "0", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_11", "match": "England Vs Ireland", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "3.0", "maiden": "0", "runs": "31", "wickets": "2", "economy": "10.33", "0s": "7", "4s": "4", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_17", "match": "England Vs New Zealand", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "4.0", "maiden": "0", "runs": "26", "wickets": "2", "economy": "6.50", "0s": "11", "4s": "1", "6s": "1", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_21", "match": "England Vs Sri Lanka", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "4.0", "maiden": "0", "runs": "27", "wickets": "1", "economy": "6.75", "0s": "9", "4s": "2", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_26", "match": "India Vs England", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "4.0", "maiden": "0", "runs": "42", "wickets": "0", "economy": "10.50", "0s": "7", "4s": "4", "6s": "2", "wdes": "2", "noballs": "0"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "bowlingTeam": "England", "bowlerName": "Sam Curran", "overs": "4.0", "maiden": "0", "runs": "12", "wickets": "3", "economy": "3.00", "0s": "15", "4s": "0", "6s": "0", "wdes": "0", "noballs": "0"},

    # Wanindu Hasaranga (Leading tournament wicket-taker: 15 wickets)
    {"match_id": "T20I_01", "match": "Namibia Vs Sri Lanka", "bowlingTeam": "Sri Lanka", "bowlerName": "Wanindu Hasaranga", "overs": "4.0", "maiden": "0", "runs": "27", "wickets": "1", "economy": "6.75", "0s": "9", "4s": "1", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_10", "match": "Australia Vs Sri Lanka", "bowlingTeam": "Sri Lanka", "bowlerName": "Wanindu Hasaranga", "overs": "3.0", "maiden": "0", "runs": "53", "wickets": "0", "economy": "17.67", "0s": "3", "4s": "3", "6s": "5", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_15", "match": "New Zealand Vs Sri Lanka", "bowlingTeam": "Sri Lanka", "bowlerName": "Wanindu Hasaranga", "overs": "4.0", "maiden": "0", "runs": "22", "wickets": "2", "economy": "5.50", "0s": "12", "4s": "2", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_21", "match": "England Vs Sri Lanka", "bowlingTeam": "Sri Lanka", "bowlerName": "Wanindu Hasaranga", "overs": "4.0", "maiden": "0", "runs": "23", "wickets": "2", "economy": "5.75", "0s": "11", "4s": "1", "6s": "1", "wdes": "0", "noballs": "0"},

    # Arshdeep Singh (10 wickets)
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "4.0", "maiden": "0", "runs": "32", "wickets": "3", "economy": "8.00", "0s": "12", "4s": "3", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_13", "match": "India Vs Netherlands", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "4.0", "maiden": "0", "runs": "37", "wickets": "2", "economy": "9.25", "0s": "10", "4s": "3", "6s": "2", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_16", "match": "India Vs South Africa", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "4.0", "maiden": "0", "runs": "25", "wickets": "2", "economy": "6.25", "0s": "13", "4s": "2", "6s": "1", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_18", "match": "India Vs Bangladesh", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "4.0", "maiden": "0", "runs": "38", "wickets": "2", "economy": "9.50", "0s": "8", "4s": "4", "6s": "1", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_24", "match": "India Vs Zimbabwe", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "3.0", "maiden": "0", "runs": "9", "wickets": "1", "economy": "3.00", "0s": "12", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_26", "match": "India Vs England", "bowlingTeam": "India", "bowlerName": "Arshdeep Singh", "overs": "2.0", "maiden": "0", "runs": "15", "wickets": "0", "economy": "7.50", "0s": "4", "4s": "2", "6s": "0", "wdes": "0", "noballs": "0"},

    # Shaheen Shah Afridi (11 wickets)
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "4.0", "maiden": "0", "runs": "34", "wickets": "0", "economy": "8.50", "0s": "11", "4s": "4", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_14", "match": "Pakistan Vs Zimbabwe", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "4.0", "maiden": "0", "runs": "29", "wickets": "0", "economy": "7.25", "0s": "10", "4s": "2", "6s": "1", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_19", "match": "Pakistan Vs South Africa", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "3.0", "maiden": "0", "runs": "14", "wickets": "3", "economy": "4.67", "0s": "11", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_23", "match": "Pakistan Vs Bangladesh", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "4.0", "maiden": "0", "runs": "22", "wickets": "4", "economy": "5.50", "0s": "14", "4s": "2", "6s": "0", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_25", "match": "New Zealand Vs Pakistan", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "4.0", "maiden": "0", "runs": "24", "wickets": "2", "economy": "6.00", "0s": "12", "4s": "2", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "bowlingTeam": "Pakistan", "bowlerName": "Shaheen Shah Afridi", "overs": "2.1", "maiden": "0", "runs": "13", "wickets": "1", "economy": "6.00", "0s": "7", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},

    # Shadab Khan (11 wickets, Economy 6.31)
    {"match_id": "T20I_07", "match": "India Vs Pakistan", "bowlingTeam": "Pakistan", "bowlerName": "Shadab Khan", "overs": "4.0", "maiden": "0", "runs": "21", "wickets": "0", "economy": "5.25", "0s": "12", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_14", "match": "Pakistan Vs Zimbabwe", "bowlingTeam": "Pakistan", "bowlerName": "Shadab Khan", "overs": "4.0", "maiden": "0", "runs": "23", "wickets": "3", "economy": "5.75", "0s": "13", "4s": "1", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_19", "match": "Pakistan Vs South Africa", "bowlingTeam": "Pakistan", "bowlerName": "Shadab Khan", "overs": "2.0", "maiden": "0", "runs": "16", "wickets": "2", "economy": "8.00", "0s": "6", "4s": "1", "6s": "1", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_23", "match": "Pakistan Vs Bangladesh", "bowlingTeam": "Pakistan", "bowlerName": "Shadab Khan", "overs": "4.0", "maiden": "0", "runs": "30", "wickets": "2", "economy": "7.50", "0s": "9", "4s": "2", "6s": "1", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_27", "match": "Pakistan Vs England", "bowlingTeam": "Pakistan", "bowlerName": "Shadab Khan", "overs": "4.0", "maiden": "0", "runs": "20", "wickets": "1", "economy": "5.00", "0s": "11", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},

    # Anrich Nortje (11 wickets, Economy 5.37)
    {"match_id": "T20I_12", "match": "South Africa Vs Bangladesh", "bowlingTeam": "South Africa", "bowlerName": "Anrich Nortje", "overs": "3.3", "maiden": "0", "runs": "10", "wickets": "4", "economy": "2.86", "0s": "15", "4s": "1", "6s": "0", "wdes": "0", "noballs": "0"},
    {"match_id": "T20I_16", "match": "India Vs South Africa", "bowlingTeam": "South Africa", "bowlerName": "Anrich Nortje", "overs": "4.0", "maiden": "0", "runs": "23", "wickets": "1", "economy": "5.75", "0s": "13", "4s": "2", "6s": "0", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_19", "match": "Pakistan Vs South Africa", "bowlingTeam": "South Africa", "bowlerName": "Anrich Nortje", "overs": "4.0", "maiden": "0", "runs": "41", "wickets": "4", "economy": "10.25", "0s": "11", "4s": "3", "6s": "2", "wdes": "2", "noballs": "0"},
    {"match_id": "T20I_22", "match": "South Africa Vs Netherlands", "bowlingTeam": "South Africa", "bowlerName": "Anrich Nortje", "overs": "4.0", "maiden": "0", "runs": "10", "wickets": "1", "economy": "2.50", "0s": "16", "4s": "0", "6s": "0", "wdes": "0", "noballs": "0"},

    # Sikandar Raza (Zimbabwe all-rounder, 10 wickets)
    {"match_id": "T20I_04", "match": "Zimbabwe Vs Ireland", "bowlingTeam": "Zimbabwe", "bowlerName": "Sikandar Raza", "overs": "3.0", "maiden": "0", "runs": "22", "wickets": "1", "economy": "7.33", "0s": "8", "4s": "2", "6s": "0", "wdes": "1", "noballs": "0"},
    {"match_id": "T20I_14", "match": "Pakistan Vs Zimbabwe", "bowlingTeam": "Zimbabwe", "bowlerName": "Sikandar Raza", "overs": "4.0", "maiden": "0", "runs": "25", "wickets": "3", "economy": "6.25", "0s": "11", "4s": "1", "6s": "1", "wdes": "0", "noballs": "0"}
]
df_bowling = pd.DataFrame(bowling_records)
df_bowling.to_csv(os.path.join(RAW_DIR, 'bowling_raw.csv'), index=False)

print("Raw data generation completed successfully in data/raw/")
