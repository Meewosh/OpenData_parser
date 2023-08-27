from flask import Flask, jsonify, request, redirect
from swagger_ui import flask_api_doc
import json
import os
import parser_Wroclaw
import parser_Warszawa
import parser_Gdansk
import parser_Karkow
import parser_Poznan


home = os.environ["TEST"]
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
flask_api_doc(app, config_path=home + '/conf/swagger.yaml', url_prefix='/api/doc', title='API doc')

PYTHONIOENCODING = "UTF-8"

@app.route("/")
def api():
    data = "OPEN DATA PARSER"
    return data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# DATA_STRUCT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/data", methods=["GET"])
def api_data():
    with open("data_struct.json", "r") as json_file:
        json_format = json.load(json_file)
    return jsonify(json_format)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# WARSZAWA
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/warszawa", methods=["GET"])
def api_warszawa():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    type_number = request.args.get('type')
    json_format = parser_Warszawa.data_parser(type_number, line_number, limit)
    return jsonify(json_format)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# WROCLAW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/wroclaw", methods=["GET"])
def api_wroclaw():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json_format = parser_Wroclaw.data_parser(limit, line_number)
    return jsonify(json_format)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# GDAŃSK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/gdansk", methods=["GET"])
def api_gdansk():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json_format = parser_Gdansk.data_parser(limit, line_number)
    return jsonify(json_format)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# KRAKÓW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/krakow", methods=["GET"])
def api_krakow():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    type_number = request.args.get('type')

    json_format = parser_Karkow.data_parser(line_number, limit, type_number)
    return jsonify(json_format)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#POZNAŃ
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/poznan", methods=["GET"])
def api_poznan():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json_format = parser_Poznan.data_parser(line_number, limit)
    return jsonify(json_format)


@app.route("/findMyVehicle", methods=["GET"])
def api_find_my_vehicle():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    redirect_url = "https://www.google.com/maps/search/?api=1&query=" + latitude +"%2C" + longitude
    return redirect_url


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    

