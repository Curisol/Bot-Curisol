import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración (usa variables de entorno en producción)
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol123")  # ¡Debe coincidir con el token de Meta!
PORT = int(os.getenv("PORT", 5000))

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea V2.7.1: Humana, Rápida y Robusta ⚡"

@app.route("/webhook", methods=["GET", "POST"])  # ¡Acepta GET y POST!
def webhook():
    if request.method == "GET":
        # Verificación del webhook (Meta envía GET primero)
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if token == VERIFY_TOKEN:
            print("✅ Webhook verificado!")
            return challenge, 200
        else:
            print("❌ Token incorrecto. Esperado:", VERIFY_TOKEN, "Recibido:", token)
            return "Token inválido", 403

    elif request.method == "POST":
        # Procesamiento de mensajes entrantes
        data = request.get_json()
        print("📩 Mensaje recibido:", data)  # Para depuración
        
        # Respuesta básica (debes implementar tu lógica aquí)
        return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
