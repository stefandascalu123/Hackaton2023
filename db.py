import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from psycopg2 import OperationalError
import csv
from psycopg2 import sql

# Replace these values with your PostgreSQL credentials
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'Diana@24.08'

# CSV file path
CSV_FILE = './population.csv'

# PostgreSQL table name
TABLE_NAME = 'population'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {} (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100),
        year INTEGER,
        series VARCHAR(1000),
        value INTEGER,
        source VARCHAR(1000)
    )
""").format(sql.Identifier(TABLE_NAME))
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Read data from CSV and insert into PostgreSQL
with open(CSV_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    next(reader)  # Skip second row
    for row in reader:

        insert_query = sql.SQL("""
            INSERT INTO {} (region, year, series, value, source) VALUES (%s, %s, %s, %s, %s)
        """).format(sql.Identifier(TABLE_NAME))
        cursor.execute(insert_query, (row[1], int(row[2]), row[3], int(float (row[4].replace(',', '')) * 100), row[6]))

# Commit the changes and close the connections
conn.commit()
cursor.close()
conn.close()

print("Data imported successfully.")