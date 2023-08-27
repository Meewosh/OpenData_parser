import requests
import urllib
import json

api_key = 'b2e1d923-55d7-48b4-872a-6ddcf3d34b25' # API key for authentication (personal)
resource_id	=  'f2e5503e-927d-4ad3-9500-4ab9e55deb59'
type = 0

def response_get(type):
    query = "?resource_id=%s&apikey=%s&type=%s" % (resource_id, api_key, type)
    url = "https://api.um.warszawa.pl/api/action/busestrams_get/" + query
    fileobj =  urllib.request.urlopen(url)
    obj = json.load(fileobj)
    return obj


def response_get_vehicle(type, vehicle):
    query = "?resource_id=%s&apikey=%s&type=%s&line=%s" % (resource_id, api_key, type, vehicle)
    url = "https://api.um.warszawa.pl/api/action/busestrams_get/" + query
    fileobj =  urllib.request.urlopen(url)
    obj = json.load(fileobj)
    return obj


def response_parse(response, iterator, keys, recordNumber):
    record = {
        recordNumber:{
            "lastUpdate": response['result'][iterator]['%s' % keys[0]],
            "lineNumber": response['result'][iterator]['%s' % keys[1]],
            "sideNumber": response['result'][iterator]['%s' % keys[2]],
            "delay": "",
            "route": "",
            "latitude": response['result'][iterator]['%s' % keys[3]],
            "longitude": response['result'][iterator]['%s' % keys[4]]
        }
    }
    return record


def data_parser(type, vehicle, limit):
    keys = ['Time', 'Lines', 'VehicleNumber', 'Lat', 'Lon']
    record = ""
    records = {}
    iterator = 0

    if vehicle == None:
        response = response_get(type)
    else:
        response = response_get_vehicle(type, vehicle)


    for recordNumber in range(len(response['result'])):
        record = response_parse(response, iterator, keys, recordNumber)

        records.update(record)
        iterator = iterator + 1

        if limit != None:
            if len(records) == int(limit):
                break
    

    return records