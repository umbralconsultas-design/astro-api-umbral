from flask import Flask, request, jsonify
import swisseph as swe
import os

app = Flask(__name__)

swe.set_ephe_path(os.getcwd())


# ===============================
# 🌍 SIGNOS
# ===============================
def obtener_signo(grados):
    signos = [
        "Aries", "Tauro", "Géminis", "Cáncer",
        "Leo", "Virgo", "Libra", "Escorpio",
        "Sagitario", "Capricornio", "Acuario", "Piscis"
    ]
    return signos[int(grados / 30)]


# ===============================
# 🔮 CARTA COMPLETA PRO
# ===============================
def calcular_carta(data):

    year = int(data.get("year"))
    month = int(data.get("month"))
    day = int(data.get("day"))

    hour = int(data.get("hour"))
    minute = int(data.get("minute"))

    lat = float(data.get("lat"))
    lon = float(data.get("lon"))

    timezone = float(data.get("timezone", -6))

    # 🔥 UTC CORRECTO
    hora_local = hour + (minute / 60.0)
    hora_utc = hora_local - timezone

    jd = swe.julday(year, month, day, hora_utc)

    # 🔥 PLANETAS
    planetas = {
        "sol": swe.SUN,
        "luna": swe.MOON,
        "mercurio": swe.MERCURY,
        "venus": swe.VENUS,
        "marte": swe.MARS,
        "jupiter": swe.JUPITER,
        "saturno": swe.SATURN
    }

    resultado = {}

    for nombre, planeta in planetas.items():
        pos = swe.calc_ut(jd, planeta)[0][0]
        resultado[nombre] = {
            "grado": round(pos, 2),
            "signo": obtener_signo(pos)
        }

    # 🔥 CASAS PLACIDUS
    casas, ascmc = swe.houses_ex(jd, lat, lon, b'P')

    asc = ascmc[0]
    mc = ascmc[1]

    resultado["ascendente"] = {
        "grado": round(asc, 2),
        "signo": obtener_signo(asc)
    }

    resultado["medio_cielo"] = {
        "grado": round(mc, 2),
        "signo": obtener_signo(mc)
    }

    # 🔥 CASAS COMPLETAS
    casas_lista = []
    for i, casa in enumerate(casas):
        casas_lista.append({
            "casa": i + 1,
            "grado": round(casa, 2),
            "signo": obtener_signo(casa)
        })

    resultado["casas"] = casas_lista

    return resultado


# ===============================
# 🟢 HOME
# ===============================
@app.route("/")
def home():
    return "UMBRAL OK"


# ===============================
# 🔥 ENDPOINT
# ===============================
@app.route("/carta", methods=["POST"])
def carta():
    try:
        data = request.json

        carta = calcular_carta(data)

        return jsonify({
            "mensaje": "Carta calculada",
            "carta": carta
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ===============================
# 🚀 RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
