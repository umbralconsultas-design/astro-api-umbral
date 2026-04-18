from flask import Flask, request, jsonify
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json

    date = Datetime(
        f"{data['year']}/{data['month']}/{data['day']}",
        f"{data['hour']}:{data['minute']}",
        str(data.get('timezone', -6))
    )

    pos = GeoPos(
        str(data.get('lat', 19.4326)),
        str(data.get('lon', -99.1332))
    )

    chart = Chart(date, pos)

    return jsonify({
        "sol": str(chart.get('SUN')),
        "luna": str(chart.get('MOON')),
        "ascendente": str(chart.get('ASC'))
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
