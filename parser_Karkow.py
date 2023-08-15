from google.transit import gtfs_realtime_pb2
from datetime import datetime
import requests
import csv


def get_request(url):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    return feed


def response_prase(vehicle, record_number, type_number, trips_update):
    
    vehicle_latitude = vehicle.vehicle.position.latitude
    vehicle_longitude = vehicle.vehicle.position.longitude
    vehicle_license_plate = vehicle.vehicle.vehicle.license_plate
    
    vehicle_last_update = datetime.fromtimestamp(vehicle.vehicle.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    if type_number == '1':
        pathfile_trips = "/home/meewosh/Pulpit/OpenData_parser_develop/OpenData_parser_dev/data/Krakow/bus/trips.txt"
        pathfile_routes = "/home/meewosh/Pulpit/OpenData_parser_develop/OpenData_parser_dev/data/Krakow/bus/routes.txt"
    else:
        pathfile_trips = "/home/meewosh/Pulpit/OpenData_parser_develop/OpenData_parser_dev/data/Krakow/tram/trips.txt"
        pathfile_routes = "/home/meewosh/Pulpit/OpenData_parser_develop/OpenData_parser_dev/data/Krakow/tram/routes.txt"

    vehicle_delay = None
    for trip in trips_update.entity:
        if vehicle.vehicle.trip.trip_id == trip.trip_update.trip.trip_id:
            vehicle_delay = round(int(trip.trip_update.stop_time_update[0].arrival.delay)/60)
            break

    with open(pathfile_trips, newline="") as csvfile_trips:
        trpis_csv = csv.DictReader(csvfile_trips)
        for row in trpis_csv:
            if row["trip_id"] == vehicle.vehicle.trip.trip_id:
                vehicle_heading = row["trip_headsign"]
                vehicle_route_id = row["route_id"]
                with open(pathfile_routes, newline="") as csvfile_route:
                    routes_csv = csv.DictReader(csvfile_route)     
                    for row_routes in routes_csv:
                        if row_routes["route_id"] == vehicle_route_id:
                            vehicle_id = row_routes["route_short_name"]
                            break
                record = {
                    record_number:{
                        "lastUpdate": vehicle_last_update,
                        "lineNumber": vehicle_id,
                        "sideNumber": vehicle_license_plate,
                        "delay": vehicle_delay,
                        "route": vehicle_heading,
                        "latitude": vehicle_latitude,
                        "longitude": vehicle_longitude
                    }
                }
                return record
        
    record = {
        record_number:{
            "lastUpdate": "No data",
            "lineNumber": "No data",
            "sideNumber": "No data",
            "delay": "No data",
            "route": "No data",
            "latitude": "No data",
            "longitude": "No data"
        }
    }
    return record



def request_loop_data_prase(line_number, limit, type_number):
    record_number = 0
    records = {}
    if type_number == '1':
        url_vehicle_positions = "https://gtfs.ztp.krakow.pl/VehiclePositions_A.pb"
        url_trips_update = "https://gtfs.ztp.krakow.pl/TripUpdates_A.pb"
    else:
        url_vehicle_positions = "https://gtfs.ztp.krakow.pl/VehiclePositions_T.pb"
        url_trips_update = "https://gtfs.ztp.krakow.pl/TripUpdates_T.pb"

    vehicle_positions = get_request(url_vehicle_positions)
    trips_update = get_request(url_trips_update)

    for vehicle in vehicle_positions.entity:
        record = response_prase(vehicle, record_number, type_number, trips_update)
        if line_number == None or record[record_number]['lineNumber'] == line_number:
            records.update(record)
            record_number = record_number + 1
            if limit != None:
                if int(limit) == len(records):
                    return records 
    return records


def dataParser(line_number, limit, type_number):
    records = request_loop_data_prase(line_number, limit, type_number)
    return records