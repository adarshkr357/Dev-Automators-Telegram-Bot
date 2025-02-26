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

def send_message(chat_id, text, reply_to_message_id=None, disable_web_page_preview=True):
    url = BASE_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_web_page_preview # Disables the preview by default
    }
    
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message

    requests.post(url, data=data)

def get_joke():
    """
    This function uses and API to fetch an joke from the joke API 
    It basically provides us with a python dictionary that has keys like type, setup and punchline which contains specific string (or we can say the main content or joke)
    This data will be called to show up the joke as I did in line 43 of code
    """
    joke_url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(joke_url)
    if response.status_code == 200:
        joke_data = response.json()
        return f"{joke_data['setup']}\n{joke_data['punchline']}"
    return "Sorry, I couldn't fetch a joke at the moment."

def get_github_profile(username):
    """
    Gets GitHub user details like profile link, public repos, 
    and followers.Converts username to lowercase to avoid errors.
    use = /github <username> - Get GitHub user details (profile, repos, followers) 
    """
    username= username.lower()
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return (
            f"🏷 <b>GitHub Profile:</b> {data['login']}\n"
            f"🔗 <a href=\"{data['html_url']}\">Profile Link</a>\n"
            f"🏆 <b>Public Repos:</b> {data['public_repos']}\n"
            f"👥 <b>Followers:</b> {data['followers']}"
        )
    else:
        return "❌ GitHub user not found."

def get_github_repo(repo_path):
    """
    Gets GitHub repo details like stars, forks, and last updated date.
    Converts repo path to lowercase to avoid errors.
    use = /github repo <owner/repo> - Get GitHub repository details (stars, forks, last update)  
    """
    repo_path = repo_path.lower()
    url = f"https://api.github.com/repos/{repo_path}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return (
            f"📌 <b>Repository:</b> {data['name']}\n"
            f"🔗 <a href=\"{data['html_url']}\">Repo Link</a>\n"
            f"⭐ <b>Stars:</b> {data['stargazers_count']}\n"
            f"🍴 <b>Forks:</b> {data['forks_count']}\n"
            f"📅 <b>Last Updated:</b> {data['updated_at'][:10]}"
        )
    else:
        return "❌ Repository not found."

# A list of sample quotes categorized by mood
quotes = {
    "inspiration": [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "It always seems impossible until it's done. – Nelson Mandela",
        "Believe you can and you're halfway there. – Theodore Roosevelt"
    ],
    "love": [
        "Love is composed of a single soul inhabiting two bodies. – Aristotle",
        "You know you're in love when you can't fall asleep because reality is finally better than your dreams. – Dr. Seuss",
        "Love all, trust a few, do wrong to none. – William Shakespeare"
    ],
    "life": [
        "In the end, we only regret the chances we didn’t take. – Lewis Carroll",
        "Life is what happens when you're busy making other plans. – John Lennon",
        "Live as if you were to die tomorrow. Learn as if you were to live forever. – Mahatma Gandhi"
    ],
    "funny": [
        "I am on a seafood diet. I see food and I eat it. – Anonymous",
        "Why don’t skeletons fight each other? They don’t have the guts. – Anonymous",
        "I told my wife she was drawing her eyebrows too high. She looked surprised. – Anonymous"
    ]
}    
# server fetching a random quote based on the mood
def suggest_quote(mood):
    print(f"Server is looking for a {mood} quote...")
    time.sleep(random.randint(1, 3))  # Simulate delay in fetching a quote

    # Fetch a random quote based on the mood category
    if mood in quotes:
        return random.choice(quotes[mood])
    else:
        return "Sorry, no quotes available for this mood. Try something else!"

    
def main():
    update_id = None
    print("Bot started...")
    while True:
        #get new updates from telegram bot
        updates = get_updates(offset=update_id)
        for update in updates.get("result", []):
            update_id = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue
            message_id = message.get("message_id")
            chat_id = message.get("chat", {}).get("id", None)
            text = message.get("text", "").strip().lower()
            
            # Add your command in this block by using elif
            if text == "/start":
                greeting = random.choice(greetings)
                send_message(chat_id, greeting, message_id)

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
                send_message(chat_id, response, message_id)

            elif text == "/joke":
                """
                This block checks if the command /joke is typed by the user while using the bot and helps us to send the joke (refer line 66)
                """
                joke = get_joke()
                send_message(chat_id, joke, message_id)
            elif text.startswith("/quote"):
                mood= text.replace("/quote" , "").strip()
                # get the mood
                if mood:
                    quote=suggest_quote(mood)
                    send_message(chat_id,quote,message_id)
            else:
                send_message(chat_id, "Invalid message", message_id)

        time.sleep(0.5)

if __name__ == "__main__":
    polling_thread = threading.Thread(target=main)
    polling_thread.start()
