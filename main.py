from flask import Flask, request, jsonify
import swisseph as swe
import math

app = Flask(__name__)

# 🔥 CONFIG EPHEMERIS (IMPORTANTE)
swe.set_ephe_path('/usr/share/ephe')  # en Render puede variar, pero funciona así normalmente


# ===============================
# 🌍 CALCULAR SIGNO
# ===============================
def obtener_signo(grados):
    signos = [
        "Aries", "Tauro", "Géminis", "Cáncer",
        "Leo", "Virgo", "Libra", "Escorpio",
        "Sagitario", "Capricornio", "Acuario", "Piscis"
    ]
    return signos[int(grados / 30)]


# ===============================
# 🔮 CALCULAR CARTA BÁSICA
# ===============================
def calcular_carta(data):
    year = int(data.get("year"))
    month = int(data.get("month"))
    day = int(data.get("day"))
    hour = int(data.get("hour"))
    minute = int(data.get("minute"))
    lat = float(data.get("lat"))
    lon = float(data.get("lon"))

    # 🔥 convertir hora decimal
    hora_decimal = hour + (minute / 60.0)

    # 🔥 fecha juliana
    jd = swe.julday(year, month, day, hora_decimal)

    # 🔥 planetas principales
    planetas = {
        "sol": swe.SUN,
        "luna": swe.MOON,
        "mercurio": swe.MERCURY,
        "venus": swe.VENUS,
        "marte": swe.MARS
    }

    resultado = {}

    for nombre, planeta in planetas.items():
        pos = swe.calc_ut(jd, planeta)[0][0]
        resultado[nombre] = {
            "grado": round(pos, 2),
            "signo": obtener_signo(pos)
        }

    # 🔥 ASCENDENTE
    casas = swe.houses(jd, lat, lon)
    asc = casas[0][0]

    resultado["ascendente"] = {
        "grado": round(asc, 2),
        "signo": obtener_signo(asc)
    }

    return resultado


# ===============================
# 🟢 HOME
# ===============================
@app.route("/")
def home():
    return "UMBRAL OK"


# ===============================
# 🔥 ENDPOINT REAL
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
