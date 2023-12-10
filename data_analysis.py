import json
import psycopg2
import requests
import math

DB_HOST = 'localhost'
DB_NAME = 'population'
DB_USER = 'postgres'
DB_PASSWORD = 'Diana@24.08'
url = "postgresql://postgres:Diana@24@localhost:5432/population"
headers = {'Content-Type': 'application/json'}

def get_population(location):
    conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
    )
    cursor = conn.cursor()
    cursor.execute("SELECT population FROM population WHERE city_ascii = %s", (location,))
    rows = cursor.fetchall()
    #data = json.dumps(rows)
    #response = requests.post(url, data=data, headers=headers)
    return rows

def compute_median(locations):
    lat_med = 0
    lng_med = 0
    length = len(locations)
    for location in locations:
        if location["latitude"] is None or location["longitude"] is None:
            length -= 1
            continue
        lat_med = lat_med + location["latitude"]
        lng_med = lng_med + location["longitude"]
    if length == 0:
        return 200, 200
    lat_med /= length
    lng_med /= length
    return lat_med, lng_med

def get_max_distance(locations):
    max_distance = 0
    for location in locations:
        if location["latitude"] is None or location["longitude"] is None:
            continue
        for location2 in locations:
            if location2["latitude"] is None or location2["longitude"] is None:
                continue
            distance = math.sqrt((location["latitude"] - location2["latitude"]) * (location["latitude"] - location2["latitude"]) + (location["longitude"] - location2["longitude"]) * (location["longitude"] - location2["longitude"]))
            if distance > max_distance:
                max_distance = distance
    return max_distance

def get_possible_locations(lat_med, lng_med, radius):
    conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
    )
    cursor = conn.cursor()
    cursor.execute("SELECT city_ascii FROM population WHERE lat <= %s AND lat >= %s AND lng <= %s AND lng >= %s", (lat_med + radius,lat_med - radius, lng_med + radius, lng_med - radius))
    rows = cursor.fetchall()
    cursor.execute("SELECT country FROM population WHERE lat <= %s AND lat >= %s AND lng <= %s AND lng >= %s", (lat_med + radius,lat_med - radius, lng_med + radius, lng_med - radius))
    rows2 = cursor.fetchall()
    cursor.execute("SELECT population FROM population WHERE lat <= %s AND lat >= %s AND lng <= %s AND lng >= %s", (lat_med + radius,lat_med - radius, lng_med + radius, lng_med - radius))
    rows3 = cursor.fetchall()
    jason = []
    for i in range(len(rows)):
        json1 = {
            "city": rows[i][0],
            "country": rows2[i][0],
            "population": rows3[i][0]
        }
        jason.append(json.dumps(json1))

    return jason

def get_locations(json):
    # code to get locations from json
    locations = json["locations"]
    return locations

def get_category(json):
    # code to get business tags from json
    business_tags = json["main_business_category"]
    return business_tags

def get_num_of_competitors(competitors):
    # code to get number of competitors from json
    num_of_competitors = competitors["count"]
    return num_of_competitors