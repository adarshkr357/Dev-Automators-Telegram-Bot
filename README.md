# **Dev-Automators-Telegram-Bot**  

Welcome to **Dev-Automators-Telegram-Bot** – a community-driven Telegram bot project!  

This bot is designed to greet users with a warm welcome and serve as a foundation for adding new, useful commands. We encourage open-source contributions to expand its capabilities while ensuring that all content remains legal, professional, and free from slang or inappropriate language.  

## **Features**  

- **Greeting Users:** The bot welcomes users as they join or interact.  
- **Extensible Commands:** Community members can propose and add new commands.  
- **Open Source Collaboration:** Follow our contribution guidelines to enhance the bot!  

---

## **How to Get Started**  

### **1. Fork & Clone the Repository**  

To get started, fork [this](https://github.com/adarshkr357/Dev-Automators-Telegram-Bot) repository on GitHub and then clone it to your local system.  

#### **Fork the Repository:**  
Click the "Fork" button on this [repo](https://github.com/adarshkr357/Dev-Automators-Telegram-Bot) to create your own copy.  

#### **Clone Your Fork:**  
Open a terminal and run the following command:  

```bash
git clone https://github.com/<your-username>/Dev-Automators-Telegram-Bot.git
cd Dev-Automators-Telegram-Bot
```  

---

### **2. Get Your Bot Token from BotFather**  

To run this bot, you'll need a bot token from Telegram's [BotFather](https://t.me/BotFather).  

#### **Steps to Get Your Token:**  

1. Open [BotFather](https://t.me/BotFather) in Telegram.  
2. Start a chat and send the command `/newbot`.  
3. Follow the prompts to set a name and username for your bot.  
4. Once created, BotFather will provide you with a bot token in this format:  
   ```plaintext
   123456789:ABCDEFghijklmnopqrstuvwxyz
   ```
5. **Save this token**, as you will need it to run the bot.  

---

### **3. Set Up Your Environment**  

Once you have your bot token, create a `.env` file in the project directory (`Dev-Automators-Telegram-Bot` folder) and paste your bot token like this:  

```plaintext
BOT_TOKEN=123456789:ABCDEFghijklmnopqrstuvwxyz
```

This ensures that your bot token remains secure and isn't exposed in the source code.  

#### **Install Required Packages**  

Run the following command to install all dependencies:  

```bash
pip install -r requirements.txt
```  

---

### **4. Set Up Ngrok for Webhooks (Not needed for now, skip it)**  

If your bot uses webhooks, you'll need to expose your local server to the internet using [Ngrok](https://ngrok.com/).  

#### **1. Create an Ngrok Account**  

- **Sign Up:**  
  Visit: [Ngrok Signup](https://dashboard.ngrok.com/signup)  

- **Email Verification & Details:**  
  After verifying your Gmail, you'll be prompted to enter some details. Use the following:  
  - *How would you describe yourself?* → Student / Hobbyist (Building for fun)  
  - *What are you interested in using ngrok for?* → Testing Webhooks on local  
  - *Are you using ngrok for?* → Development  

- **Continue:**  
  Click the **Continue** button to proceed.  

#### **2. Download and Install Ngrok**  

- **Choose Your Platform:**  
  - For Windows users: [Download for Windows](https://dashboard.ngrok.com/get-started/setup/windows)  
  - For macOS users: [Download for macOS](https://dashboard.ngrok.com/get-started/setup/macos)  
  - For Linux users: [Download for Linux](https://dashboard.ngrok.com/get-started/setup/linux)  

- **Download the Zip File:**  
  Under the **Installation** section of the ngrok dashboard, click on the **Download** tab. A ZIP file will begin downloading.  

- **Extract the File:**  
  Extract the ZIP file. You will find a single file named `ngrok` (or `ngrok.exe` on Windows).  

- **Move the File:**  
  Cut and paste the `ngrok` file into your bot project's folder (`Dev-Automators-Telegram-Bot` folder).  

- **Launch Ngrok:**  
  Open the Ngrok application from your project folder.  

#### **3. Configure Your Authentication Token**  

- **Find Your Auth Token:**  
  Go back to your Ngrok dashboard ([Ngrok Dashboard](https://dashboard.ngrok.com)) and locate the command under the **configuration** section. It will look similar to:  
  ```bash
  ngrok config add-authtoken <token>
  ```
- **Apply the Token:**  
  Copy this command, paste it into the Ngrok terminal, and press **Enter**. (This is a one-time setup process.)  

#### **4. Start Tunneling Your Local Server**  

- **Open a Tunnel:**  
  In your terminal, run the following command:  
  ```bash
  ngrok http 5000
  ```
  The **5000** port is set as the default. If your Flask (or similar) server is running on a different port, replace `5000` with the correct port number:  
  ```bash
  ngrok http <PORT>
  ```
  _(Replace `<PORT>` with the port your local server is using.)_  

By following these steps, you'll successfully set up **Ngrok** to expose your local development server. 🎉  

---

## **How to Contribute**  

To contribute, please follow our standard open-source workflow:  

### **1. Create a New Branch**  

Always work on a new branch for your contribution.  

```bash
git checkout -b add-new-command
```  

### **2. Read the Contribution Guidelines**  

Please review our [CONTRIBUTORS.md](./CONTRIBUTORS.md) for detailed instructions and the expected format for your contributions.  

### **3. Make Your Changes**  

- Update or add command functionality in the code.  
- **Append your contribution** in the designated file (see below in the CONTRIBUTORS.md).  

### **4. Commit and Push Your Changes**  

```bash
git add .
git commit -m "Added new command: [Your Command Name] -> by [Your Name] - [Your Roll Number]"
git push origin add-new-command
```  

### **5. Submit a Pull Request**  

Go to your fork on GitHub and open a pull request to merge your changes into the main repository.  

---

## **Guidelines**  

- **Be Professional:** All contributions must be legal and free from slang or inappropriate language.  
- **Follow the Format:** Adhere to the guidelines provided in [CONTRIBUTORS.md](./CONTRIBUTORS.md) for adding your details or new commands.  
- **Communication:** If you encounter any issues or have questions, please ask in the group.  

---

Happy contributing and happy coding! 🚀  
— **DevInnovators Team**  
