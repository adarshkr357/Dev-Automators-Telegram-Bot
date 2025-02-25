import os
import time
import threading
import random
import requests
import pycountry #helps by converting full country names into their official country codes. as required by open Weather Api
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
moods=[ "😊 Happy: Because you’re here, and that’s all I need!",
        "😔 Sad: Feeling a little down... but your message just made it better!",
        "😠 Angry: Ugh! Someone tested my patience today. But you? You're my peace. 😌",
        "🤩 Excited: Ahh! You’re here! U made my  day! 🎉"
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
Added by AkshitBhandari - 27016
This function uses and API to fetch an joke from the joke API 
It basically provides us with a python dictionary that has keys like type, setup and punchline which contains specific string (or we can say the main content or joke)
This data will be called to show up the joke as I did in line 43 of code
"""
def get_joke():
    joke_url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(joke_url)
    if response.status_code == 200:
        joke_data = response.json()
        return f"{joke_data['setup']}\n{joke_data['punchline']}"
    return "Sorry, I couldn't fetch a joke at the moment."

def get_github_profile(username):
    """Gets GitHub user details like profile link, public repos, 
    and followers.Converts username to lowercase to avoid errors.
    use = /github <username> - Get GitHub user details (profile, repos, followers) 
    """
    username= username.lower()
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return (
            f"🏷 *GitHub Profile:* {data['login']}\n"
            f"🔗 [Profile Link]({data['html_url']})\n"
            f"🏆 *Public Repos:* {data['public_repos']}\n"
            f"👥 *Followers:* {data['followers']}"
        )
    else:
        return "❌ GitHub user not found."

def get_github_repo(repo_path):
    """Gets GitHub repo details like stars, forks, and last updated date.
    Converts repo path to lowercase to avoid errors.
    use = /github repo <owner/repo> - Get GitHub repository details (stars, forks, last update)  
     """
    repo_path = repo_path.lower()
    url = f"https://api.github.com/repos/{repo_path}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return (
            f"📌 *Repository:* {data['name']}\n"
            f"🔗 [Repo Link]({data['html_url']})\n"
            f"⭐ *Stars:* {data['stargazers_count']}\n"
            f"🍴 *Forks:* {data['forks_count']}\n"
            f"📅 *Last Updated:* {data['updated_at'][:10]}"
        )
    else:
        return "❌ Repository not found."
# Added by Disha --> 27057 
# This will return weather details of user-entered city and country like Temperature and Condition of weather

user_states = {}  # Dictionary to store users waiting for city input

def get_country_code(country_name):
    """Convert full country name to country code (e.g., 'India' -> 'IN')."""
    country = pycountry.countries.get(name=country_name.title())  # Capitalization of country code 
    return country.alpha_2 if country else None  # Return country code if found, else None

def get_weather(city, country):
    """Fetch weather details using OpenWeather API."""
    api_key = os.getenv("Open_Weather_Api")
    country_code = get_country_code(country)
    if not country_code:
        return "❌ Invalid country name! Please enter a valid country (e.g., 'India')."
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        desc = weather_data["weather"][0]["description"].capitalize()
        return f"🌤 Weather in {city}, {country_code}:\n🌡 Temperature: {temp}°C\n☁ Condition: {desc}"
    return "Error: Unable to get weather update!"

def main():
    update_id = None
    print("Bot started...")
    while True:
        updates = get_updates(offset=update_id)
        for update in updates.get("result", []):
            update_id = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue
            chat_id = message.get("chat", {}).get("id", None)
            text = message.get("text", "").strip().lower()
            
            # Add your command in this block by using elif
            if text == "/start":
                greeting = random.choice(greetings)
                send_message(chat_id, greeting)
            elif text.startswith("/github"):
                """
                Gets GitHub user details like profile link, public repos, and followers.
                Converts username to lowercase to avoid errors.
                """
                inpu = text.split()
                if len(inpu) == 2:
                    username = inpu[1]
                    response = get_github_profile(username)
                elif len(inpu) == 3 and inpu[1] == "repo" :
                    repo_path = inpu[2]
                    response = get_github_repo(repo_path)
                else:
                    response = "ℹ️ Usage: `/github <username>` or `/github repo <username>/<repo>`"
                send_message(chat_id, response)

            elif text == "/joke":
                """
                This block checks if the command /joke is typed by the user while using the bot and helps us to send the joke (refer line 66)
                """
                joke = get_joke()
                send_message(chat_id, joke)
                """
                Added by Disha - 27057
                1)This will show up moods by random, sometimes happy, sad, angry and exicited in pickup lines sense.
                2)This will retrieves real-time weather data for a given city and country, typically using an API like 
                OpenWeatherMap, and returns the formatted weather details.
                """           
            elif  text == "/mood":
                mood = random.choice(moods)
                send_message(chat_id, mood)
            elif text == "/weather":
                """Handle weather command: prompt user for city and country."""
                user_states[chat_id] = "awaiting_location"
                send_message(chat_id, "🌍 Please enter the city and country (e.g., Delhi, India):")
            elif chat_id in user_states and user_states[chat_id] == "awaiting_location":
                """Process user input after weather command."""
                try:
                    city, country = map(str.strip, text.split(","))
                    weather = get_weather(city, country)
                    send_message(chat_id, weather)
                except ValueError:
                    send_message(chat_id, "❌ Invalid format! Please enter as: City, Country (e.g., Delhi, India)")
                del user_states[chat_id]  # Remove user from awaiting state
            else:
                send_message(chat_id, "Invalid command. Use /help for assistance.")
            
        time.sleep(0.5)

if __name__ == "__main__":
    polling_thread = threading.Thread(target=main)
    polling_thread.start()
