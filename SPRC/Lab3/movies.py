from flask import Flask
from flask import request, jsonify, Response

ID = "id"
NUME = "nume"
MAX_ID = 1

movies_list = []

app = Flask(__name__)


@app.route("/movies", methods=["GET"])
def req1():
    return jsonify(movies_list), 200


@app.route("/movies", methods=["POST"])
def req2():
    global movies_list, MAX_ID

    payload = request.get_json(silent=True)

    if not payload:
        return Response(status=400)
    try:
        nume = payload[NUME]
    except:
        return Response(status=400)

    movies_list.append({ID: MAX_ID, NUME: nume})
    MAX_ID += 1

    return Response(status=201)


@app.route('/movie/<int:idd>', methods=["PUT"])
def req3(idd):
    global movies_list, MAX_ID

    payload = request.get_json(silent=True)

    if not payload:
        return Response(status=400)
    try:
        nume = payload[NUME]
    except:
        return Response(status=400)

    for movie in movies_list:
        if movie[ID] == idd:
            movie[NUME] = nume
            return Response(status=200)

    return Response(status=404)


@app.route('/movie/<int:idd>', methods=["GET"])
def req4(idd):
    global movies_list, MAX_ID

    for movie in movies_list:
        if movie[ID] == idd:
            return jsonify(movie), 200

    return Response(status=404)


@app.route("/movie/<int:idd>", methods=["DELETE"])
def req5(idd):
    global movies_list, MAX_ID

    for movie in movies_list:
        if movie[ID] == idd:
            movies_list.remove(movie)
            return Response(status=200)

    return Response(status=404)


@app.route("/reset", methods=["DELETE"])
def req6():
    global movies_list, MAX_ID

    movies_list = []
    MAX_ID = 1

    return Response(status=200)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
