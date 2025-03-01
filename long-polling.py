# Built-in modules
import os
import time
import threading
import random
import io

# Third-party modules
import requests
from dotenv import load_dotenv
import pycountry
from PIL import Image
from PyPDF2 import PdfReader

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found. Please set it in .env file.")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Get from https://newsapi.org/register
if not NEWS_API_KEY:
    print("NEWS_API_KEY not found. Please set it in .env file.")

CRIC_KEY = os.getenv("CRIC_KEY")  # Get from https://cricketdata.org/signup.aspx
if not CRIC_KEY:
    print("CRIC_KEY not found. Please set it in .env file.")

"""
Follow these steps to get your API key:

1️⃣ Go to https://home.openweathermap.org/users/sign_up and sign up.
2️⃣ Log in to your account.
3️⃣ Navigate to the "API keys" section.
4️⃣ Click on "Generate a new key" and give it a name.
5️⃣ Copy the generated API key and use it.

🔹 Note: It may take a few hours for the API key to activate.
🔹 Free-tier API has rate limits, so use it wisely!
"""
OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
if not OPEN_WEATHER_KEY:
    print("OPEN_WEATHER_KEY not found. Please set it in .env file.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

greetings = ["Hello!", "Hi there!", "Greetings!", "Salutations!", "Howdy!"]

moods = [
    "😊 Happy: Because you're here, and that's all I need!",
    "😔 Sad: Feeling a little down... but your message just made it better!",
    "😠 Angry: Ugh! Someone tested my patience today. But you? You're my peace. 😌",
    "🤩 Excited: Ahh! You're here! U made my  day! 🎉",
]


def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params).json()
    return response


def get_news():
    params = {
        "apikey": NEWS_API_KEY,
        "country": "us",
        "category": "general",
        "pageSize": 5,
    }
    response = requests.get(NEWS_URL, params=params)
    news_data = response.json()
    articles = news_data.get("articles", [])
    news_list = [
        f"{article['title']} - {article['source']['name']}" for article in articles
    ]
    return "\n".join(news_list)


def send_message(
    chat_id, text, reply_to_message_id=None, disable_web_page_preview=True
):
    url = BASE_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_web_page_preview,  # Disables the preview by default
    }

    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message

    requests.post(url, data=data)


def send_photo(
    chat_id,
    photo,
    reply_to_message_id=None,
    caption=None,
    disable_web_page_preview=True,
):
    """
    Added this in order to convert URL into an image
    """
    url = BASE_URL + "sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_web_page_preview,  # Disables the preview by default
    }

    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message

    if caption:
        data["caption"] = caption

    requests.post(url, data=data)


def send_document(chat_id, document, filename, reply_to_message_id):
    url = BASE_URL + "sendDocument"
    files = {"document": (filename, document)}
    data = {"chat_id": chat_id, "parse_mode": "HTML"}

    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id  # Reply to user's message

    requests.post(url, data=data, files=files)


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


def get_dog_fact():
    """
    This function fetches a random dog fact from the Dog API.
    It returns the first fact from the API response.
    """
    dog_fact_url = "https://dog-api.kinduff.com/api/facts"
    response = requests.get(dog_fact_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("facts", ["No fact available"])[
            0
        ]  # Safely fetching the first fact
    return "Sorry, I couldn't fetch a dog fact at the moment."


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
            devians_data = (
                "\n".join(devians)
                .replace(",", "\n")
                .replace("Name:", "📝 Name:")
                .replace("Roll:", "🎓 Roll:")
                .replace("Branch:", "🏛 Branch:")
                .replace("Section:", "📚 Section:")
                .replace("Email:", "📩 Email:")
            )

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


def get_help_message():
    """
    Returns a help message listing all available commands and their usage.
    """
    return (
        "📌 <b>Available Commands:</b>\n\n"
        "🔹 <b>/start</b> - Start the bot and receive a greeting\n"
        "🔹 <b>/help</b> - Display this help message\n"
        "🔹 <b>/mood</b> - Get a random bot mood\n\n"
        "📰 <b>News & Information:</b>\n"
        "🔹 <b>/news</b> - Get the latest news headlines\n"
        "🔹 <b>/weather City, Country</b> - Get current weather updates\n\n"
        "😂 <b>Fun & Entertainment:</b>\n"
        "🔹 <b>/joke</b> - Get a random joke\n"
        "🔹 <b>/cat</b> - Get a random cat image\n\n"
        "🛠 <b>Utilities & API-Based:</b>\n"
        "🔹 <b>/github &lt;username&gt;</b> - Get GitHub user details (profile, repos, followers)\n"
        "🔹 <b>/github repo &lt;owner/repo&gt;</b> - Get GitHub repository details (stars, forks, last update)\n"
        "🔹 <b>/devian &lt;roll_no&gt;</b> - Get Devians details using roll number\n\n"
        "🏏 <b>Cricket & IPL:</b>\n"
        "🔹 <b>/ipl</b> - Get history and details about Kolkata Knight Riders (KKR)\n"
        "🔹 <b>/iplstats &lt;player_name&gt;</b> - Get KKR player's statistics\n\n"
        "📁 <b>File Processing:</b>\n"
        "🔹 <b>Upload an Image</b> - Convert between PNG and JPEG formats\n"
        "🔹 <b>Upload a PDF</b> - Extract text from the PDF file\n\n"
        "ℹ️ <i>Type a command or send a file to get started!</i>"
    )


# Function to convert an image to a different format
def convert_image(file_path, output_format):
    image = Image.open(file_path)
    output = io.BytesIO()
    image.save(output, format=output_format)
    output.seek(0)
    return output


# Function to extract text from a PDF file
def convert_pdf_to_text(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# To get country code by country name
def get_country_code(country_name):
    """
    Convert full country name to country code (e.g., 'India' -> 'IN').
    """
    country = pycountry.countries.get(name=country_name.title())
    return country.alpha_2 if country else None


# Fetch weather details when country code is provided
def get_weather(city, country):
    country_code = get_country_code(country)
    if not country_code:
        return "❌ Invalid country name! Please enter a valid country (e.g., 'India')."
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPEN_WEATHER_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"].capitalize()
        return f"🌤 Weather in {city.capitalize()}, {country.capitalize()}:\n🌡 Temperature: {temp}°C\n☁ Condition: {description}"

    return "Error: Unable to get weather update!"


# Function to get live cricket scores
def get_live_score():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRIC_KEY}&offset=0"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success" and "data" in data:
            matches = data["data"]
            live_matches = [
                m for m in matches if m.get("matchStarted") and not m.get("matchEnded")
            ]

            if live_matches:
                match = None
                for team in live_matches:
                    if team.get("teamInfo", False):
                        match = team
                        if match.get("score", False):
                            score = match.get("score")
                            break
                team1 = match["teamInfo"][0]["name"]
                team2 = match["teamInfo"][1]["name"]

                team1_score = score[0].get("r", "NA")
                team1_wickets = score[0].get("w", "NA")
                team1_overs = score[0].get("o", "NA")

                team2_score = score[1].get("r", "NA") if len(score) > 1 else "NA"
                team2_wickets = score[1].get("w", "NA") if len(score) > 1 else "NA"
                team2_overs = score[1].get("o", "NA") if len(score) > 1 else "NA"

                return (
                    f"🏏 <b>Live Match:</b> {team1} vs {team2}\n\n"
                    f"🔹 <b>{team1}:</b> {team1_score}/{team1_wickets} ({team1_overs} overs)\n"
                    f"🔹 <b>{team2}:</b> {team2_score}/{team2_wickets} ({team2_overs} overs)\n\n"
                    f"📢 <b>Status:</b> {match['status']}"
                )

            else:
                return "⚠ No live matches currently. Check back later!"
        else:
            return "❌ Error fetching live scores!"
    else:
        return "❌ Unable to connect to live score API!"


# This will give a random fun fact
def get_fun_fact():
    """
    Fetches a random fun fact.
    Returns the fact as a string.
    """
    fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(fact_url)

    if response.status_code == 200:
        data = response.json()
        return f"🤓 <b>Did You Know?</b>\n{data['text']}"
    return "❌ Unable to fetch a fun fact at the moment."


def get_movie_details(movie_name):
    """
    Fetches movie details from the OMDB API.
    """
    api_key = "your_omdb_api_key"  # Replace with your OMDB API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["Response"] == "True":
            movie_info = (
                f"🎬 <b>{data['Title']}</b> ({data['Year']})\n"
                f"📽 <b>Genre:</b> {data['Genre']}\n"
                f"🎭 <b>Actors:</b> {data['Actors']}\n"
                f"📊 <b>IMDB Rating:</b> {data['imdbRating']}\n"
                f"📝 <b>Plot:</b> {data['Plot']}"
            )
            return movie_info
        else:
            return "❌ Movie not found! Please check the name and try again."
    return "❌ Unable to fetch movie details at the moment."

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
            document = message.get("document")

            # Add your command in this block by using elif
            if text == "/start":
                greeting = random.choice(greetings)
                send_message(chat_id, greeting, message_id)
            elif text.startswith("/movie "):
                """
                Fetches movie details from OMDB API using the given movie name.
                Usage: /movie <movie_name>
                """
                movie_name = text.split("/movie ", 1)[1]
                movie_details = get_movie_details(movie_name)
                send_message(chat_id, movie_details, message_id)

            elif text == "/fact":
                fact = get_fun_fact()
                send_message(chat_id, fact, message_id)

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
                elif len(inpu) == 3 and inpu[1] == "repo":
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
                send_photo(
                    chat_id,
                    cat_image_url,
                    message_id,
                    caption="Here's a awe-some cat for you!",
                )

            elif text == "/ipl":
                send_message(chat_id, get_kkr_history(), message_id)

            elif text.startswith("/iplstats "):
                player_name = text.split("/iplstats ", 1)[1].strip()
                send_message(chat_id, get_kkr_player_stats(player_name), message_id)

            elif text == "/news":
                news = get_news()
                send_message(chat_id, news, message_id)

            elif text == "/dogfact":
                dog_fact = get_dog_fact()
                send_message(chat_id, dog_fact, message_id)

            elif text == "/help":
                """
                Sends a list of available commands when the user types /help
                """
                help_message = get_help_message()
                send_message(chat_id, help_message, message_id)

            elif document:
                file_id = document["file_id"]
                file_info = requests.get(BASE_URL + f"getFile?file_id={file_id}").json()
                file_path = file_info["result"]["file_path"]
                file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                file_content = requests.get(file_url).content

                if document["mime_type"].startswith("image/"):
                    output_format = (
                        "PNG" if document["mime_type"] == "image/jpeg" else "JPEG"
                    )
                    converted_image = convert_image(
                        io.BytesIO(file_content), output_format
                    )
                    send_document(
                        chat_id,
                        converted_image,
                        f"converted_image.{output_format.lower()}",
                        message_id,
                    )
                elif document["mime_type"] == "application/pdf":
                    text = convert_pdf_to_text(io.BytesIO(file_content))
                    send_message(chat_id, text, message_id)
                else:
                    send_message(chat_id, "Unsupported file type.", message_id)

            elif text == "/mood":
                mood = random.choice(moods)
                send_message(chat_id, mood, message_id)

            # Command handling for the bot
            elif text == "/livescore":
                send_message(chat_id, get_live_score(), message_id)

            elif text.startswith("/weather"):
                """
                Fetches weather details if the user provides a city and country.
                Ensures correct input format and prevents errors.
                """
                inpu = text.split("/weather", 1)[-1].strip()

                if not inpu:
                    send_message(
                        chat_id,
                        "❌ Please enter the city and country in this format:\n<code>/weather Delhi, India</code>",
                        message_id,
                    )

                else:
                    try:
                        city, country = map(str.strip, inpu.split(", ", 1))
                        weather = get_weather(city, country)
                        send_message(chat_id, weather, message_id)
                    except ValueError:
                        send_message(
                            chat_id,
                            "❌ Invalid format! Please enter as: <code>/weather City, Country</code>\nExample: <code>/weather Delhi, India</code>",
                            message_id,
                        )

            else:
                send_message(chat_id, "Invalid message", message_id)

        time.sleep(0.5)


if __name__ == "__main__":
    polling_thread = threading.Thread(target=main)
    polling_thread.start()
