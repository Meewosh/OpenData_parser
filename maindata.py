import requests
# with urllib.request.urlopen("https://www.wroclaw.pl/open-data/api/action/datastore_search?resource_id=17308285-3977-42f7-81b7-fdd168c210a2&limit=5&q=title:jones") as url:
#     s = url.read()
#     # I'm guessing this would output the html source code ?
#     print(s)




def offset_change(offset):
    response = requests.get("https://www.wroclaw.pl/open-data/api/action/datastore_search?offset=%i&resource_id=17308285-3977-42f7-81b7-fdd168c210a2" % offset).json()
    
    return response


offset = 0

response = offset_change(offset)

total = response['result']['total']

iterator = 0
table = []

keys = ['Data_Aktualizacji', 'Nazwa_Linii', 'Nr_Boczny', 'Ostatnia_Pozycja_Szerokosc', 'Ostatnia_Pozycja_Dlugosc']

for x in range(total):
    
    for key in keys:
        table.append(response['result']['records'][iterator]['%s' % key])
        
    # Ostatnia_Pozycja_Szerokosc = response['result']['records'][iterator]['Ostatnia_Pozycja_Szerokosc']
    # Ostatnia_Pozycja_Dlugosc = response['result']['records'][iterator]['Ostatnia_Pozycja_Dlugosc']
    # Nazwa_Linii = response['result']['records'][iterator]['Nazwa_Linii']
    # Data_Aktualizacji = response['result']['records'][iterator]['Data_Aktualizacji']
    # Nr_Boczny = response['result']['records'][iterator]['Nr_Boczny']

    # table.append(Data_Aktualizacji)
    # table.append(Nazwa_Linii)
    # table.append(Nr_Boczny)
    # table.append(Ostatnia_Pozycja_Szerokosc)
    # table.append(Ostatnia_Pozycja_Dlugosc)

    print(table)
    table = []
    #print("--------------------------------")
    iterator = iterator + 1 
    
    if (iterator) == 100:
        iterator = 0
        offset = offset + 100
        response = offset_change(offset)
    
    #if offset == total:
    #    break
print("done")
print(offset)

