# Abhay yadav 27006
# File converter bot
# This bot can convert images to PNG format and extract text from PDF files.
# It uses long polling to receive updates from Telegram and processes the received documents.   
# For more information, please refer to the README.md file.



import os
import time
import threading
import random
import requests
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader
import io

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# List of greeting messages
greetings = [
    "Hello!",
    "Hi there!",
    "Greetings!",
    "Salutations!",
    "Howdy!"
]

# Function to get updates from Telegram
def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params).json()
    return response

# Function to send a message to a chat
def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

# Function to send a document to a chat
def send_document(chat_id, document, filename):
    url = BASE_URL + "sendDocument"
    files = {"document": (filename, document)}
    data = {"chat_id": chat_id}
    requests.post(url, data=data, files=files)

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

# Main function to handle updates and process messages
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
            document = message.get("document")

            if text == "/start":
                # Send a random greeting message
                greeting = random.choice(greetings)
                send_message(chat_id, greeting)
            elif document:
                # Process the received document
                file_id = document["file_id"]
                file_info = requests.get(BASE_URL + f"getFile?file_id={file_id}").json()
                file_path = file_info["result"]["file_path"]
                file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                file_content = requests.get(file_url).content

                if document["mime_type"].startswith("image/"):
                    # Convert image to PNG format and send back
                    output = convert_image(io.BytesIO(file_content), "PNG")
                    send_document(chat_id, output, "converted_image.png")
                elif document["mime_type"] == "application/pdf":
                    # Extract text from PDF and send back
                    text = convert_pdf_to_text(io.BytesIO(file_content))
                    send_message(chat_id, text)
                else:
                    # Unsupported file type
                    send_message(chat_id, "Unsupported file type.")
            else:
                # No document received
                send_message(chat_id, "Please send a file to convert.")

        time.sleep(0.5)

if __name__ == "__main__":
    polling_thread = threading.Thread(target=main)
    polling_thread.start()