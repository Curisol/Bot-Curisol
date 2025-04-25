import os
from flask import Flask, request

app = Flask(__name__)

# Token de verificación para Meta
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol2024")

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea V2.7.1: Humana, Rápida y Robusta ⚡"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta verifica el token
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Token inválido", 403

    elif request.method == "POST":
        # Aquí llegan los mensajes reales
        data = request.get_json()
        print("Mensaje recibido:", data)
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
