from sqlalchemy import create_engine
from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

def connect_to_db():
    print("Connecting to MySQL database...")
    mysql_conn_str = "mysql+pymysql://root:1234@mysql_meteo_db:3306"
    engine = create_engine(mysql_conn_str)
    connection = engine.connect()
    print("Connection successful!")

    return connection

def create_db(connection):
    print("Creating database if it doesn't already exist!")

    connection.execute("CREATE DATABASE IF NOT EXISTS meteo;")
    connection.execute("USE meteo;")

    database_creation_command = """
        CREATE TABLE IF NOT EXISTS tari(
            id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            nume_tara varchar(50) UNIQUE,
            latitudine varchar(50),
            longitudine varchar(50)
        );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS orase(
        id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_tara int(5),
        nume_oras varchar(50),
        latitudine varchar(50),
        longitudine varchar(50),
        
        FOREIGN KEY (id_tara) REFERENCES tari(id),
        UNIQUE KEY unique_index (id_tara, nume_oras)
    );
    """
    connection.execute(database_creation_command)

    database_creation_command = """
    CREATE TABLE IF NOT EXISTS temperaturi(
        id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_oras int(5),
        valoare int(5),
        time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (id_oras) REFERENCES orase(id),
        UNIQUE KEY unique_index (id_oras, time_stamp)
    );"""
    connection.execute(database_creation_command)

    print("Database created successfully!")

def main():
    connection = connect_to_db()
    create_db(connection)

if __name__ == "__main__":
    main()
    app.run(host=('0.0.0.0'), port=5001, debug=True)