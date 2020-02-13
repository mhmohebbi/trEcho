import pprint
import json
import requests
from math import asin,cos,pi,sin,atan2,acos
from datetime import datetime, timedelta
from flask import Flask, jsonify, session, redirect, abort, url_for, render_template, request, flash

app = Flask(__name__)

search_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
key = "&key=AIzaSyAoJQiNhaHcqKJjh97ie8mDM3Fc5qw6UDI"

@app.route("/", methods=["GET", "POST"])
def retreive():
    return render_template('layout.html') 

def timeJson(lat1, lon1, lat2, lon2):
    search_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    origin1 = "origins="+str(lat1)+','+str(lon1)
    dest1 = "&destinations="+str(lat2)+','+str(lon2)
    search_req = requests.get(search_url + origin1 + dest1 + key)
    search_json = search_req.json()
    if search_json['rows'][0]['elements'][0]['status'] != 'OK':
        return None
    else:
        secs = search_json['rows'][0]['elements'][0]['duration']['value']
        future = datetime.now() + timedelta(seconds=secs)
        #future.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        am = False
        if int(future.strftime("%H")) < 12:
            am = True
        future = future.strftime("Your package will arrive on %B %d %Y at %H:%M")
        if am:
            return future + " am"
        else:
            return future + " pm"


def distJson (search_json):
    dist = int(search_json['rows'][0]['elements'][0]['distance']['value'])/1000
    return dist


rEarth = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality


def deg2rad(angle):
    return angle*pi/180


def rad2deg(angle):
    return angle*180/pi


def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rbearing = deg2rad(bearing)
    rdistance = distance / rEarth # normalize linear distance to radian angle

    rlat = asin( sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return (lat, lon)

def latlonBearing(lat1, lon1, lat2, lon2):
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rlat2 = deg2rad(lat2)
    rlon2 = deg2rad(lon2)
    search_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    origin1 = "origins="+str(lat1)+','+str(lon1)
    dest1 = "&destinations="+str(lat2)+','+str(lon2)
    search_req = requests.get(search_url + origin1 + dest1 + key)
    search_json = search_req.json()

    if search_json['rows'][0]['elements'][0]['status'] != 'OK':
        return None

    dist = distJson(search_json) / rEarth
    brng = acos((sin(rlat1)*cos(dist) - sin(rlat2))/cos(rlat1)*sin(dist))
    return rad2deg(brng)

def latlon2city(lat, lon, isCity):
    search_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    latlon = "latlng="+str(lat)+','+str(lon)
    search_req = requests.get(search_url + latlon + key)
    search_json = search_req.json()
    #pprint.pprint(search_json)
    if isCity is False:
        address = search_json['results'][0]['formatted_address']
    else:
        for component in search_json['results'][0]['address_components']:
            if component['types'][0] == "locality":
                address = component['long_name']

    return address

@app.route('/predict-package', methods=['POST', 'GET'])
def predict(package):
    startlat = package["origin"][0]
    startlon = package["origin"][1]
    name = package["description"]

    endlat = package["destination"][0]
    endlon = package["destination"][1]

    hrs = package['last_request'][0]
    dist = 100*hrs # d = vt

    last_loc_lat = package['last_location'][0]
    last_loc_lon = package['last_location'][1]

    bearing = latlonBearing(last_loc_lat, last_loc_lon, endlat, endlon)

    curr_location = pointRadialDistance(last_loc_lat, last_loc_lon, bearing, dist) #(lat, lon)
    ret_str =  "Your " + name + " Package from " + latlon2city(startlat, startlon, True) + " is currently at " + latlon2city(curr_location[0], curr_location[1], False) + '. ' + timeJson(curr_location[0], curr_location[1], endlat, endlon) + '.'
    return ret_str

if __name__ ==  "__main__":
    app.run(debug=True)
    
# dic =  [
#         {
#             "description": "Apple MacBook Pro 2019",
#             "origin": [43.676350, -79.384152], 
#             "destination": [45.422963, -75.684919], 
#             "last_request": [2.034], 
#             "last_location": [44.913468, -76.024684] 
#         },
#         {
#             "description": "Alexo Echo Dot",
#             "origin": [49.897619, -97.069013], 
#             "destination": [46.295149, -79.451957], 
#             "last_request": [8.575], 
#             "last_location": [48.628141, -90.057692] 
#         },
#         {
#             "description": "Adidas Shoes",
#             "origin": [45.502653, -73.580076], 
#             "destination": [43.453437, -80.497555], 
#             "last_request": [.302],
#             "last_location": [43.720872, -79.785269] 
#         },
#     ]

# import time
# for item in dic:
#     time.sleep(1)
#     print(predict(item))
#     print('')

# print(pointRadialDistance(45.502653, -73.580076, 89.8212206629, 3100))
# print(latlonBearing(45.502653, -73.580076, 43.453437, -80.497555))
# print(latlon2city(45.3432, -75.4321214))