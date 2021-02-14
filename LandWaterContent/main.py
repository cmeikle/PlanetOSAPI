import pandas as pd

import requests
import logging
import io

from pathlib import Path

logger = logging.getLogger(__name__)

data_folder = Path("../LandWaterContentData/")

def query_api(apikey:str, latitude:str, longitude:str, count="1000"):
    # Construct the Url to request the dataset
    # TODO: There is a way to pull this down using a Polygon, which may give us more information
    url_csv = f"https://api.planetos.com/v1/datasets/nasa_gldas_lwc_monthly/point?apikey={apikey}&lat={latitude}&origin=dataset-details&lon={longitude}&csv=true&count={count}"
    try:
        r = requests.get(url_csv)
        data = r.content.decode('utf8')
        # Read Csv into pandas
        df = pd.read_csv(io.StringIO(data))
        filename = f"Lat{latitude}Lon{longitude}Count{count}.csv"
        filepath = data_folder.joinpath(filename)
        # And create a csv file in your local directory with the info, so that we don't have to continue querying the API
        df.to_csv(filepath)
    except:
        ## TODO update this exception
        logger.error("Something went wrong")

def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df

if __name__ == "__main__":
    apikey = "c9f1fcccdac44031a945633ce6df8da3&lat"
    # The resolution of this dataset is 1, so it rounds to the .5
    latitude = "-15.5"
    longitude = "15.5"
    # TODO: write a little function that takes in the longitude and latitude 
    # and make sure it is always passed so that the api can read it, ending with .5 possibly
    count = "1000"
    try:
        filename = f"Lat{latitude}Lon{longitude}Count{count}.csv"
        filepath = data_folder.joinpath(filename)
        df = read_csv(filepath)
    except FileNotFoundError:
        logger.info("The file has not been found, this is probably because it has not been run, we will run a request to the API")
        query_api(apikey, latitude, longitude, count)
