from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "UMBRAL OK"

@app.route("/carta", methods=["POST"])
def carta():
    data = request.json

    return jsonify({
        "mensaje": "Carta recibida",
        "datos": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
