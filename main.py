from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "API UMBRAL funcionando"

@app.route("/carta", methods=["POST"])
def carta():
    data = request.json

    url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.post(url, json=data)

    return jsonify({
        "status": "ok",
        "data_recibida": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
