import pandas as pd
import matplotlib.pyplot as plt

import requests
import logging
import io
import folium
#import urllib


from pathlib import Path

data_folder = Path("../LandWaterContentData/")
apikey = "c9f1fcccdac44031a945633ce6df8da3"

latitude = "15.5"
longitude = "-15.5"
#latitude, longitude = lat_long_rounding(latitude, longitude)

area_of_interest = folium.Map(location = [latitude, longitude], zoom_start= 10.5, control_scale=True)
folium.Marker(latitude, longitude).add_to(area_of_interest)
# TODO: Need to figure out how to mae this into a pop up
#area_of_interest.save("area_of_interest.html")
#urllib.urlopen("area_of_interest.html") Look at my German python file to remind myself how to do this
count="1000"

filename = f"Lat{latitude}Lon{longitude}Count{count}.csv"
filepath = data_folder.joinpath(filename)
df = pd.read_csv(filepath)

plt.plot(pd.to_datetime(df["axis:time"]), df["data:Water_Thickness"])
plt.show()