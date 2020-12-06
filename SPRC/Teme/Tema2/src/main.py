import sqlalchemy as db
from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

global engine, connection, metadata
global tari, orase, temperaturi

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
            nume_tara varchar(50) UNIQUE,
            latitudine DOUBLE(20,20),
            longitudine DOUBLE(20,20)
        );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS orase(
        id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_tara INT(5),
        nume_oras varchar(50),
        latitudine DOUBLE(20,20),
        longitudine DOUBLE(20,20),
        
        FOREIGN KEY (id_tara) REFERENCES tari(id),
        UNIQUE KEY unique_index (id_tara, nume_oras)
    );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS temperaturi(
        id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_oras INT(5),
        valoare INT(5),
        time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (id_oras) REFERENCES orase(id),
        UNIQUE KEY unique_index (id_oras, time_stamp)
    );
    """
    connection.execute(database_creation_command)

    print("Database created successfully!")

    tari = db.Table('tari', metadata, autoload=True, autoload_with=engine)
    orase = db.Table('orase', metadata, autoload=True, autoload_with=engine)
    temperaturi = db.Table('temperaturi', metadata, autoload=True, autoload_with=engine)

def main():
    connect_to_db()
    create_db()

if __name__ == "__main__":
    main()
    app.run(host=('0.0.0.0'), port=5001, debug=True)