from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔹 Traducción de signos
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

# 🔹 Traducción de casas
def traducir_casa(casa):
    casas = {
        "First_House": "1",
        "Second_House": "2",
        "Third_House": "3",
        "Fourth_House": "4",
        "Fifth_House": "5",
        "Sixth_House": "6",
        "Seventh_House": "7",
        "Eighth_House": "8",
        "Ninth_House": "9",
        "Tenth_House": "10",
        "Eleventh_House": "11",
        "Twelfth_House": "12"
    }
    return casas.get(casa, casa)

# 🔹 Traducción de nombres planetarios
def traducir_nombre(nombre):
    nombres = {
        "Sun": "Sol",
        "Moon": "Luna",
        "Ascendant": "Ascendente"
    }
    return nombres.get(nombre, nombre)

# 🔹 Formato final UMBRAL
def formatear(planeta):
    nombre = traducir_nombre(planeta.name)
    signo = traducir_signo(planeta.sign)
    casa = traducir_casa(planeta.house)

    return f"{nombre} en {signo} casa {casa}"

# 🔹 Endpoint principal
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

        resultado = {
            "sol": formatear(subject.sun),
            "luna": formatear(subject.moon),
            "ascendente": formatear(subject.ascendant)
        }

        return jsonify(resultado)

    except Exception as e:
        return jsonify({
            "status": "error",
            "detalle": str(e)
        }), 500

# 🔹 Run server
app.run(host='0.0.0.0', port=10000)
