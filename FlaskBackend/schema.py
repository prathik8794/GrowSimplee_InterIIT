from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
from bson import json_util

url = "mongodb url"
client = MongoClient(url)

db = client["Cluster0"]

driver_schema = {
    "productID": {
        "type": "list",
        "minlength": 1,
        "required": True
    },
    "Address": {
        "type": "list",
        "minlength": 1,
        "required": True
    },
    "locations": {
        "type": "list",
        "required": False
    },
    "driverid": {

        "type": "string",
        "minlength": 1,
        "required": True

    },
    "drivername": {

        "type": "string",
        "minlength": 1,
        "required": True
    }

}

post_route_schema = {
    "Time-Taken": {
        "type": "float",
        "required": True
    },
    "Drivername": {
        "type": "string",
        "minlength": 1,
        "required": True
    },
    "DriverID": {
        "type": "string",
        "minlength": 1,
        "required": True
    },
    "DistanceTravelled": {
        "type": "float",
        "required": True
    },
    "source_coord": {
        "type": {
            "lat": {
                "type": "float",
                "required": True
            },
            "lng": {
                "type": "float",
                "required": True
            }
        },
        "required": True
    },
    "destination_coord": {
        "type": {
            "lat": {
                "type": "float",
                "required": True
            },
            "lng": {
                "type": "float",
                "required": True
            }
        },
        "required": True
    }
}

collection = db["driver_data"]


def add_driver_data(pdtid, address, loc, driverphone, drivername):
    collection.insert_one({
        "productID": pdtid,
        "Address": address,
        "locations": loc,
        "driverid": driverphone,
        "drivername": drivername
    })


route_collection = db["route_data"]


def add_route_data(time, driverphone, drivername, dist, src, dest):
    route_collection.insert_one({
        "Time-Taken": time,
        "DriverID": driverphone,
        "Drivername": drivername,
        "DistanceTravelled": dist,
        "source_coord": src,
        "destination_coord": dest
    })


driver_id_collection = db["driver_id_data"]


def add_driver_Id(driverid, drivername):
    driver_id_collection.insert_one({
        "driverid": driverid,
        "drivername": drivername
    })


volume_collection = db["volume_data"]


def add_volume_info(productId, volume):
    volume_collection.insert_one({
        "productID": productId,
        "volume": volume
    })


def getvolume():

    collection = db["volume_data"]
    cursor = collection.find({})
    documents = list(cursor)
    json_documents = json.loads(json_util.dumps(documents))
    print(json_documents)
    return json_documents


def getdriver(number):

    collection = db["driver_data"]
    # Define the search parameter
    search_parameter = {"driverid": str(number)}

    # Query the collection and get the results
    cursor = collection.find(search_parameter)
    documents = list(cursor)
    json_documents = json.loads(json_util.dumps(documents))
    print(json_documents)

    return json_documents


def getroute(number):

    collection = db["route_data"]

    # Define the search parameter
    search_parameter = {"DriverID": number}

    # Query the collection and get the results
    cursor = collection.find(search_parameter)
    documents = list(cursor)
    json_documents = json.loads(json_util.dumps(documents))
    print(json_documents)

    return json_documents


def getdriverid():
    collection = db["driver_id_data"]
    cursor = collection.find({})
    documents = list(cursor)
    json_documents = json.loads(json_util.dumps(documents))
    print(json_documents)
    return json_documents
