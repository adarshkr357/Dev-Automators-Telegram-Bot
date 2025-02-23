import os
import random
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
NGROK_URL = "https://6578-2409-40d0-118d-43d9-e871-ae68-53f-a8d7.ngrok-free.app"  
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
WEBHOOK_URL = f"{NGROK_URL}/webhook"

greetings = [
    "Hello!",
    "Hi there!",
    "Greetings!",
    "Salutations!",
    "Howdy!"
]

app = Flask(__name__)

def set_webhook():
    url = BASE_URL + "setWebhook"
    data = {"url": WEBHOOK_URL}
    response = requests.post(url, data=data)
    print("Webhook set:", response.json())

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if update and "message" in update:
        message = update["message"]
        chat_id = message.get("chat", {}).get("id", None)

        # Add your command in this block by using elif
        if message.get("text", "").strip() == "/start":
            greeting = random.choice(greetings)
            send_message(chat_id, greeting)
        elif message.get("text", "").strip() == "/help":
            send_message(chat_id, "Here are the available commands:\n/start - Greet the user\n/help - Show available commands")
        else:
            send_message(chat_id, "Invalid message")

    return "OK", 200

@app.route("/", methods=["GET"])
def test():
    return "Flask server is up and running!", 200

if __name__ == "__main__":
    print("Setting webhook...")
    set_webhook()
    print("Starting Flask server on port 5000...")
    app.run(port=5000)
