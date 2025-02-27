import sqlite3
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Database setup
def init_db():
    conn = sqlite3.connect("crush_bot.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS crushes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        crush TEXT NOT NULL,
                        mutual BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()

# Add crush function
def add_crush(user, crush):
    conn = sqlite3.connect("crush_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crushes WHERE user=? AND crush=?", (crush, user))
    existing_crush = cursor.fetchone()
    if existing_crush:
        cursor.execute("UPDATE crushes SET mutual=1 WHERE user=? AND crush=?", (crush, user))
        conn.commit()
        conn.close()
        return True
    else:
        cursor.execute("INSERT INTO crushes (user, crush) VALUES (?, ?)", (user, crush))
        conn.commit()
        conn.close()
        return False

# /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Secret Crush Messenger! Send /crush @username to anonymously message your crush.')

# /crush command
def crush(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1 or not context.args[0].startswith("@"): 
        update.message.reply_text("Usage: /crush @username")
        return
    
    user = update.message.from_user.username
    crush = context.args[0][1:]
    if not user:
        update.message.reply_text("You must set a Telegram username to use this bot!")
        return
    
    if add_crush(user, crush):
        update.message.reply_text(f"💖 Mutual crush detected! You and @{crush} have liked each other! 🎉")
        context.bot.send_message(chat_id=update.message.chat_id, text=f"You and @{crush} have a match! ❤️")
    else:
        update.message.reply_text(f"✅ Your message has been sent to @{crush} anonymously! Let's see if they like you too!")
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Someone likes you! Use /crush @{user} to reveal them.")

# Main function
def main():
    init_db()
    updater = Updater("YOUR_BOT_TOKEN")  # Replace with your bot token
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("crush", crush))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
