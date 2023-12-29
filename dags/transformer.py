import json
import pandas as pd
from pandas import DataFrame, json_normalize
import datetime as dt

def transform_Mitsubishi(im_json : str):
    
    print(im_json)

    # load the string into a json object
    api_json = json.loads(im_json)

    # normalize data
    normalized = json_normalize(api_json)

    # Create a column with the time from the system
    normalized['timestamp'] = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+02:00')     

    # create a new json with the info
    ex_json = DataFrame.to_json(normalized, orient='records')

    return ex_json