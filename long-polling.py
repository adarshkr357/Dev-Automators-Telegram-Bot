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
		"disable_web_page_preview": disable_web_page_preview  # Disables the preview by default
	}
	
	if reply_to_message_id:
		data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message

	requests.post(url, data=data)

def send_photo(chat_id, photo, reply_to_message_id=None, caption=None, disable_web_page_preview=True):
	"""
	Added this in order to convert URL into an image
	"""
	url = BASE_URL + "sendPhoto"
	data = {
		"chat_id": chat_id,
		"photo": photo,
		"parse_mode": "HTML",
		"disable_web_page_preview": disable_web_page_preview # Disables the preview by default
	}
	
	if reply_to_message_id:
		data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message
		
	if caption:
		data["caption"] = caption
	
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
	username = username.lower()
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


def get_cat_image():
	"""
	Gets a photo of a cat from the Cat API
	"""
	cat_api_url = "https://api.thecatapi.com/v1/images/search"
	response = requests.get(cat_api_url)
	if response.status_code == 200:
		cat_data = response.json()
		return cat_data[0]["url"]
	return "Sorry, The cats are sleeping, try again later"


def get_devians_details(roll_no):
	"""
	Fetches student details from contributors.txt on GitHub using roll number.
	"""
	file_url = "https://raw.githubusercontent.com/adarshkr357/DevInnovators-FirstOpenSourceCommit/main/contributors.txt"
	
	response = requests.get(file_url)
	
	if response.status_code == 200:
		lines = response.text.split("\n")
		devians = []
		
		for line in lines:
			if f"Roll: {roll_no}" in line:
				devians.append(line)
				break
		
		if devians:
			devians_data = "\n".join(devians).replace(",","\n")\
											 .replace("Name:", "📝 Name:") \
											 .replace("Roll:", "🎓 Roll:") \
											 .replace("Branch:", "🏛 Branch:") \
											 .replace("Section:", "📚 Section:") \
											 .replace("Email:", "📩 Email:")

			return f"📌 <b>Devians Details:</b>\n{devians_data}"
		else:
			return "❌ Devians not found!"
	
	return "❌ Unable to fetch devians data. Try again later!"


def get_kkr_history():
    return (
        "🏏 <b>History of Kolkata Knight Riders (KKR)</b>\n\n"
        "📅 <b>Founded:</b> 2008\n"
        "🎭 <b>Owners:</b> Red Chillies Entertainment & Mehta Group\n"
        "🏟 <b>Home Ground:</b> Eden Gardens, Kolkata\n\n"
        "🏆 <b>IPL Titles:</b> 2012, 2014, 2024\n"
        "📜 <b>Legacy:</b> KKR is known for its passionate fanbase, unique playing style, and never-give-up attitude!\n\n"
        "🔗 <a href='https://www.kkr.in/'>Official Website</a>"
    )


def get_kkr_player_stats(player_name):
    player_name = player_name.lower().replace(" ", "-")
    url = f"https://api.cricapi.com/v1/players?name={player_name}&apikey=YOUR_API_KEY"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            player = data["data"][0]
            return (
                f"📊 <b>Player Stats for {player['name']}</b>\n\n"
                f"🏏 <b>Matches Played:</b> {player.get('matches', 'N/A')}\n"
                f"⚡ <b>Runs Scored:</b> {player.get('runs', 'N/A')}\n"
                f"🎯 <b>Wickets Taken:</b> {player.get('wickets', 'N/A')}\n"
                f"🔗 <a href='{player.get('profile', '#')}'>More Details</a>"
            )
        else:
            return "❌ Player not found in KKR database."
    return "❌ Unable to fetch player statistics. Try again later!"



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
			message_id = message.get("message_id")
			chat_id = message.get("chat", {}).get("id", None)
			text = message.get("text", "").strip().lower()
			
			# Add your command in this block by using elif
			if text == "/start":
				greeting = random.choice(greetings)
				send_message(chat_id, greeting, message_id)
			
			elif text.startswith("/devian "):
				"""
				Fetches student details from contributors.txt on GitHub using roll number.
				use = /devian <roll_no> - Get Devians details using roll number
				"""
				roll_no = text.split(" ", 1)[1]
				devians_info = get_devians_details(roll_no)
				send_message(chat_id, devians_info, message_id)

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

			elif text == "/cat":
				"""
				It will give a random cat image
				"""
				cat_image_url = get_cat_image()
				send_photo(chat_id, cat_image_url, message_id, caption="Here's a awe-some cat for you!")

			elif text == "/ipl":
				send_message(chat_id, get_kkr_history(), message_id)

			elif text.startswith("/iplstats "):
				player_name = text.split("/iplstats ", 1)[1].strip()
				send_message(chat_id, get_kkr_player_stats(player_name), message_id)

			else:
				send_message(chat_id, "Invalid message", message_id)

		time.sleep(0.5)

if __name__ == "__main__":
	polling_thread = threading.Thread(target=main)
	polling_thread.start()
