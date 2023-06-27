# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 13:34:17 2022

@author: Ahmad Hosseini, Yves Bähler
"""


import platform

from flask import Flask, render_template,jsonify
from flask_cors import CORS
from os import path, walk
from pymongo import MongoClient, InsertOne
import json
import pandas as pd






#Database
requesting = []
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.admin
collection = db.osm
if "osm" in db.list_collection_names():  #Check if collection "osm" 
                                        #  exists in db 

    nodes = db['posts']
    if collection.count_documents == 0:   #Check if collection named 'posts' is empty
        f=open(r"osm-output.json")
        for line in f:
            #print(line)
            #print(line.rstrip(',\n'))
            myDict = json.loads(line.rstrip(',\n'))
            #print(myDict)
            requesting.append(InsertOne(myDict))
        
        result = nodes.bulk_write(requesting)
###client.close()







def return_amenity_long_lat(amen):
    res_json=[]
    for node in nodes.find({"amenity":amen},{"lat":1,"lon":1,"name":1,"_id":0}):
       res_json.append(node)
    return res_json

def query_religion(rel):
    i=0
    for node in nodes.find({"religion":rel},{"name":1,"_id":0}):
        i+=1
    print (i)


def query_amenity(amen,relig=""):
    if (relig==""):
        i=0
        for node in nodes.find({"amenity":amen},{"name":1,"_id":0}):
            i+=1
        return i
    else:
        i=0
        if(relig!=""):
            for node in nodes.find({"amenity":amen,"religion":relig},{"name":1,"_id":0}):
                i+=1
            return i


    
def query_amenity_distinct(amen):
    amen_distinct=[]
    for node in nodes.find({"amenity":amen},{"name":1,"_id":0}).distinct("religion"):
        amen_distinct.append(node)  
    return amen_distinct 
    
    
    
#distribution of  amenity
def amenity_distribution(amen):
    amenity_distinct=query_amenity_distinct(amen)  
    count_of_amenity={}
    for category in amenity_distinct:
        count_of_amenity[category]=query_amenity(amen,category)
    return count_of_amenity
    
# query_religion("christian")
# query_amenity("place_of_worship")
#print(amenity_distribution("place_of_worship"))


def amenities():
    res={}
    res_json=[]
    ids=0
    for node in nodes.find({},{"amenity":1,"_id":0}).distinct("amenity"):
       #print(node)
        prop={}
        prop["Id"]=str(ids)
        prop["Name"]=node
        res_json.append(prop)
        ids+=1
    #print(res_json)
    #print(res_json)
    return res_json    




extra_dirs = ['templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
                
app = Flask(__name__, static_folder = 'templates')
cors = CORS(app)

@app.route('/bar', methods=['GET'])
def barchart():
    response = jsonify(amenity_distribution("place_of_worship"))
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/map/<amenity>', methods=['GET'])
def map_coords(amenity="place_of_worship"):
    res_json={"coords":return_amenity_long_lat(amenity)}
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/amenities', methods=['GET'])
def amenities_array():
    res_json=amenities()
    response = jsonify(res_json)
    #to allow cross origin ajax calls:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response






if __name__ == '__main__':
    #amenities()
    app.run(host='localhost',port=5000, debug=True, extra_files=extra_files)