import os
import time
import threading
import random
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

greetings = [
    "Hello!",
    "Hi there!",
    "Greetings!",
    "Salutations!",
    "Howdy!"
]

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params).json()
    return response

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

"""
Added by Aditya Yadav - 27226
This function uses and API to fetch weather from the weather API 
It basically provides us with a python dictionary that has keys like type, setup and punchline which contains specific string (or we can say the main content or weather)
This data will be called to show up the weather as I did in line 43 of code
"""
def weather():
    weather_url = "https://official-weather-api.appspot.com/weather/random"
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = response.json()
        return (f"{weather_data['setup']}\n{weather_data['punchline']}")
    return "Sorry, I couldn't fetch the weather at the moment."

def main():
    update_id = None
    print("Bot started...")
    while True:
        updates = get_updates(offset=update_id)
        for update in updates.get("result", []):
            update_id = update["update_id"] + 1
            message = update.get("message")
            chat_id = message.get("chat", {}).get("id", None)
            text = message.get("text", "").strip().lower()
            
            # Add your command in this block by using elif
            if text == "/start":
                greeting = random.choice(greetings)
                send_message(chat_id, greeting)
            elif text == "/weather":
                """
                This block checks if the command /weather is typed by the user while using the bot and which helps us to send the weather details(refer from line 66)
                """
                weather = weather()
                send_message(chat_id, weather)
            else:
                send_message(chat_id, "Invalid message")

        time.sleep(0.6)

if __name__ == "__main__":
    polling_thread = threading.Thread(target=main)
    polling_thread.start()