import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Replace 'YOUR_API_KEY' with your actual Telegram Bot API Key
API_KEY = 'YOUR_API_KEY'

# Create an Updater object and pass in your API key
updater = Updater(token=API_KEY, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Define a function to echo the user's messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Register the echo function with a MessageHandler
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# Define a /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am your Echo Bot. Send me a message, and I'll echo it back to you.")

# Register the start function with a CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()

# Run the bot until you send a signal to stop (e.g., Ctrl+C)
updater.idle()
