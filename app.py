from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

# Charger les variables locales (.env) — ignoré sur Render, utile en local
load_dotenv()

app = Flask(__name__)

# Variables d’environnement
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# -----------------------------
# Webhook Verification (GET)
# -----------------------------
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # Debug (visible dans les logs Render)
    print("VERIFY TOKEN REÇU :", token)
    print("VERIFY TOKEN ATTENDU :", VERIFY_TOKEN)

    if token == VERIFY_TOKEN:
        return challenge, 200

    return "Invalid verification token", 403


# -----------------------------
# Réception des messages (POST)
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("DATA REÇUE :", data)

    try:
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                if "message" in event and "text" in event["message"]:
                    send_message(
                        sender_id,
                        "Bonjour 👋 Je suis un bot automatique.\nComment puis-je vous aider ?"
                    )

    except Exception as e:
        print("Erreur webhook :", e)

    return "ok", 200


# -----------------------------
# Envoi de message
# -----------------------------
def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, params=params, json=payload)
    print("Réponse Meta :", response.status_code, response.text)


# -----------------------------
# Lancement local uniquement
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
