from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    return jsonify({"status": "ok", "mensaje": "funciona"})

app.run(host='0.0.0.0', port=10000)
