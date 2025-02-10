from fastapi import Request
import sqlite3
import pandas as pd

def get_client_ip(request: Request):
    return request.client.host

def db_to_csv():
    # Connect to the database
    conn = sqlite3.connect("speed_tests.db")
    
    # Read the table into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM Test", conn)
    
    # Save DataFrame as CSV
    df.to_csv("speed_tests.csv", index=False)
    
    # Close connection
    conn.close()

def db_to_json():
    # Connect to the database
    conn = sqlite3.connect("speed_tests.db")
    
    # Read the table into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM Test", conn)
    
    # Save DataFrame as JSON
    df.to_json("speed_tests.json", orient="records", indent=4)
    
    # Close connection
    conn.close()
