import parser_Wroclaw
import parser_Warszawa
import parser_Gdansk
import json
from flask import Flask, jsonify,request, redirect
from swagger_ui import flask_api_doc
import socket

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
flask_api_doc(app, config_path='./conf/swagger.yaml', url_prefix='/api/doc', title='API doc')

PYTHONIOENCODING="UTF-8"

@app.route("/")
def hello_world():
    if __name__=='__main__':
        return redirect("http://192.168.0.11:8000/api/doc", code = 302)
    else:
        return redirect("http://62.21.49.198:5000/api/doc", code = 302)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#DATA_STRUCT
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/data", methods=["GET"])
def apiData():
    with open("data_struct.json", "r") as json_file:
        json_object = json.load(json_file)
    
    return jsonify(json_object)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#WARSZAWA
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/warszawa", methods=["GET"])
def apiWarsaw():
    limit = request.args.get('limit')
    lineNumber = request.args.get('lineNumber')
    type = request.args.get('type')
    json = parser_Warszawa.dataParser(type, lineNumber, limit)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#WROCLAW
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/wroclaw", methods=["GET"])
def apiWroclaw():
    limit = request.args.get('limit')
    lineNumber = request.args.get('lineNumber')
    json = parser_Wroclaw.dataParser(limit, lineNumber)
    return jsonify(json)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#GDAŃSK
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.route("/gdansk", methods=["GET"])
def apiGdansk():
    limit = request.args.get('limit')
    lineNumber = request.args.get('lineNumber')
    json = parser_Gdansk.dataParser(limit, lineNumber)
    return jsonify(json)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    