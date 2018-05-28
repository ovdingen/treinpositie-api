import argparse
import zmq
import json
import zlib
import sqlite3
import xmltodict
from collections import OrderedDict

parser = argparse.ArgumentParser(description="Ontvangt NS treinpositiedata")
parser.add_argument('config')

args = parser.parse_args()

config = json.load(open(args.config))

db_conn = sqlite3.connect(config['db'])
query = "REPLACE INTO posities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"

zmq_context = zmq.Context()
zmq_sock = zmq_context.socket(zmq.SUB)
zmq_sock.connect(config['addr'])
zmq_sock.setsockopt(zmq.SUBSCRIBE, '/RIG/NStreinpositiesInterface5')

while True:
    c = db_conn.cursor()
    topic = zmq_sock.recv()

    message_gzip = zmq_sock.recv()
    message = xmltodict.parse(zlib.decompress(message_gzip, 16+zlib.MAX_WBITS))
    # Decompress gzip data, and convert resulting XML to a dict

    rows = []

    for trein in message['tns:ArrayOfTreinLocation']['tns:TreinLocation']:
        
        treinNr = trein['tns:TreinNummer']
        if type(trein['tns:TreinMaterieelDelen']) is OrderedDict:
            mat = trein['tns:TreinMaterieelDelen']
            row = (mat['tns:MaterieelDeelNummer'], treinNr, mat['tns:Materieelvolgnummer'], mat['tns:Snelheid'], mat['tns:Richting'], mat['tns:Latitude'], mat['tns:Longitude'], mat['tns:Fix'], mat['tns:GpsDatumTijd'])
            print(row)
            rows.append(row)
        else:
            for mat in trein['tns:TreinMaterieelDelen']:
                row = (mat['tns:MaterieelDeelNummer'], treinNr, mat['tns:Materieelvolgnummer'], mat['tns:Snelheid'], mat['tns:Richting'], mat['tns:Latitude'], mat['tns:Longitude'], mat['tns:Fix'], mat['tns:GpsDatumTijd'])
                rows.append(row)
    c.executemany(query, rows)
    db_conn.commit()
    
    

    