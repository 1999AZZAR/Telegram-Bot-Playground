import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import sympy

# Replace 'YOUR_API_TOKEN' with your actual Telegram Bot API token
TOKEN = 'YOUR_API_TOKEN'

# Define conversation states
START, SOLVING = range(2)

# Initialize the bot
bot = telegram.Bot(token=TOKEN)

# Create a cache for memoization
memo_cache = {}

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text("Hello! I can help you solve math problems. Just send me a math expression, and I'll do my best to solve it.")
    return START

# Define a function to handle incoming text messages and solve math problems
def handle_message(update, context):
    # Get the user's message
    user_message = update.message.text

    try:
        # Check if the result is already in the cache
        if user_message in memo_cache:
            result = memo_cache[user_message]
        else:
            # Use sympy to evaluate the math expression
            result = sympy.sympify(user_message)
            # Store the result in the cache
            memo_cache[user_message] = result

        update.message.reply_text(f"The result is: {result}")
    except Exception as e:
        update.message.reply_text(f"Sorry, I couldn't solve the math problem. Error: {str(e)}")

# Define a function to cancel the conversation
def stop(update, context):
    update.message.reply_text("stoped. If you have more math problems, feel free to ask anytime.")
    return ConversationHandler.END

def main():
    # Create an Updater for the bot
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(Filters.text & ~Filters.command, handle_message)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    # Register the conversation handler
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
