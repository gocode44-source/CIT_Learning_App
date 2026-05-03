import pandas as pd
import sqlite3
import streamlit as st

DB_NAME = "data/progress.db"

def show_progress_chart(username):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM progress WHERE username=?", conn, params=(username,))
    conn.close()

    if not df.empty:
        df['date'] = pd.to_datetime('today')
        chart = df.groupby('date')['xp'].sum()
        st.line_chart(chart)
