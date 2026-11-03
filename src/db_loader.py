"""
Database Loader: Creates the SQLite database and loads processed CSVs into tables.
"""
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DB_PATH = os.path.join(BASE_DIR, 'cricket_world_cup.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'sql', 'schema.sql')

def load_database():
    db_filename = os.path.basename(DB_PATH)
    print(f"Connecting to SQLite database: {db_filename}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute DDL schema
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, 'r') as f:
            schema_ddl = f.read()
        cursor.executescript(schema_ddl)
        print(" Applied relational schema DDL.")

    # Load tables
    tables = [
        ('dim_matches', 'dim_matches.csv'),
        ('dim_players', 'dim_players.csv'),
        ('fact_batting_summary', 'fact_batting_summary.csv'),
        ('fact_bowling_summary', 'fact_bowling_summary.csv')
    ]

    for table_name, csv_file in tables:
        csv_path = os.path.join(PROC_DIR, csv_file)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f" Loaded {len(df)} records into '{table_name}'")

    conn.commit()
    conn.close()
    print("Database initialization and loading complete!")

if __name__ == '__main__':
    load_database()
