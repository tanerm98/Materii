from sqlalchemy import create_engine
from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)

def connect_to_db():
    print("///////////////////////////////////////////////////////////")
    mysql_conn_str = "mysql+pymysql://root:1234@mysql_meteo_db:3306/meteo"
    engine = create_engine(mysql_conn_str)
    connection = engine.connect()

    connection.execute('use meteo')
    print("============================================================")

@app.route("/ruta1", methods=["GET"])
def hello():
    return "Hello, World!"

@app.route("/ruta2")
def salut():
    return "Salut, Lume!"

def main():
    connect_to_db()

if __name__ == "__main__":
    main()
    app.run('0.0.0.0', debug=True)