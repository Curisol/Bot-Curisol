from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"Mensaje recibido de {sender}: {incoming_msg}")

    reply = "Hola, soy tu bot de prueba. Pronto estaré conectado con GPT 😎"

    return f"""<Response>
        <Message>{reply}</Message>
    </Response>""", 200, {'Content-Type': 'application/xml'}

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea ⚡"

if __name__ == "__main__":
    app.run()
