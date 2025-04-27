import os
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol123")
PORT         = int(os.getenv("PORT", 10000))

@app.route("/", methods=["GET"])
def home():
    return "Bot listo ✅", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode      = request.args.get("hub.mode")
        token     = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Token inválido", 403

    # Lógica para mensajes POST aquí
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
