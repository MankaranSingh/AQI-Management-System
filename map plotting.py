from gmplot import gmplot
import pandas as pd

df = pd.read_csv('Dummy_AQI.txt', names = ['timestamp','lat','lon','state','city','area','AQI','humidity', 'temp', 'CO','NO2','O3','PM10','PM25','SO2'])

means = df[['lat','lon','AQI','area']].groupby('area').mean()

gmap = gmplot.GoogleMapPlotter(22.002066, 78.065544,5)
gmap.apikey = ''
gmap.scatter(means.lat,means.lon, 'red', size=200, marker=False)
gmap.draw("my_map.html")
