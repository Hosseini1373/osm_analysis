from pymongo import MongoClient, InsertOne
import json

# read in Database, connect to it.
requesting = []
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.Softwareproj3
nodes = db.SP3

# Below: reading in the file, where given osm-data is. The file is then processed, and the values are then input into the DB.
# The DB runs continuously during the server process.

if "osm" in db.list_collection_names():  #Check if collection "osm"
                                        #  exists in db

    nodes = db['posts']
    if nodes.count_documents == 0:   #Check if collection named 'posts' is empty
        f=open(r"osm-output.json")
        for line in f:
            #print(line)
            #print(line.rstrip(',\n'))
            myDict = json.loads(line.rstrip(',\n'))
            #print(myDict)
            requesting.append(InsertOne(myDict))

        result = nodes.bulk_write(requesting)
client.close()
