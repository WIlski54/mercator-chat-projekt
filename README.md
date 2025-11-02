# Mercator Chat Projekt

Ein interaktives Chat-Interface mit Gerhard Mercator, dem berühmten Kartografen aus dem 16. Jahrhundert.

## Projektstruktur

```
mercator-chat-projekt/
├── app.py                 # Flask Backend
├── requirements.txt       # Python Dependencies
├── templates/
│   └── interview.html     # Frontend HTML
└── .gitignore
```

## Lokale Installation

1. Repository klonen
2. Virtual Environment erstellen:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```
3. Dependencies installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. `.env` Datei erstellen mit:
   ```
   OPENAI_API_KEY=dein_api_key_hier
   ```
5. App starten:
   ```bash
   python app.py
   ```

## Deployment auf Render.com

### Schritt-für-Schritt Anleitung:

1. **GitHub Repository vorbereiten**
   - Pushe alle Dateien (app.py, requirements.txt, templates/) zu GitHub
   - Die `.env` Datei NICHT hochladen (steht in .gitignore)

2. **Render.com Service erstellen**
   - Gehe zu [render.com](https://render.com) und melde dich an
   - Klicke auf "New +" → "Web Service"
   - Verbinde dein GitHub Repository

3. **Service konfigurieren**
   - **Name**: `mercator-chat` (oder ein anderer Name)
   - **Region**: Frankfurt (für deutsche User)
   - **Branch**: `main`
   - **Root Directory**: Leer lassen (wir haben keine Unterordner mehr)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Environment Variables setzen**
   - Klicke auf "Environment" im Render Dashboard
   - Füge hinzu:
     - Key: `OPENAI_API_KEY`
     - Value: Dein OpenAI API Key
   - Klicke auf "Save Changes"

5. **Deploy**
   - Render wird automatisch deployen
   - Warte bis der Status "Live" ist
   - Deine App ist dann unter `https://dein-service-name.onrender.com` erreichbar

## Wichtige Änderungen gegenüber der lokalen Version

- **Port**: Die App nutzt jetzt `os.environ.get('PORT', 5000)` statt fest Port 5000
- **Host**: Die App bindet an `0.0.0.0` statt `127.0.0.1`
- **API URL**: Im Frontend wird ein relativer Pfad `/chat-mercator` verwendet statt `http://127.0.0.1:5000/chat-mercator`
- **Debug Mode**: Ist auf `False` gesetzt für Production

## Häufige Probleme

### 404 Error nach Deployment
- **Ursache**: Die Dateien liegen nicht im Root-Verzeichnis
- **Lösung**: Stelle sicher, dass `app.py`, `requirements.txt` und der `templates/` Ordner im Root des Repositories liegen

### 500 Internal Server Error
- **Ursache**: Fehlende Environment Variable oder API Key Problem
- **Lösung**: Überprüfe, ob `OPENAI_API_KEY` korrekt in Render gesetzt ist

### "Cannot find module" Error
- **Ursache**: Dependencies nicht installiert
- **Lösung**: Überprüfe ob `Build Command` richtig gesetzt ist: `pip install -r requirements.txt`

### Chat funktioniert nicht / keine Antwort
- **Ursache 1**: CORS-Problem
- **Lösung**: Sollte nicht auftreten, da Frontend und Backend auf derselben Domain laufen
- **Ursache 2**: OpenAI API Key ungültig
- **Lösung**: Überprüfe den API Key in den Environment Variables

## Support

Bei Fragen: Schau in die Render.com Logs unter "Logs" im Dashboard.
