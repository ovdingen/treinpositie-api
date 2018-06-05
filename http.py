import sys
import json
from flask import Flask, jsonify
import sqlite3
import collections



configfile = 'conf/daemon.json'

config = json.load(open(configfile))

app = Flask(__name__)

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@app.route("/v1/trein/<trein_nr>")
def trein(trein_nr):
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    treinen = []
    
    rows = c.execute("SELECT * FROM posities WHERE trein_nummer = ?", [trein_nr])
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        treinen.append(row_dict)

    if len(treinen) is 0:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "trains": treinen}
    db.close()
    return jsonify(return_dict)

@app.route("/v1/mat/<mat_nr>")
def mat(mat_nr):
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    mat = {}
    
    rows = c.execute("SELECT * FROM posities WHERE mat_nummer = ? LIMIT 1", [mat_nr])
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        mat = row_dict

    if mat == {}:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "mat": mat}
    db.close()
    return jsonify(return_dict)

@app.route("/v1/total")
def total():
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    mat = []
    
    rows = c.execute("SELECT * FROM posities")
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        mat.append(row_dict)

    if mat == []:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "mat": mat}
    db.close()
    return jsonify(return_dict)

@app.route("/v1/total_geojson")
def total_geojson():
    db = sqlite3.connect(config['db'])
    db.row_factory = sqlite3.Row
    c = db.cursor()

    features = []
    
    rows = c.execute("SELECT * FROM posities")
    
    for row in rows:
        row_dict = dict_from_row(row)
        geometry = collections.OrderedDict()
        geometry['type'] = "Point"
        geometry['coordinates'] = [row_dict['lon'], row_dict['lat']]

        properties = collections.OrderedDict()
        properties['mat_nummer'] = row_dict['mat_nummer']
        properties['trein_nummer'] = row_dict['trein_nummer']
        properties['speed'] = row_dict['speed_kmh']
        properties['heading'] = row_dict['heading']

        feature = collections.OrderedDict()
        
        feature['type'] = "Feature"
        feature['geometry'] = geometry
        feature['properties'] = properties
        print(feature)
        
        features.append(feature)
    
    return_dict = collections.OrderedDict()
    return_dict['type'] = "FeatureCollection"
    return_dict['features'] = features
    
    db.close()
    return jsonify(return_dict)
