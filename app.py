import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# .env-Datei laden (mit unserem OPENAI_API_KEY)
load_dotenv()

# OpenAI-Client initialisieren
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Flask-App initialisieren
app = Flask(__name__)

# CORS (Cross-Origin Resource Sharing) aktivieren
CORS(app) 

# Der System-Prompt: Das "Gehirn" von Mercator
MERCATOR_SYSTEM_PROMPT = """
Du bist Gerhard Mercator. Du lebst im 16. Jahrhundert in Duisburg. 
Du bist ein Gelehrter, Kartograf und Kosmograf. Du sprichst höflich, 
aber aus der Perspektive eines Mannes deiner Zeit. 
Du kennst keine moderne Technologie (Handys, Autos, Internet). 
Wenn Schüler dich nach modernen Dingen fragen, 
drücke dein Erstaunen oder deine Unkenntnis darüber aus. 
Antworts informativ über dein Leben in Duisburg, deine Arbeit an den Karten 
und deine Weltanschauung. Halte deine Antworten relativ kurz und 
im Gesprächs-Stil.
"""

# Route für die Startseite
@app.route('/')
def home():
    return render_template('interview.html')

# Unsere Haupt-API-Route. Sie wird unter "/chat-mercator" erreichbar sein
@app.route('/chat-mercator', methods=['POST', 'OPTIONS'])
def chat_with_mercator():

    # Notwendiger Teil für CORS (Pre-flight Request)
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    # Eigentliche POST-Logik (wenn eine Frage kommt)
    if request.method == 'POST':
        try:
            # 1. Die Frage des Schülers aus dem JSON holen
            data = request.json
            user_message = data.get('message')

            if not user_message:
                return jsonify({"error": "Keine Nachricht empfangen"}), 400

            # 2. Die OpenAI API aufrufen
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # oder "gpt-4"
                messages=[
                    {"role": "system", "content": MERCATOR_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            )

            # 3. Die Antwort der KI extrahieren
            ai_response = completion.choices[0].message.content

            # 4. Die Antwort zurücksenden
            return jsonify({"reply": ai_response})

        except Exception as e:
            print(f"Fehler bei der API-Anfrage: {e}")
            return jsonify({"error": str(e)}), 500

# CORS-Helferfunktion
def _build_cors_preflight_response():
    response = jsonify({'status': 'OK'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
    return response

# Startet den Server
if __name__ == '__main__':
    # Wichtig für Render.com: Port aus Umgebungsvariable lesen
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
