import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Pegá tu clave API aquí directamente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea con GPT ⚡"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    print(f"Mensaje de {sender}: {incoming_msg}")

    if incoming_msg:
        # Llamar a OpenAI
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
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Eres un asistente amigable y profesional de Curisol. Responde de manera clara, cercana y útil."},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            error_message = result["error"].get("message", "Error desconocido.")
            print("Error de OpenAI:", error_message)
            return f"OpenAI respondió con error: {error_message}"
        else:
            return "Respuesta inesperada del modelo."

    except Exception as e:
        print("Excepción general con OpenAI:", e)
        return "Ocurrió un error al procesar tu mensaje 🤖"

if __name__ == "__main__":
    app.run()
