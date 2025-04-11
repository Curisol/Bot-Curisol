import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Tu API Key, organización y proyecto reales
OPENAI_API_KEY = "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"
OPENAI_ORG_ID = "org-iTVIYG3D6kGi443rtfD7anuw"
OPENAI_PROJECT_ID = "proj_HnqW5nde4w6JZWKqouQdeJhO"

@app.route("/", methods=["GET"])
def home():
    return "Bot Curisol en línea con GPT (versión producción) ⚡"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    print(f"Mensaje de {sender}: {incoming_msg}")

    if incoming_msg:
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
            "OpenAI-Organization": OPENAI_ORG_ID,
            "OpenAI-Project": OPENAI_PROJECT_ID,
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Eres un asistente profesional, amigable y claro, parte del equipo de Curisol."},
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
