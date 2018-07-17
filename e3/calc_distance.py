import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
#Formulas taken from here
def distance(coordinates):  
    myTotal = pd.DataFrame(
        columns = ['total'])
   
    lat1 = coordinates['lat']
    lon1 = coordinates['lon']
    
    lat2 = coordinates.lat.shift(1)
    lon2 = coordinates.lon.shift(1)

    radius = 6371000;
    degLat = (lat2 - lat1)*(np.pi/180)
    degLon = (lon2 - lon1)*(np.pi/180)
    
    a = np.sin(degLat/2) * np.sin(degLat/2) + (np.cos((lat1)*(np.pi/180))) * (np.cos((lat2)*(np.pi/180))) * np.sin(degLon/2) * np.sin(degLon/2)
    formula = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    myTotal['total'] = radius * formula
    total = myTotal['total'].sum()

    return total

def main():
    points = ET.parse(sys.argv[1])
    root = points.getroot()
    coordinates = pd.DataFrame(
            columns = ['lat', 'lon'])
    for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/0}trkpt'):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        latlon = {'lat' : [lat], 'lon' : [lon]}
        df = pd.DataFrame(data = latlon)
        coordinates = coordinates.append(df)
    
    distance(coordinates)
    print('Unfiltered distance: %0.2f' % (distance(coordinates)))
    
    kalman_data = coordinates
    initial_state = kalman_data.iloc[0]

    observation_covariance = np.diag([0.55, 0.55]) ** 2 # TODO: shouldn't be zero
    transition_covariance = np.diag([0.5, 0.5]) ** 2 # TODO: shouldn't be zero
    transition = [[1, 0], [0, 1]] # TODO: shouldn't (all) be zero

    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition
    )
    smoothed_points, _ = (kf.smooth(kalman_data.values))
    smoothed_data = pd.DataFrame(smoothed_points, columns = ['lat', 'lon'])
    print('Filtered distance: %0.2f' % (distance(smoothed_data)))
    output_gpx(smoothed_data, 'out.gpx')


if __name__ == '__main__':
    main()