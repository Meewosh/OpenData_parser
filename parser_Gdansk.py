import requests


def response_get():
    response = requests.get("https://ckan2.multimediagdansk.pl/gpsPositions?v=2").json()
    return response


def response_parse(response, iterator, keys, recordNumber):
    record = {
        recordNumber:{
            "lastUpdate": response['vehicles'][iterator]['%s' % keys[0]],
            "lineNumber": response['vehicles'][iterator]['%s' % keys[1]],
            "sideNumber": response['vehicles'][iterator]['%s' % keys[2]],
            "delay": response['vehicles'][iterator]['%s' % keys[3]],
            "route": response['vehicles'][iterator]['%s' % keys[4]],
            "latitude": response['vehicles'][iterator]['%s' % keys[5]],
            "longitude": response['vehicles'][iterator]['%s' % keys[6]]
        }
    }
    return record


def dataParser(limit, lineNumber):
    keys = ['generated', 'routeShortName', 'vehicleCode', 'delay', 'headsign',  'lat', 'lon']
    record = ""
    records = {}
    iterator = 0
    response = response_get()
    
    for recordNumber in range(len(response['vehicles'])):
        record = response_parse(response, iterator, keys, recordNumber)
        
        if lineNumber == None or record[recordNumber]['lineNumber'] == lineNumber:
            records.update(record)
            
        iterator = iterator + 1
        if limit != None:
            if int(limit) == len(records):
                return records 
            
    return records