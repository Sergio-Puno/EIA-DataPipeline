import requests
import numpy as np
import pandas as pd
import mysql.connector
from pandas.tseries.offsets import MonthEnd
import json
import os
import re
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Import API key from file
ref_file = json.load(open(parent_dir + '/keys/key_info.json'))
eia_key = ref_file['eia_key']

# Import state abbreviations for API URL building
# Not all states are represented in the EIA database, only pulling for what is available
date_abbr = pd.read_csv(parent_dir + '/state_abbr.csv', dtype={'state': 'string', 'abbr': 'string'})

# Build padd keys for API call with based key + state abbr
padd_keys = ['EMISS.CO2-TOTV-CC-TO-' + x + '.A' for x in date_abbr['abbr']]

# Establish database connection
print("Establishing connection to database...")
conn = mysql.connector.Connect(
    host="localhost",
    user="root",
    password=ref_file['mysql_cred'],
    database="coal_consumption"
)

cursor = conn.cursor(prepared=True)

def clean_dataframe(df):
    # Add state of report to dataframe
    df['state'] = re.search('EMISS.CO2-TOTV-CC-TO-(.*).A', padd_keys[i]).group(1)

    # Convert datatypes
    df['data_year'] = pd.to_datetime(df['data_year'], format="%Y")
    df[padd_keys[i]] = df[padd_keys[i]].astype(float)

    # Rename columns
    df.rename(columns={padd_keys[i]: 'co2_emission'}, inplace=True)

    # Replace consumption NULL values to 0 value
    df['co2_emission'].fillna(0.0, inplace=True)

    return df

def write_dataframe_to_table(df, conn, file):
    insert_array = list(df.itertuples(index=False, name=None))
    sql_update_query = """INSERT INTO co2_emissions (data_year, co2_emission, state) VALUES (%s, %s, %s)"""

    # Process the array
    for j in range(0, len(insert_array)):
        data_tuple = insert_array[j]
        cursor.execute(sql_update_query, data_tuple)

    conn.commit()
    print("File updated to table:", file)

for i in range(len(padd_keys)):

    ######### API Processing #########
    print("############# PROCESSING RECORD", i + 1, "OF", len(padd_keys), "#############")

    # Build URL
    URL = 'https://api.eia.gov/series/?api_key='+ eia_key +'&series_id='+padd_keys[i]

    # Send our API request: Try to get for the state, continue otherwise
    try:
        r = requests.get(URL)
        json_data = r.json()
        print('---API Call: SUCCESS---')            
    except:
        print('Skipping:', padd_keys[i])
        continue

    ######### DataFrame Creation and Manipulation #########

    # Build DataFrame from API json data
    df = pd.DataFrame(json_data.get('series')[0].get('data'), columns=['data_year', padd_keys[i]])

    # Data cleaning function
    df_clean = clean_dataframe(df)

    # Write to mysql database table
    write_dataframe_to_table(df_clean, conn, padd_keys[i])

# Ensure that the connection is closed after the script finishes
if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")