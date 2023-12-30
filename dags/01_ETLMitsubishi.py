
# imports Airflow
import pendulum
from airflow.decorators import dag, task

# import modules
import json
import requests
import pandas as pd
from pandas import DataFrame, json_normalize
import datetime as dt
import psycopg2 
import time as t

from transformer import transform_Mitsubishi


# instance DAG
@dag(
    schedule_interval=None,                             
    start_date=pendulum.datetime(2023, 12, 28, tz="UTC"), 
    catchup=False,                                          
    tags=['EmilianoRegazzoni'],                      
)

# define ETL job

def ETLMitsubishi():
    """
    (https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """

    # EXTRACT: Query the info from twelvedata, the endpoint /price which says the price of a share right now
    @task()
    def extract():

        info = {'symbol': 'MSBHF', 'apikey': '6af9514997a34911a0444f72c165da56'}
        r = requests.get("http://api.twelvedata.com/price?", params=info)

        # Get the json
        r_string = r.json()
        print(r_string)
        return r_string
 
    # TRANSFORM: Transform the API response, date and time added to load to database
    @task()
    def transform(mitsubishi_json: json):

        mitsubishi_str = json.dumps(mitsubishi_json)
        transformed_str = transform_Mitsubishi(mitsubishi_str)

        # turn string into dictionary
        ex_dict = json.loads(transformed_str)
        print(ex_dict)
        return ex_dict     

    # Save the data into Postgres database
    @task()
    def load(mitsubishi_data: dict):

        try:
            connection = psycopg2.connect(user="airflow",
                                        password="airflow",
                                        host="postgres",
                                        port="5432",
                                        database="mitsubishi")
            cursor = connection.cursor()
            postgres_insert_query = """INSERT INTO mitsubishi_info (price, timestamp) VALUES ( %s, %s );"""
            print(postgres_insert_query)

            record_to_insert = (mitsubishi_data[0]["price"],mitsubishi_data[0]["timestamp"] ) # let , so python can understand is a record with 1 column
            
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully")

        except (Exception, psycopg2.Error) as error:
            
            print("Failed to insert record into tableeee", error)
            
            if connection:
                cursor.close()
                connection.close()
                print("Connection is closed")
            
            raise Exception(error)

        finally:
            # close db
            if connection:
                cursor.close()
                connection.close()
                print("Connection is closed")

    
    # Defining the flow in Airflow
    mitsubishi_data = extract()
    mitsubishi_summary = transform(mitsubishi_data)
    load(mitsubishi_summary)


# call the DAG
mitsubishi_dag_posgres = ETLMitsubishi()