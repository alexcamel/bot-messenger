from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        messaging_event = data["entry"][0]["messaging"][0]
        sender_id = messaging_event["sender"]["id"]

        if "message" in messaging_event and "text" in messaging_event["message"]:
            send_message(
                sender_id,
                "Bonjour 👋 Je suis un bot automatique. Comment puis-je vous aider ?"
            )

    except Exception as e:
        print("Erreur:", e)

    return "ok", 200


def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    requests.post(url, params=params, json=payload)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
