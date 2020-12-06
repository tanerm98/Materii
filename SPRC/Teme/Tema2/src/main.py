import sqlalchemy as db
import pandas as pd
import json
from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

global engine, connection, metadata
global tari, orase, temperaturi

NUME = "nume"
LAT = "lat"
LON = "lon"
ID = "id"
IDTARA = "idTara"
IDORAS = "idOras"
VALOARE = "valoare"
TIMESTAMP = "timestamp"

NUME_TARA = "nume_tara"
LATITUDINE = "latitudine"
LONGITUDINE = "longitudine"
ID_TARA = "id_tara"
NUME_ORAS = "nume_oras"
ID_ORAS = "id_oras"
VALOARE = "valoare"
TIME_STAMP = "time_stamp"

def connect_to_db():
    global engine, connection, metadata

    print("Connecting to MySQL database...")
    mysql_conn_str = "mysql+pymysql://root:1234@mysql_meteo_db:3306/meteo"
    engine = db.create_engine(mysql_conn_str)
    connection = engine.connect()
    metadata = db.MetaData()
    print("Connection successful!")

def create_db():
    global engine, connection, metadata
    global tari, orase, temperaturi

    print("Creating database if it doesn't already exist!")

    database_creation_command = """
        CREATE TABLE IF NOT EXISTS tari(
            id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            nume_tara varchar(50) UNIQUE NOT NULL,
            latitudine DOUBLE,
            longitudine DOUBLE
        );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS orase(
        id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_tara INT(5) NOT NULL,
        nume_oras varchar(50) NOT NULL,
        latitudine DOUBLE,
        longitudine DOUBLE,
        
        FOREIGN KEY (id_tara) REFERENCES tari(id) ON DELETE CASCADE,
        UNIQUE KEY unique_index (id_tara, nume_oras)
    );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS temperaturi(
        id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_oras INT(5) NOT NULL,
        valoare INT(5) NOT NULL,
        time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (id_oras) REFERENCES orase(id) ON DELETE CASCADE,
        UNIQUE KEY unique_index (id_oras, time_stamp)
    );
    """
    connection.execute(database_creation_command)

    print("Database created successfully!")

    tari = db.Table('tari', metadata, autoload=True, autoload_with=engine)
    orase = db.Table('orase', metadata, autoload=True, autoload_with=engine)
    temperaturi = db.Table('temperaturi', metadata, autoload=True, autoload_with=engine)

@app.route("/api/countries", methods=["POST"])
def req1():
    global tari
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        nume = payload[NUME]
        lat = payload[LAT]
        lon = payload[LON]

        int(lat)
        int(lon)
        if str(nume) == 0:
            raise
    except:
        return Response(status=400)

    try:
        query = db.insert(tari).values(nume_tara=nume, latitudine=lat, longitudine=lon)
        connection.execute(query)
    except:
        return Response(status=409)

    last_insert = connection.execute(db.select([tari])).fetchall()
    id = int(last_insert[-1].id)

    response = app.response_class(
        response=json.dumps({"id": id}),
        status=201,
        mimetype='application/json'
    )
    return response

def main():
    connect_to_db()
    create_db()

    print(repr(metadata.tables['orase']))

if __name__ == "__main__":
    main()
    app.run(host=('0.0.0.0'), port=5001, debug=True)