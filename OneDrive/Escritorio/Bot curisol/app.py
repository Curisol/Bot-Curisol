import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== CONFIGURACIÓN =====
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol123")  # Token para Meta
PORT = int(os.getenv("PORT", 10000))  # Render usa puerto 10000

# ===== RUTAS =====
@app.route("/", methods=["GET"])
def home():
    """Endpoint de estado"""
    return "Bot Curisol en línea: Seguro, Rápido y Robusto ⚡", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """Maneja verificación (GET) y mensajes (POST) de WhatsApp"""
    if request.method == "GET":
        # Verificación del webhook (Meta)
        token = request.args.get("hub.verify_token")
        if token == VERIFY_TOKEN:
            print("✅ Webhook verificado")
            return request.args.get("hub.challenge"), 200
        print(f"❌ Token inválido. Esperado: {VERIFY_TOKEN}, Recibido: {token}")
        return "Token inválido", 403

    elif request.method == "POST":
        try:
            data = request.get_json()
            print("📩 Mensaje recibido:", data)

            # ----- LÓGICA PARA MENSAJES WHATSAPP -----
            if data.get("object") == "whatsapp_business_account":
                # Ejemplo: responder mensajes de texto
                if "messages" in data["entry"][0]["changes"][0]["value"]:
                    message = data["entry"][0]["changes"][0]["value"]["messages"][0]
                    print(f"💬 Mensaje de {message['from']}: {message['text']['body']}")
                    # Aquí implementa tu respuesta automática
                    return jsonify({"status": "success"}), 200

            return jsonify({"error": "Formato no soportado"}), 400

        except Exception as e:
            print("⚠️ Error procesando mensaje:", str(e))
            return jsonify({"error": "Error interno"}), 500

# ===== INICIO =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)