import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gzip
import difflib
import sys


def divideBy10(float):
	float = float/10.0
	return float

def toKM(float):
	float = float/1000000.0
	return float

#Write a function distance(city, stations) that calculates the distance between one city and every station. You can probably adapt your function from the GPS question last week. [1]
def distance(city, stations):  
    #print(stations)
    #print(city)
    myTotal = pd.DataFrame(
        columns = ['total'])
   
    lat1 = city['latitude']
    lon1 = city['longitude']
    
    lat2 = stations['latitude']
    lon2 = stations['longitude']

    radius = 6371000; #radius of earth
    degLat = (lat2 - lat1)*(np.pi/180)
    degLon = (lon2 - lon1)*(np.pi/180)
    
    a = np.sin(degLat/2) * np.sin(degLat/2) + (np.cos((lat1)*(np.pi/180))) * (np.cos((lat2)*(np.pi/180))) * np.sin(degLon/2) * np.sin(degLon/2)
    formula = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    myTotal['total'] = radius * formula

    return myTotal['total']

def best_tmax(city, stations):
	#myTest = pd.DataFrame(
     #   columns = ['best_tmax'])
	cityDistance = distance(city, stations)
	cityDistance = cityDistance.idxmin()
	#cityDistance = cityDistance.drop_duplicates()
	#myTest['best_tmax'] = stations['avg_tmax'].iloc[cityDistance]
	return (stations['avg_tmax'].iloc[cityDistance])


gzFile = sys.argv[1]
csvFile = sys.argv[2]
output = sys.argv[3]

station_fh = gzip.open(gzFile, 'rt', encoding='utf-8')
stations = pd.read_json(station_fh, lines=True)
cityData = pd.read_csv(csvFile)

stations['avg_tmax'] = stations['avg_tmax'].apply(divideBy10)
cityData = cityData[np.isfinite(cityData['population'])]
cityData = cityData[np.isfinite(cityData['area'])]
cityData['area'] = cityData['area'].apply(toKM)
cityData = cityData[cityData['area'] < 10000]
cityData['density'] = cityData['population'] / cityData['area']

cityData['best_tmax'] = cityData.apply(best_tmax, stations = stations, axis=1)

plt.figure(figsize=(8, 4))
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.title('Temperature vs Population Density')
plt.plot(cityData['best_tmax'], cityData['density'], 'b.', alpha=0.2, label='Original Points')
plt.savefig(output)

#avgTemp = pd.DataFrame(
 #       columns = ['best_tmax'])
#avgTemp['best_tmax'] = cityData.apply(best_tmax, stations = stations)
#print(avgTemp)


#print(stations)
print(cityData)