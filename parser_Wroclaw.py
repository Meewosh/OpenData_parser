import requests


def response_get(offset):
    response = requests.get("https://www.wroclaw.pl/open-data/api/action/datastore_search?offset=%i&resource_id=17308285-3977-42f7-81b7-fdd168c210a2" % offset).json()
    return response


def response_parse(response, iterator, keys, recordNumber):
    record = {
        recordNumber:{
            "lastUpdate": response['result']['records'][iterator]['%s' % keys[0]],
            "lineNumber": response['result']['records'][iterator]['%s' % keys[1]],
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


def ifChangeNumberOfRecord(record, records, recordNumber, iterator_tmp, lineNumber):
    if lineNumber == None:
        records.update(record)
    else:
        record_tmp = {}
        record_tmp[iterator_tmp] = record[recordNumber]
        records.update(record_tmp)


def dataParser(limit, lineNumber):
    keys = ['Data_Aktualizacji', 'Nazwa_Linii', 'Nr_Boczny', 'Ostatnia_Pozycja_Szerokosc', 'Ostatnia_Pozycja_Dlugosc']
    records = {}
    iterator = 0
    iterator_tmp = 0
    offset = 0
    response = response_get(offset)
    totalAmountOfRecordBeforePrase = response['result']['total']

    for recordNumber in range(totalAmountOfRecordBeforePrase):
        record = response_parse(response, iterator, keys, recordNumber)
        
        if lineNumber == None or record[recordNumber]['lineNumber'] == lineNumber:
            ifChangeNumberOfRecord(record, records, recordNumber, iterator_tmp, lineNumber)
            iterator_tmp = iterator_tmp + 1
            
        iterator = iterator + 1

        if limit != None:
            if int(limit) == len(records):
                return records 

        if (iterator) == 100:  
            iterator = 0
            response = offset_value_change(offset)
  
    return records