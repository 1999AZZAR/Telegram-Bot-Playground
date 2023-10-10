import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gtts import gTTS
import time
import os

bot_token = "your_telegram_bot_token" 

# Define a function to send chat actions
def send_audio_actions(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.RECORD_AUDIO)
    time.sleep(2)  # Simulate recording audio for 2 seconds
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_AUDIO)
    time.sleep(2)  # Simulate sending audio for 2 seconds

# Define the voice response function
def voice_response(update, context):
    send_audio_actions(update, context)  # Send audio recording and sending actions
    text = update.message.text  # Get the incoming text message
    tts = gTTS(text=text, lang='en', tld='ca')  # Create a gTTS object with the text
    tts.save('response.mp3')  # Save the generated voice as an MP3 file
    context.bot.send_voice(chat_id=update.effective_chat.id, voice=open('response.mp3', 'rb'))

    os.remove('response.mp3')


# Define the start function
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a message, and I'll convert it to voice.")

# Set up the bot
bot = telegram.Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# Add a command handler for /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add a message handler for text messages
message_handler = MessageHandler(Filters.text & ~Filters.command, voice_response)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
