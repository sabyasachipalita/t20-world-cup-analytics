"""
Executes the analytical SQL queries against cricket_world_cup.db
and prints out structured tabular outputs.
"""
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'cricket_world_cup.db')
SQL_PATH = os.path.join(BASE_DIR, 'sql', 'analysis_queries.sql')

def run_queries():
    conn = sqlite3.connect(DB_PATH)
    with open(SQL_PATH, 'r') as f:
        sql_content = f.read()

    # Split queries by double dash comments marking each query
    raw_sections = sql_content.split('-- QUERY ')
    
    for section in raw_sections[1:]:
        lines = section.strip().split('\n')
        title = lines[0].strip()
        # Filter out all comment lines and empty lines at top
        query_lines = [l for l in lines[1:] if not l.strip().startswith('--')]
        query_text = '\n'.join(query_lines).strip()
        
        # Remove trailing semicolon for pandas
        if query_text.endswith(';'):
            query_text = query_text[:-1]

        print("\n" + "=" * 75)
        print(f"QUERY {title}")
        print("=" * 75)
        
        try:
            df = pd.read_sql_query(query_text, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Error executing query: {e}")

    conn.close()

if __name__ == '__main__':
    run_queries()
