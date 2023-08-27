from google.transit import gtfs_realtime_pb2
from datetime import datetime
import requests
import csv
import main


def get_request(url):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url)
    feed.ParseFromString(response.content)
    
    return feed


def response_prase(vehicle, record_number, trips_update):
    
    vehicle_latitude = vehicle.vehicle.position.latitude
    vehicle_longitude = vehicle.vehicle.position.longitude
    vehicle_license_plate = vehicle.vehicle.vehicle.label
    vehicle_last_update = datetime.fromtimestamp(vehicle.vehicle.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    pathfile_trips = main.home + "/data/Poznan/trips.txt"
    pathfile_routes = main.home + "/data/Poznan/routes.txt"
    vehicle_delay_seconds = "None"

    for trip in trips_update.entity:
        if vehicle.vehicle.trip.trip_id == trip.trip_update.trip.trip_id:
            vehicle_delay_seconds = trip.trip_update.stop_time_update[0].arrival.delay
            break
        
    if vehicle_delay_seconds != "None":
        vehicle_delay = round(int(vehicle_delay_seconds)/60)
    else:
        vehicle_delay = "None"

    with open(pathfile_trips, newline="") as csvfile_trips:
        trpis_csv = csv.DictReader(csvfile_trips)
        for row in trpis_csv:
            if row['trip_id'] == vehicle.vehicle.trip.trip_id:
                vehicle_heading = row['trip_headsign']
                vehicle_route_id = row["\ufeffroute_id"]   
                with open(pathfile_routes, newline="") as csvfile_route:
                    routes_csv = csv.DictReader(csvfile_route)     
                    for row_routes in routes_csv:
                        if row_routes['\ufeffroute_id'] == vehicle_route_id:
                            vehicle_id = row_routes['route_short_name']
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
        record_number: {
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


def data_parser(line_number, limit):
    record_number = 0
    records = {}

    url_trips_update = "https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=trip_updates.pb"
    url_vehicle_positions = "https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=vehicle_positions.pb"    
    vehicle_positions = get_request(url_vehicle_positions)
    trips_update = get_request(url_trips_update)

    for vehicle in vehicle_positions.entity:
        record = response_prase(vehicle, record_number, trips_update)
        if line_number is None or record[record_number]['lineNumber'] == line_number:
            records.update(record)
            record_number = record_number + 1
            if limit is not None:
                if int(limit) == len(records):
                    return records 
    return records
