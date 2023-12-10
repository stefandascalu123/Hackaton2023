import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from psycopg2 import OperationalError
import csv
from psycopg2 import sql

# Replace these values with your PostgreSQL credentials
DB_HOST = 'localhost'
DB_NAME = 'population'
DB_USER = 'postgres'
DB_PASSWORD = 'Diana@24.08'

# CSV file path
CSV_FILE = './worldcities.csv'

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
        city_ascii VARCHAR(1000),
        lat FLOAT,
        lng FLOAT,
        country VARCHAR(1000),
        population FLOAT
    )
""").format(sql.Identifier(TABLE_NAME))
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Read data from CSV and insert into PostgreSQL
with open(CSV_FILE, 'r',encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        if row[9] != '' and float(row[9]) > 200000:
            insert_query = sql.SQL("""
                INSERT INTO {} ( city_ascii, lat, lng, country, population) VALUES (%s, %s, %s, %s, %s)
            """).format(sql.Identifier(TABLE_NAME))
            cursor.execute(insert_query, (row[1], float(row[2]), float(row[3]), row[4], float(row[9])))

# Commit the changes and close the connections
conn.commit()
cursor.close()
conn.close()

print("Data imported successfully.")