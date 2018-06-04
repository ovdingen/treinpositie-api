import sys
import json
from flask import Flask, jsonify
import sqlite3


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

    mat = {}
    
    rows = c.execute("SELECT * FROM posities")
    status = "OK"
    for row in rows:
        row_dict = dict_from_row(row)
        mat = row_dict

    if mat == {}:
        status = "NOTFOUND"
    
    return_dict = {"status": status, "mat": mat}
    db.close()
    return jsonify(return_dict)
