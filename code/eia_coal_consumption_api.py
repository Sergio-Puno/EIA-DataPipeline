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

# Import data dump file paths from file
data_path = ref_file['data_path']
log_path = ref_file['log_path']

# Import state abbreviations for API URL building
# Not all states are represented in the EIA database, only pulling for what is available
date_abbr = pd.read_csv(parent_dir + '/state_abbr.csv', dtype={'state': 'string', 'abbr': 'string'})

# Build padd keys for API call with based key + state abbr
padd_keys = ['ELEC.CONS_TOT.COW-' + x + '-98.M' for x in date_abbr['abbr']]

# Function to clean the dataframe and return a clean dataframe back to the loop
def clean_dataframe(df):
    # Add state of report to dataframe
    df['state'] = re.search('ELEC.CONS_TOT.COW-(.*)-98.M', padd_keys[i]).group(1)

    # Convert the year-month date into full datetime using last day of month
    df['date'] = pd.to_datetime(df['date'], format='%Y%m') + MonthEnd(1)

    # Rename columns
    df.rename(columns={'date': 'report_date', padd_keys[i]: 'coal_consumption'}, inplace=True)

    # Replace consumption NULL values to 0 value
    df['coal_consumption'].fillna(0.0, inplace=True)

    return df

# Write raw data file to data storage
def generate_data_file(json_data, file):
    filename_data = 'coal_consumption_monthly_data_' + file + '_' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.json'
    data_complete_name = os.path.join(data_path, filename_data)

    print('---Writing raw data file:', type(json_data), '::', data_complete_name)

    with open(data_complete_name, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return data_complete_name

# Write file metadata to log storage
def generate_log_file(metadata, file):
    filename_logs = 'coal_consumption_monthly_logs' + file + '_' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.json'
    log_complete_name = os.path.join(log_path, filename_logs)

    print('---Writing log data file:', type(metadata), '::', log_complete_name)

    with open(log_complete_name, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

def write_dataframe_to_table(df, conn, file):

    insert_array = list(df.itertuples(index=False, name=None))
    sql_update_query = """INSERT INTO state_consumption (report_date, coal_consumption, state) VALUES (%s, %s, %s)"""

    # Process the array
    for j in range(0, len(insert_array)):
        data_tuple = insert_array[j]
        cursor.execute(sql_update_query, data_tuple)

    conn.commit()
    print("File updated to table:", file)

def write_dataframe_to_pkl(df, file):
    pd.to_pickle(df, ref_file['pkl_path'] + '_' + file + 'raw_data.pkl')
    print("Raw CSV dumped to storage:", file)

# Establish database connection
print("Establishing connection to database...")

conn = mysql.connector.Connect(
    host="localhost",
    user="root",
    password=ref_file['mysql_cred'],
    database="coal_consumption"
)

cursor = conn.cursor(prepared=True)

# Testing list
# padd_test = ['ELEC.CONS_TOT.COW-AL-98.M']

# Loop over the padd keys and build the final URL for request
# Pull in the json return data and parse into dataframe
# Write out to individual file, send data to MySQL database
for i in range(len(padd_keys)):

    ######### API Processing #########
    print("############# PROCESSING RECORD", i + 1, "OF", len(padd_keys), "#############")

    # Build URL
    URL = 'https://api.eia.gov/series/?api_key='+ eia_key +'&series_id='+padd_keys[i]

    # Send our API request
    r = requests.get(URL)
    json_data = r.json()

    # Testing-Error Handling
    if r.status_code == 200:
        print('---API Call: SUCCESS---')
    else:
        print('Error', r.status_code)

    ######### DataFrame Creation and Manipulation #########

    # Build DataFrame from API json data
    df = pd.DataFrame(json_data.get('series')[0].get('data'), columns=['date', padd_keys[i]])

    # Data cleaning function
    df_clean = clean_dataframe(df)

    # Write to mysql database table
    write_dataframe_to_table(df_clean, conn, padd_keys[i])

    ######### Write out all files to appropriate folders #########

    # Generate CSV file with dataframe data
    filelocation = generate_data_file(json_data, padd_keys[i])

    # Logging API call success and failure status codes and other meta data to separate file
    metadata = {
        'event_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'statuscode': r.status_code,
        'url_used': URL,
        'datasize': os.path.getsize(filelocation)
    }

    # Generate log file name datetime + 'coal_consumption' --MAKE A FUNCTION--
    generate_log_file(metadata, padd_keys[i])

    # Write out pickle copy of the dataframe
    write_dataframe_to_pkl(df_clean, padd_keys[i])

# Ensure that the connection is closed after the script finishes
if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")