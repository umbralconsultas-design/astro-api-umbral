from flask import Flask, request, jsonify
from kerykeion import AstrologicalSubject

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json

    subject = AstrologicalSubject(
        name=data.get("name"),
        year=int(data.get("year")),
        month=int(data.get("month")),
        day=int(data.get("day")),
        hour=int(data.get("hour")),
        minute=int(data.get("minute")),
        lat=19.4326,
        lng=-99.1332,
        tz_str="America/Mexico_City"
    )

    resultado = {
        "sun": subject.sun,
        "moon": subject.moon,
        "ascendant": subject.ascendant,
        "planets": subject.planets
    }

    return jsonify(resultado)

app.run(host='0.0.0.0', port=10000)
