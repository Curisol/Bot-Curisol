from flask import Flask, request
import os

app = Flask(__name__)

# Token para validar el webhook con Meta
VERIFY_TOKEN = os.getenv('WEBHOOK_TOKEN', 'curisol2024')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        print("🟢 Verificando Webhook con Meta (GET)")
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        return 'Token inválido', 403

    if request.method == 'POST':
        data = request.get_json()
        print(f"📨 Mensaje recibido: {data}")
        return 'OK', 200

# Para ejecutar localmente
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
