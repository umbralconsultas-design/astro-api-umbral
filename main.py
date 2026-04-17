from flask import Flask, request, jsonify

app = Flask(__name__)

def traducir_signo(sign):
    signos = {
        "Ari": "Aries",
        "Tau": "Tauro",
        "Gem": "Géminis",
        "Can": "Cáncer",
        "Leo": "Leo",
        "Vir": "Virgo",
        "Lib": "Libra",
        "Sco": "Escorpio",
        "Sag": "Sagitario",
        "Cap": "Capricornio",
        "Aqu": "Acuario",
        "Pis": "Piscis"
    }
    return signos.get(sign, sign)

def limpiar(data):
    sign = traducir_signo(data.sign)
    house = data.house.replace("_House", "").replace("First", "1").replace("Second", "2").replace("Third", "3").replace("Fourth", "4").replace("Fifth", "5").replace("Sixth", "6").replace("Seventh", "7").replace("Eighth", "8").replace("Ninth", "9").replace("Tenth", "10").replace("Eleventh", "11").replace("Twelfth", "12")
    return f"{data.name} en {sign} casa {house}"

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
            "sol": limpiar(subject.sun),
            "luna": limpiar(subject.moon),
            "ascendente": limpiar(subject.ascendant)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

app.run(host='0.0.0.0', port=10000)
