from flask import Flask, jsonify,request, redirect
from swagger_ui import flask_api_doc
import json
import parser_Wroclaw
import parser_Warszawa
import parser_Gdansk
import parser_Karkow
import parser_Poznan


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
flask_api_doc(app, config_path='/home/meewosh/Pulpit/OpenData_parser_develop/OpenData_parser_dev/conf/swagger.yaml', url_prefix='/api/doc', title='API doc')

PYTHONIOENCODING="UTF-8"

@app.route("/")
def redirect_uri():
    if __name__=='__main__':
        return redirect("http://192.168.0.24:8000/api/doc", code = 302)
    return redirect("http://62.21.49.198:5000/api/doc", code = 302)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#DATA_STRUCT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/data", methods=["GET"])
def api_data():
    with open("data_struct.json", "r") as json_file:
        json_object = json.load(json_file)
    return jsonify(json_object)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#WARSZAWA
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/warszawa", methods=["GET"])
def api_warszawa():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    type = request.args.get('type')
    json = parser_Warszawa.dataParser(type, line_number, limit)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#WROCLAW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/wroclaw", methods=["GET"])
def api_wroclaw():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json = parser_Wroclaw.dataParser(limit, line_number)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#GDAŃSK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/gdansk", methods=["GET"])
def api_gdansk():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json = parser_Gdansk.dataParser(limit, line_number)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#KRAKÓW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/krakow", methods=["GET"])
def api_krakow():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    type_number = request.args.get('type')
    json = parser_Karkow.get_records(line_number, limit, type_number)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#POZNAŃ
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/poznan", methods=["GET"])
def api_poznan():
    limit = request.args.get('limit')
    line_number = request.args.get('lineNumber')
    json = parser_Poznan.get_records(line_number, limit)
    return jsonify(json)



if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    