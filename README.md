# **File Converter Bot**

Welcome to **File Converter Bot** – a versatile Telegram bot project!

This bot is designed to convert files to different formats and extract text from PDFs. It serves as a foundation for adding new, useful commands. We encourage open-source contributions to expand its capabilities while ensuring that all content remains legal, professional, and free from slang or inappropriate language.

## **Introduction**

**Name:** Abhay Yadav  
**ID:** 27006  

**Project:** File Converter Bot

**Description:**
This project is a Telegram bot that allows users to convert files to different formats. The bot can handle images, PDFs, and text files. Users can interact with the bot by sending commands and files, and the bot will respond with the converted files or extracted text.

**Features:**
- **Greeting Messages:** The bot sends a random greeting message when the `/start` command is received.
- **Image Conversion:** The bot can convert images to PNG format.
- **PDF Text Extraction:** The bot can extract text from PDF files and send it back to the user.
- **Unsupported File Types:** The bot informs the user if the file type is unsupported.

**How It Works:**
1. **Environment Setup:** The bot token is loaded from a `.env` file.
2. **Polling for Updates:** The bot continuously polls the Telegram API for updates.
3. **Processing Messages:** The bot processes incoming messages and documents.
4. **File Conversion:** Depending on the file type, the bot converts the file or extracts text and sends it back to the user.

**Example Interaction:**
- **Send `/start` Command:** The bot responds with a random greeting message.
- **Send an Image File:** The bot converts the image to PNG format and sends it back.
- **Send a PDF File:** The bot extracts text from the PDF and sends it back.
- **Send an Unsupported File Type:** The bot informs the user that the file type is unsupported.

## **Features**

- **Greeting Users:** The bot welcomes users as they join or interact.
- **Image Conversion:** Convert images to PNG format.
- **PDF Text Extraction:** Extract text from PDF files.
- **Unsupported File Types:** Inform users if the file type is unsupported.
- **Extensible Commands:** Community members can propose and add new commands.
- **Open Source Collaboration:** Follow our contribution guidelines to enhance the bot!

---

## **How to Get Started**

### **1. Fork & Clone the Repository**

To get started, fork [this](https://github.com/your-username/File-Converter-Bot) repository on GitHub and then clone it to your local system.

#### **Fork the Repository:**
Click the "Fork" button on this [repo](https://github.com/your-username/File-Converter-Bot) to create your own copy.

#### **Clone Your Fork:**
Open a terminal and run the following command:

```bash
git clone https://github.com/<your-username>/File-Converter-Bot.git
cd File-Converter-Bot