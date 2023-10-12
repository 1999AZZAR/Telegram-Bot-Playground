import requests
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your Telegram Bot Token
TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the bot
bot = telegram.Bot(token=TOKEN)

# Function to handle user messages
def translate(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_input = update.message.text

    # Use Google Translate API
    url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=en&q={user_input}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }

    try:
        request_result = requests.get(url, headers=headers).json()
        # Extract the translation
        translation = request_result[0][0]

        # Send the translation as a response to the user
        bot.send_message(chat_id=chat_id, text=translation)
    except:
        bot.send_message(chat_id=chat_id, text="Translation failed. Please try again later.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command to start the bot
    dp.add_handler(CommandHandler("start", start))

    # Handler for user messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Translation Bot. Send me a message, and I'll translate it for you.")

if __name__ == '__main__':
    main()
