import sqlalchemy as db
import pandas as pd
import json
from flask import Flask
from flask import request, jsonify, Response
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)

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
FROM = "from"
UNTIL = "until"

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
        valoare DOUBLE NOT NULL,
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
def add_country():
    global tari
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        nume = payload[NUME]
        lat = payload[LAT]
        lon = payload[LON]

        float(lat)
        float(lon)
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

@app.route("/api/countries", methods=["GET"])
def get_countries():
    global tari
    global connection

    query = db.select([tari])
    result = connection.execute(query).fetchall()

    response_data = []
    for (id, nume, latitudine, longitudine) in result:
        data = {
            ID: int(id),
            NUME: nume,
            LAT: float(latitudine),
            LON: float(longitudine)
        }
        response_data.append(data)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/countries/<int:id>", methods=["PUT"])
def update_country(id):
    global tari
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        idp = payload[ID]
        nume = payload[NUME]
        lat = payload[LAT]
        lon = payload[LON]

        int(id)
        float(lat)
        float(lon)
        assert id == idp
        if str(nume) == 0:
            raise
    except:
        return Response(status=400)

    try:
        query = db.select([tari]).where(tari.columns.id == id)
        results = connection.execute(query).fetchall()
        if results == []:
            raise

        query = db.update(tari).values(nume_tara=nume, latitudine=lat, longitudine=lon)
        query = query.where(tari.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_country(id):
    global tari
    global connection, engine

    try:
        query = db.select([tari]).where(tari.columns.id == id)
        results = connection.execute(query).fetchall()
        if results == []:
            raise

        query = db.delete(tari).where(tari.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/cities", methods=["POST"])
def add_city():
    global tari, orase
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        idtara = payload[IDTARA]
        nume = payload[NUME]
        lat = payload[LAT]
        lon = payload[LON]

        int(idtara)
        float(lat)
        float(lon)
        if str(nume) == 0:
            raise

        query = db.select([tari]).where(tari.columns.id == idtara)
        results = connection.execute(query).fetchall()
        if results == []:
            raise
    except:
        return Response(status=400)

    try:
        query = db.insert(orase).values(id_tara=idtara, nume_oras=nume, latitudine=lat, longitudine=lon)
        connection.execute(query)
    except:
        return Response(status=409)

    last_insert = connection.execute(db.select([orase])).fetchall()
    id_oras = int(last_insert[-1].id)

    response = app.response_class(
        response=json.dumps({"id": id_oras}),
        status=201,
        mimetype='application/json'
    )
    return response

@app.route("/api/cities", methods=["GET"])
def get_cities():
    global tari, orase
    global connection

    query = db.select([orase])
    result = connection.execute(query).fetchall()

    response_data = []
    for (id_oras, id_tara, nume_oras, latitudine, longitudine) in result:
        data = {
            ID: int(id_oras),
            IDTARA: int(id_tara),
            NUME: nume_oras,
            LAT: float(latitudine),
            LON: float(longitudine)
        }
        response_data.append(data)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/cities/country/<int:idTara>", methods=["GET"])
def get_cities_by_country(idTara):
    global orase
    global connection

    query = db.select([orase]).where(orase.columns.id_tara == idTara)
    result = connection.execute(query).fetchall()

    response_data = []
    for (id_oras, id_tara, nume_oras, latitudine, longitudine) in result:
        data = {
            ID: int(id_oras),
            NUME: nume_oras,
            LAT: float(latitudine),
            LON: float(longitudine)
        }
        response_data.append(data)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/cities/<int:id>", methods=["PUT"])
def update_city(id):
    global tari, orase
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        idp = payload[ID]
        idtara = payload[IDTARA]
        nume = payload[NUME]
        lat = payload[LAT]
        lon = payload[LON]

        int(idp)
        int(idtara)
        float(lat)
        float(lon)
        assert idp == id
        if str(nume) == 0:
            raise

        query = db.select([tari]).where(tari.columns.id == idtara)
        results = connection.execute(query).fetchall()
        if results == []:
            raise
    except:
        return Response(status=400)

    try:
        query = db.update(orase).values(id_tara=idtara, nume_oras=nume, latitudine=lat, longitudine=lon)
        query = query.where(orase.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_city(id):
    global orase
    global connection, engine

    try:
        query = db.select([orase]).where(orase.columns.id == id)
        results = connection.execute(query).fetchall()
        if results == []:
            raise

        query = db.delete(orase).where(orase.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures", methods=["POST"])
def add_temperature():
    global temperaturi, orase
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        idoras = payload[IDORAS]
        valoare = payload[VALOARE]

        int(idoras)
        float(valoare)

        query = db.select([orase]).where(orase.columns.id == idoras)
        results = connection.execute(query).fetchall()
        if results == []:
            raise
    except:
        return Response(status=400)

    try:
        query = db.insert(temperaturi).values(id_oras=idoras, valoare=valoare)
        connection.execute(query)
    except:
        return Response(status=409)

    last_insert = connection.execute(db.select([temperaturi])).fetchall()
    id_temp = int(last_insert[-1].id)

    response = app.response_class(
        response=json.dumps({"id": id_temp}),
        status=201,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures/<int:id>", methods=["PUT"])
def update_temperature(id):
    global temperaturi, orase
    global connection

    payload = request.get_json()
    if not payload:
        return Response(status=400)
    try:
        idtemp = payload[ID]
        idoras = payload[IDORAS]
        valoare = payload[VALOARE]

        int(idtemp)
        int(idoras)
        float(valoare)

        assert(id == idtemp)

        query = db.select([orase]).where(orase.columns.id == idoras)
        results = connection.execute(query).fetchall()
        if results == []:
            raise
    except:
        return Response(status=400)

    try:
        query = db.update(temperaturi).values(id_oras=idoras, valoare=valoare)
        query = query.where(temperaturi.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures/<int:id>", methods=["DELETE"])
def delete_temperature(id):
    global temperaturi
    global connection, engine

    try:
        query = db.select([temperaturi]).where(temperaturi.columns.id == id)
        results = connection.execute(query).fetchall()
        if results == []:
            raise

        query = db.delete(temperaturi).where(temperaturi.columns.id == id)
        connection.execute(query)
    except:
        return Response(status=404)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures", methods=["GET"])
def req1():
    global temperaturi, orase, tari
    global connection, engine

    lat = request.args.get(LAT)
    lon = request.args.get(LON)
    from_ = request.args.get(FROM)
    until = request.args.get(UNTIL)

    from_datetime_string = None
    until_datetime_string = None

    response_data = []

    try:
        if lat is not None:
            float(lat)
        if lon is not None:
            float(lon)

        if from_ is not None:
            from_datetime_string = datetime.strptime(from_, '%Y-%m-%d').strftime("%Y-%m-%d")
        if until is not None:
            until_datetime_string = datetime.strptime(until, '%Y-%m-%d').strftime("%Y-%m-%d")

        results = connection.execute(db.select([temperaturi])).fetchall()

        for element in results:
            (id_temp, id_oras, valoare, time_stamp) = element
            date_time_string = time_stamp.strftime("%Y-%m-%d")

            if from_datetime_string is not None:
                if from_datetime_string > date_time_string:
                    continue
            if until_datetime_string is not None:
                if until_datetime_string < date_time_string:
                    continue

            cities_lat = None
            if lat is not None:
                query = db.select([orase]).where(orase.columns.latitudine == lat)
                cities_lat = connection.execute(query).fetchall()
                if cities_lat == []:
                    continue

            if lon is not None:
                query = db.select([orase]).where(orase.columns.longitudine == lon)
                cities_lon = connection.execute(query).fetchall()
                if cities_lon == []:
                    continue
                if cities_lat is not None:
                    lat_lon_city = [value for value in cities_lat if value in cities_lon]
                    if lat_lon_city == []:
                        continue

            response_data.append({
                ID: int(id_temp),
                VALOARE: float(valoare),
                TIMESTAMP: date_time_string
            })

    except Exception as e:
        logging.info(e)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures/cities/<int:idOras>", methods=["GET"])
def req2(idOras):
    global temperaturi, orase, tari
    global connection, engine

    from_ = request.args.get(FROM)
    until = request.args.get(UNTIL)

    from_datetime_string = None
    until_datetime_string = None

    response_data = []

    try:
        int(idOras)

        if from_ is not None:
            from_datetime_string = datetime.strptime(from_, '%Y-%m-%d').strftime("%Y-%m-%d")
        if until is not None:
            until_datetime_string = datetime.strptime(until, '%Y-%m-%d').strftime("%Y-%m-%d")

        results = connection.execute(db.select([temperaturi])).fetchall()

        for element in results:
            (id_temp, id_oras, valoare, time_stamp) = element
            date_time_string = time_stamp.strftime("%Y-%m-%d")

            if int(id_oras) != idOras:
                continue
            if from_datetime_string is not None:
                if from_datetime_string > date_time_string:
                    continue
            if until_datetime_string is not None:
                if until_datetime_string < date_time_string:
                    continue

            response_data.append({
                ID: int(id_temp),
                VALOARE: float(valoare),
                TIMESTAMP: date_time_string
            })

    except Exception as e:
        logging.info(e)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/api/temperatures/countries//<int:idTara>", methods=["GET"])
def req3(idTara):
    global temperaturi, orase, tari
    global connection, engine

    from_ = request.args.get(FROM)
    until = request.args.get(UNTIL)

    from_datetime_string = None
    until_datetime_string = None

    response_data = []

    try:
        int(idTara)

        if from_ is not None:
            from_datetime_string = datetime.strptime(from_, '%Y-%m-%d').strftime("%Y-%m-%d")
        if until is not None:
            until_datetime_string = datetime.strptime(until, '%Y-%m-%d').strftime("%Y-%m-%d")

        results = connection.execute(db.select([temperaturi])).fetchall()

        for element in results:
            (id_temp, id_oras, valoare, time_stamp) = element
            date_time_string = time_stamp.strftime("%Y-%m-%d")

            if from_datetime_string is not None:
                if from_datetime_string > date_time_string:
                    continue
            if until_datetime_string is not None:
                if until_datetime_string < date_time_string:
                    continue

            query = db.select([orase]).where(orase.columns.id == id_oras)
            cities = connection.execute(query).fetchall()
            id_tara = cities[0][1]
            if id_tara != idTara:
                continue

            response_data.append({
                ID: int(id_temp),
                VALOARE: float(valoare),
                TIMESTAMP: date_time_string
            })

    except Exception as e:
        logging.info(e)

    response = app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

def main():
    connect_to_db()
    create_db()

if __name__ == "__main__":
    main()
    app.run(host=('0.0.0.0'), port=5001, debug=True)