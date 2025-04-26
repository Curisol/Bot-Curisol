import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración - Usa variables de entorno en producción
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol123")  # ¡Debe coincidir con Meta!
PORT = int(os.getenv("PORT", 10000))  # Render usa 10000 por defecto

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea V2.7.1: Humana, Rápida y Robusta ⚡"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del webhook (Meta envía GET)
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if token == VERIFY_TOKEN:
            print("✅ Webhook verificado!")
            return challenge, 200
        print(f"❌ Token inválido. Esperado: {VERIFY_TOKEN}, Recibido: {token}")
        return "Token inválido", 403

    elif request.method == "POST":
        # Procesar mensajes entrantes de WhatsApp
        try:
            data = request.get_json()
            print("📩 Mensaje recibido:", data)  # Debug
            
            # Implementa tu lógica aquí:
            # Ejemplo básico:
            if data.get("object") == "whatsapp_business_account":
                return jsonify({"status": "success"}), 200
            
            return jsonify({"error": "Formato no válido"}), 400
            
        except Exception as e:
            print("⚠️ Error procesando POST:", str(e))
            return jsonify({"error": "Error interno"}), 500

if __name__ == "__main__":
    # ¡Importante! Render usa el puerto 10000 por defecto
    app.run(host="0.0.0.0", port=PORT)