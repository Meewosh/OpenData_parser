import requests
import json


def response_get(offset):
    response = requests.get("https://www.wroclaw.pl/open-data/api/action/datastore_search?offset=%i&resource_id=17308285-3977-42f7-81b7-fdd168c210a2" % offset)
    return response


def response_parse(response, iterator, keys, record_number):
    # gmaps = googlemaps.Client(key='AIzaSyAbSkiFB85VDcxzdhX1qQVuPLaG-wj2ThI')
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    # https://www.google.com/maps/search/?api=1&query=51.078685760498%2C17.0066871643066

    if str(response['result']['records'][iterator]['%s' % keys[5]]) != "None":
        line_number = str(response['result']['records'][iterator]['%s' % keys[5]])[:3]
        if line_number[:1] == "0":
            line_number = line_number[1:3]
            if line_number[:1] == "0":
                line_number = line_number[1]
    else:
        line_number = response['result']['records'][iterator]['%s' % keys[5]]

    record = {
        record_number:{
            "lastUpdate": response['result']['records'][iterator]['%s' % keys[0]],
            "lineNumber": line_number,
            "sideNumber": response['result']['records'][iterator]['%s' % keys[2]],
            "delay": "",
            "route": "",
            "latitude": response['result']['records'][iterator]['%s' % keys[3]],
            "longitude": response['result']['records'][iterator]['%s' % keys[4]]
        }
    } 
    return record


def offset_value_change(offset):
    offset = offset + 100
    response = response_get(offset)
    return response


def if_change_number_of_record(record, records, record_number, iterator_tmp, line_number):
    if line_number is None:
        records.update(record)
    else:
        record_tmp = {}
        record_tmp[iterator_tmp] = record[record_number]
        records.update(record_tmp)


def data_parser(limit, line_number):
    keys = ['Data_Aktualizacji', 'Nazwa_Linii', 'Nr_Boczny',
            'Ostatnia_Pozycja_Szerokosc', 'Ostatnia_Pozycja_Dlugosc', 'Brygada']
    records = {}
    iterator = 0
    iterator_tmp = 0
    offset = 0
    response = response_get(offset)
    print("Status code: " + str(response.status_code))\
    
    if response.status_code == 500:
        return records
    response = json.loads(response.text)

    total_amount_of_record_before_prase = response['result']['total']

    for recordNumber in range(total_amount_of_record_before_prase):
        record = response_parse(response, iterator, keys, recordNumber)
        
        if line_number is None or record[recordNumber]['lineNumber'] == line_number:
            if_change_number_of_record(record, records, recordNumber, iterator_tmp, line_number)
            iterator_tmp = iterator_tmp + 1
            
        iterator = iterator + 1

        if limit is not None:
            if int(limit) == len(records):
                return records 

        if iterator == 100:
            iterator = 0
            response = offset_value_change(offset)
            if response.status_code == 500:
                return records
            response = json.loads(response.text)
  
    return records
