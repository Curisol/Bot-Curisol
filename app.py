import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Para cargar la API key si usás un archivo .env en el futuro

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"  # ← PEGÁ tu API key aquí si no usás .env

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea con GPT ⚡"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    print(f"Mensaje de {sender}: {incoming_msg}")

    if incoming_msg:
        # Llamada a OpenAI
        response = openai_response(incoming_msg)
    else:
        response = "No entendí tu mensaje 🤖"

    return f"""<Response>
        <Message>{response}</Message>
    </Response>""", 200, {'Content-Type': 'application/xml'}

def openai_response(user_input):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",  # Podés cambiar a "gpt-4" si tenés acceso
            "messages": [
                {"role": "system", "content": "Eres un asistente amigable y profesional de Curisol."},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("Error con OpenAI:", e)
        return "Lo siento, hubo un error procesando tu mensaje 🤖"

if __name__ == "__main__":
    app.run()
