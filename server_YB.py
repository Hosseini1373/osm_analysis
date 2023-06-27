# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 13:34:17 2022

@author: Ahmad Hosseini, Yves Bähler
"""
import math

from flask import Flask ,jsonify
from flask_cors import CORS
from os import path, walk
from pymongo import MongoClient
import numpy as np
import requests
import json
import http.client, urllib.parse

# Global Variables

# read in Database, connect to it.
requesting = []
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.Softwareproj3
nodes = db.SP3


extra_dirs = ['templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
                print(extra_dir)

app = Flask(__name__, static_folder = 'templates')
cors = CORS(app)

# takes in a religion argument, returns amount of chosen religion
def query_religion(rel):
    i=0
    for node in nodes.find({"religion":rel},{"name":1,"_id":0}):
        i+=1
    return i

# takes in a amenity argument, followed by optional religion argument. Returns amount for chosen parameters
def query_amenity(amen,relig=""):
    if (relig==""):
        i=0
        for node in nodes.find({"amenity":amen},{"name":1,"_id":0}):
            i+=1
        return i
    else:
        i=0
        for node in nodes.find({"amenity":amen,"religion":relig},{"name":1,"_id":0}):
            i+=1
        return i

# returns distinct values for a given amenity.
# Takes in chosen amenity.
# Only works for place_of_worship or other values which include religion as an attribute.
def query_amenity_distinct(amen):
    amen_distinct=[]
    for node in nodes.find({"amenity":amen},{"name":1,"_id":0}).distinct("religion"):
        amen_distinct.append(node)  
    return amen_distinct 

# takes in amenity, returns the count for said amenity based on religious archetypes.
def amenity_distribution(amen):
    amenity_distinct=query_amenity_distinct(amen)  
    count_of_amenity={}
    for category in amenity_distinct:
        count_of_amenity[category]=query_amenity(amen,category)
    return count_of_amenity

# takes in amenity, finds the minimum and maximum distance objects of said amenity,
# returns the distance as arbitrary value(lon/lat-dist),
# and the two objects representing min/max values.
def dist_calc(amenity = ''):
    max_dist = 0
    node_min = {'lon': float('inf'), 'lat':float('inf')} #initialize nodes with max values
    node_max = {'lon': float('-inf'), 'lat':float('-inf')} #initialize nodes with min values
    if amenity == '':
        for node in nodes.find():
            #print(type(node['lon']))
            if node['lon'] == '-inf' or node['lat'] == '-inf' or node['lon'] == 'inf' or node['lat'] == 'inf':
                pass
            #check min
            elif float(node['lon']) < float(node_min['lon']) and float(node['lat']) < float(node_min['lat']): #both true, no check
                node_min = node

            elif float(node['lon']) < float(node_min['lon']) and float(node['lat']) > float(node_min['lat']) or float(node['lon']) > float(node_min['lon']) and float(node['lat']) < float(node_min['lat']): #one is larger, other smaller, further check required
                if float(node['lon'])+float(node['lat']) > float(node_min['lon'])+float(node_min['lat']):
                    pass
                else:
                    node_min = node

            #check max
            if node['lon'] == '-inf' or node['lat'] == '-inf' or node['lon'] == 'inf' or node['lat'] == 'inf':
                pass
            elif float(node['lon']) > float(node_max['lon']) and float(node['lat']) > float(node_max['lat']): #both true, no check
                node_max = node

            elif float(node['lon']) < float(node_max['lon']) and float(node['lat']) > float(node_max['lat']) or float(node['lon']) > float(node_max['lon']) and float(node['lat']) < float(node_max['lat']): #one is larger, other smaller, further check required
                if float(node['lon']) + float(node['lat']) > float(node_min['lon']) + float(node_min['lat']):
                    pass
                else:
                    node_max = node
    else:
        for node in nodes.find({"amenity": amenity}):
            if node['lon'] == '-inf' or node['lat'] == '-inf' or node['lon'] == 'inf' or node['lat'] == 'inf': #necessary, otherwise the function fails.
                pass
            # check min
            elif float(node['lon']) < float(node_min['lon']) and float(node['lat']) < float(
                    node_min['lat']):  # both true, no check
                node_min = node

            elif float(node['lon']) < float(node_min['lon']) and float(node['lat']) > float(node_min['lat']) or float(
                    node['lon']) > float(node_min['lon']) and float(node['lat']) < float(
                    node_min['lat']):  # one is larger, other smaller, further check required
                if float(node['lon']) + float(node['lat']) > float(node_min['lon']) + float(node_min['lat']):
                    pass
                else:
                    node_min = node

            # check max
            if node['lon'] == '-inf' or node['lat'] == '-inf' or node['lon'] == 'inf' or node['lat'] == 'inf':
                pass
            elif float(node['lon']) > float(node_max['lon']) and float(node['lat']) > float(
                    node_max['lat']):  # both true, no check
                node_max = node

            elif float(node['lon']) < float(node_max['lon']) and float(node['lat']) > float(node_max['lat']) or float(
                    node['lon']) > float(node_max['lon']) and float(node['lat']) < float(
                    node_max['lat']):  # one is larger, other smaller, further check required
                if float(node['lon']) + float(node['lat']) > float(node_min['lon']) + float(node_min['lat']):
                    pass
                else:
                    node_max = node

    difference = (float(node_max['lon'])-float(node_min['lon']))+(float(node_max['lat'])-float(node_min['lat']))
    #convert to kilometers in lon_lat_to_km() function
    return difference, node_min, node_max

def distance_place_worship():
    response = jsonify(dist_calc())
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Takes in amenity, returns amenity, its longititudes, latitudes as json list.
def return_amenity_long_lat(amen):
    res_json=[]
    for node in nodes.find({"amenity":amen},{"lat":1,"lon":1,"name":1,"_id":0}):
       res_json.append(node)
    return res_json

# Reverse geocode using the service from positionstack. One time use, here for completions sake.
def rev_geocode(amenity):
    api_key = '6701141b24e38073ece9164dd636491f'
    try:

        for node in nodes.find():
            link = 'http://api.positionstack.com/v1/forward?access_key=6701141b24e38073ece9164dd636491f&query={},{}&output=json'.format(node['lat'], node['lon'])
            if node['amenity'] == amenity:
                response = requests.get(link)
                conn = http.client.HTTPConnection('api.positionstack.com')

                params = urllib.parse.urlencode({
                    'access_key': '6701141b24e38073ece9164dd636491f',
                    'query': '{},{}'.format(node['lat'], node['lon']),
                })

                conn.request('GET', '/v1/reverse?{}'.format(params))
                res = conn.getresponse()
                data = res.read()
                data = data.decode('latin')

                data = json.loads(data)['data']
                db.SP3.update({"_id": node["_id"]}, {"$set": {"county": data[0]['county']}})
                print(node)
    except:
        pass

# Takes in no arguments, returns a Json dictionary for the city Zürich with the predefined amenities and their occurence in the city.
def city_amenities():
    res = {}
    counties = 'Zurich'
    amens = ['atm', 'toilets', 'place_of_worship', 'post_office', 'kindergarten']
    temp2 = {}
    for amenity in amens:
            temp = nodes.find({'$and':[{'amenity' : amenity},{"county": counties}]}).limit(10000)
            temp = temp.count(True)
            temp2[amenity] = temp
            res[counties] = temp2

    return (json.dumps(res))

# Takes in no arguments, returns json list with ID and name, used for the amenity list in the website.
def amenities():
    res_json=[]
    ids=0
    for node in nodes.find({},{"amenity":1,"_id":0}).distinct("amenity"):
        prop={}
        prop["Id"]=str(ids)
        prop["Name"]=node
        res_json.append(prop)
        ids+=1
    return res_json

# Calls to/from server below.

@app.route('/test', methods=['GET'])
def hello_world():
    response = jsonify(amenity_distribution("place_of_worship"))
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Calculate the Distance between two points in Kilometers.
# After the function call dist_calc(), which returns the distance in longitude, latitude and both values.
# These values are then transformed with the function test_latcalc.
# takes in amenity, returns value in KM for min/max of chosen amenity.
@app.route('/dist_place_worship', methods=['GET'])
def lon_lat_to_km(amenity = ''):
    if amenity == '':
        x, p1, p2 = dist_calc()
        print(p1)
        print(p2)
        p1_lat = float(p1['lat']) #min
        p1_lon = float(p1['lon'])
        p2_lat = float(p2['lat']) #max
        p2_long =  float(p2['lon'])
        R = 6371 #kmeter
        phi1 = p1_lat * np.pi/180
        phi2 = p2_lat * np.pi/180
        delta_phi = (p2_lat - p2_lat) * np.pi/180
        delta_lambda = (p2_long - p1_lon)*np.pi/180
        a = (np.sin(delta_phi/2) * np.sin(delta_phi/2) +
             np.cos(phi1)* np.cos(phi2) * np.sin(delta_lambda / 2) * math.sin(delta_lambda/2))
        c = 2 * math.atan2(np.sqrt(a), np.sqrt(1-a))
        d = R*c
        return d
    else:
        x, p1, p2 = dist_calc(amenity)
        print(p1)
        print(p2)
        p1_lat = float(p1['lat']) #min
        p1_lon = float(p1['lon'])
        p2_lat = float(p2['lat']) #max
        p2_long =  float(p2['lon'])
        R = 6371 #kmeter
        phi1 = p1_lat * np.pi/180
        phi2 = p2_lat * np.pi/180
        delta_phi = (p2_lat - p2_lat) * np.pi/180
        delta_lambda = (p2_long - p1_lon)*np.pi/180
        a = (np.sin(delta_phi/2) * np.sin(delta_phi/2) +
             np.cos(phi1)* np.cos(phi2) * np.sin(delta_lambda / 2) * math.sin(delta_lambda/2))
        c = 2 * math.atan2(np.sqrt(a), np.sqrt(1-a))
        d = R*c
        return int(d)

# calls function amenity_distribution(), returns the response as json, further processed on HTML-Side.
@app.route('/bar', methods=['GET'])
def barchart():
    response = jsonify(amenity_distribution("place_of_worship"))
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# calls function map_coords(), returns the response as json, further processed on HTML-Side.
@app.route('/map/<amenity>', methods=['GET'])
def map_coords(amenity="place_of_worship"):
    res_json={"coords":return_amenity_long_lat(amenity)}
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# calls function amenities(), returns the response as json, further processed on HTML-Side.
@app.route('/amenities', methods=['GET'])
def amenities_array():
    res_json=amenities()
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# calls function city_amenities(), returns the response as json, further processed on HTML-Side.
@app.route('/city_amen', methods=['GET'])
def city_amen():
    res_json=city_amenities()
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# calls function lon_lat_to_km(), returns the response as json, further processed on HTML-Side.
@app.route('/distance/<amenity>', methods=['GET'])
def distance(amenity="place_of_worship"):
    res_json={"distance":lon_lat_to_km(amenity)}
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='localhost',port=5000, debug=True, extra_files=extra_files)
