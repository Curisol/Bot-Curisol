import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tokens y configuración
VERIFY_TOKEN = os.getenv("WEBHOOK_TOKEN", "curisol2024")
PORT = int(os.getenv("PORT", 5000))

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea V2.7.1: Humana, Rápida y Robusta ⚡"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    try:
        if request.method == "GET":
            # Verificación del webhook
            mode = request.args.get("hub.mode")
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            
            if not all([mode, token, challenge]):
                logger.warning("Faltan parámetros en la verificación")
                return "Parámetros faltantes", 400
                
            if mode == "subscribe" and token == VERIFY_TOKEN:
                logger.info("Webhook verificado exitosamente")
                return challenge, 200
            else:
                logger.warning("Token de verificación inválido")
                return "Token inválido", 403

        elif request.method == "POST":
            # Procesamiento de mensajes
            data = request.get_json()
            if not data:
                logger.error("No se recibió JSON válido")
                return "Datos inválidos", 400
            
            logger.info(f"Datos recibidos: {data}")
            
            # Aquí deberías procesar el mensaje real
            # Ejemplo básico:
            if 'object' in data and 'entry' in data:
                for entry in data['entry']:
                    for change in entry.get('changes', []):
                        # Procesar cada cambio/mensaje
                        process_message(change['value'])
            
            return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"Error en webhook: {str(e)}")
        return jsonify({"error": "Error interno"}), 500

def process_message(message_data):
    """Función para procesar mensajes entrantes"""
    # TODO: Implementar lógica de negocio aquí
    logger.info(f"Procesando mensaje: {message_data}")
    # Ejemplo: responder a mensajes de texto
    # ...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=os.getenv("DEBUG", False))