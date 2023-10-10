import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import datetime

# Replace 'YOUR_API_TOKEN' with your actual Telegram Bot API token
TOKEN = 'YOUR_API_TOKEN'

# Define conversation states
START, SET_TIME, SET_MESSAGE = range(3)

# Initialize the bot
bot = telegram.Bot(token=TOKEN)

# Store user reminders
user_reminders = {}

# Define a function to start the conversation
def start(update, context):
    update.message.reply_text("Hello! I can help you set reminders. Please send me the time (HH:MM) when you want to be reminded.")

    # Transition to the SET_TIME state
    return SET_TIME

# Define a function to set the reminder time
def set_time(update, context):
    user_id = update.message.from_user.id
    time_str = update.message.text

    try:
        # Parse the user's time input into a datetime object
        reminder_time = datetime.datetime.strptime(time_str, '%H:%M').time()

        # Store the reminder time for the user
        user_reminders[user_id] = {'time': reminder_time}
        
        update.message.reply_text(f"Great! Now, please send me the reminder message.")
        
        # Transition to the SET_MESSAGE state
        return SET_MESSAGE
    except ValueError:
        update.message.reply_text("Invalid time format. Please send the time in HH:MM format.")

    # End the conversation
    return ConversationHandler.END

# Define a function to set the reminder message
def set_message(update, context):
    user_id = update.message.from_user.id
    message = update.message.text

    # Retrieve the user's reminder time
    reminder_time = user_reminders.get(user_id, {}).get('time')

    if reminder_time:
        # Calculate the datetime for the next occurrence of the reminder
        now = datetime.datetime.now().time()
        today = datetime.date.today()
        reminder_datetime = datetime.datetime.combine(today, reminder_time)
        
        if now > reminder_time:
            # If the time has already passed today, set the reminder for tomorrow
            reminder_datetime += datetime.timedelta(days=1)

        # Store the full reminder information
        user_reminders[user_id]['message'] = message
        user_reminders[user_id]['datetime'] = reminder_datetime
        
        update.message.reply_text(f"Reminder set for {reminder_datetime.strftime('%H:%M')} with the message: {message}")

        # Schedule the reminder
        schedule_reminder(update, user_id, context.job_queue)

    # End the conversation
    return ConversationHandler.END

# Define a function to schedule the reminder
def schedule_reminder(update, user_id, job_queue):
    reminder_info = user_reminders.get(user_id)

    if reminder_info:
        reminder_datetime = reminder_info['datetime']
        message = reminder_info['message']
        delay = (reminder_datetime - datetime.datetime.now()).total_seconds()

        # Schedule the reminder
        if delay > 0:
            job_queue.run_once(send_reminder, delay, context={'chat_id': update.message.chat_id, 'text': message})

# Define a function to send the reminder
def send_reminder(context):
    chat_id = context.job.context['chat_id']
    text = context.job.context['text']
    
    bot.send_message(chat_id=chat_id, text=f"⏰ Reminder: {text}")

def main():
    # Create an Updater for the bot
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SET_TIME: [MessageHandler(Filters.text & ~Filters.command, set_time)],
            SET_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, set_message)],
        },
        fallbacks=[],
    )

    # Register the conversation handler
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
