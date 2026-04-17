from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        from kerykeion import AstrologicalSubject

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

        return jsonify({
            "sun": str(subject.sun),
            "moon": str(subject.moon),
            "ascendant": str(subject.ascendant)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "detalle": str(e)
        })

app.run(host='0.0.0.0', port=10000)
