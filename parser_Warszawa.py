import requests
import json

api_key = 'aeec556e-6dce-4697-80af-6814e1a40abc' # API key for authentication (personal)
resource_id	=  'f2e5503e-927d-4ad3-9500-4ab9e55deb59'
type = 0

def response_get(type):
    query = "/?resource_id=%s&apikey=%s&type=%s" % (resource_id, api_key, type)
    response = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get" + query)
    print("wywołanie 1")
    return response


def response_get_vehicle(type, vehicle):
    query = "?resource_id=%s&apikey=%s&type=%s&line=%s" % (resource_id, api_key, type, vehicle)
    response = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get" + query)
    print("wywołanie 2")
    return response


def response_parse(response, iterator, keys, recordNumber):
    print("Przed parsowaniem")
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
    print("Po parsowaniu")
    return record


def dataParser(type, vehicle, limit):
    keys = ['Time', 'Lines', 'VehicleNumber', 'Lat', 'Lon']
    record = ""
    records = {}
    iterator = 0
    print("Przed wywpłaniem")
    if vehicle == None:
        response = response_get(type)
    else:
        response = response_get_vehicle(type, vehicle)
    
    print("Po wywołaniu")
    if response.status_code == 500:
        return records
    response = json.loads(response.text)

    for recordNumber in range(len(response['result'])):
        print("Wywolanie parsowania")
        record = response_parse(response, iterator, keys, recordNumber)

        records.update(record)
        print("Przypisanie")
        
        iterator = iterator + 1

        if limit != None:
            if len(records) == int(limit):
                break
    

    return records