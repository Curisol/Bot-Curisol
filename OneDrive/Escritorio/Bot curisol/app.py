import os
from flask import Flask, request

app = Flask(__name__)

# Configuración
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol123")  # ¡Mismo token que en Meta!

@app.route("/webhook", methods=["GET", "POST"])  # ¡Acepta GET y POST!
def webhook():
    if request.method == "GET":
        # Verificación del webhook
        token = request.args.get("hub.verify_token")
        if token == VERIFY_TOKEN:
            print("✅ Webhook verificado!")
            return request.args.get("hub.challenge"), 200
        print(f"❌ Token inválido. Esperado: {VERIFY_TOKEN}, Recibido: {token}")
        return "Token inválido", 403
    
    elif request.method == "POST":
        print("📩 Mensaje recibido:", request.json)
        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa puerto 10000
    app.run(host="0.0.0.0", port=port)
    