from flask import Flask, request
import os

app = Flask(__name__)

# Token para validar webhook con Meta
VERIFY_TOKEN = os.getenv('WEBHOOK_TOKEN', 'curisol2024')

# Ruta principal para recibir y validar mensajes desde Meta
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("🔥 ENTRANDO A /webhook CON MÉTODO:", request.method)

    if request.method == 'GET':
        # Meta valida el webhook con estos parámetros
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        # Recibir y mostrar los datos del mensaje recibido
        data = request.get_json()
        print(f"📩 Mensaje recibido: {data}")
        return 'OK', 200

# Solo para correr localmente o si PORT está definido
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usa 10000 si no hay otra asignación
    app.run(host='0.0.0.0', port=port)
