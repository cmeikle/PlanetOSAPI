import pandas as pd

import requests
import logging
import io
import folium


from pathlib import Path

logger = logging.getLogger(__name__)

data_folder = Path("../LandWaterContentData/")


def query_api(apikey:str, latitude:str, longitude:str, count="1000"):
    """
    The API Query - Parameters passed, your api key, latitude, longitude 
    and the number of months you want starting from 2001, default = 1000,
    giving you the full dataset
    """
    # Construct the Url to request the dataset
    # TODO: There is a way to pull this down using a Polygon, which may give us more information
    url_csv = f"https://api.planetos.com/v1/datasets/nasa_gldas_lwc_monthly/point?apikey={apikey}&lat={latitude}&origin=dataset-details&lon={longitude}&csv=true&count={count}"
    try:
        r = requests.get(url_csv)
        data = r.content.decode('utf8')
    except Exception as e:
        logger.error(e)
    # Read Csv into pandas
    # TODO: Something is failing at this point and returning empty dfs, it may be that I have queried the api too much today
    df = pd.read_csv(io.StringIO(data))

    filename = f"Lat{latitude}Lon{longitude}Count{count}.csv"
    filepath = data_folder.joinpath(filename)
    # And create a csv file in your local directory with the info, so that we don't have to continue querying the API
    df.to_csv(filepath)


def lat_long_rounding(latitude, longitude):
    """
    The resolution of this dataset is 1, so we are always querying an average at .5 latitude and longitude
    """
    latitude = latitude.split(".")[0] + ".5"
    longitude = longitude.split(".")[0] + ".5"
    return latitude, longitude

if __name__ == "__main__":
    apikey = "c9f1fcccdac44031a945633ce6df8da3"
    
    latitude = "15.5"
    longitude = "-15.5"
    latitude, longitude = lat_long_rounding(latitude, longitude)

    # area_of_interest = folium.Map(location = [latitude, longitude], zoom_start= 10.5, control_scale=True)
    # # TODO: Need to figure out how to mae this into a pop up
    # area_of_interest
    count="1000"
    try:
        filename = f"Lat{latitude}Lon{longitude}Count{count}.csv"
        filepath = data_folder.joinpath(filename)
        df = pd.read_csv(filepath)
        if df.empty:
            raise("The dataframe is empty, something went wrong when downloading it from the api")
            # TODO: Create a function to remove this datafile from the folder and then query the api
    except FileNotFoundError:
        logger.info("The file has not been found, this is probably because a query of this sort has not been run, we will now query the API")
        query_api(apikey, latitude, longitude, count)
