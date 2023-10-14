import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random

# Define states for the conversation
START, QUESTION, ANSWER = range(3)

# Define the questions and answers
questions = ["What is the capital of France?",
             "What is the largest planet in our solar system?",
             "Who wrote 'Romeo and Juliet'?"]
answers = ["Paris", "Jupiter", "William Shakespeare"]

# Create a dictionary to store user scores
user_scores = {}

# Define the start function
def start(update, context):
    user_id = update.effective_user.id
    user_scores[user_id] = 0
    update.message.reply_text("Welcome to the Trivia Quiz Bot! I'll ask you some questions. Let's get started!")
    return ask_question(update, context)

# Ask a question
def ask_question(update, context):
    user_id = update.effective_user.id
    question = random.choice(questions)
    context.user_data['correct_answer'] = answers[questions.index(question)]

    update.message.reply_text(question)

    return ANSWER

# Check the answer
def check_answer(update, context):
    user_id = update.effective_user.id
    user_answer = update.message.text
    correct_answer = context.user_data['correct_answer']

    if user_answer == correct_answer:
        user_scores[user_id] += 1
        update.message.reply_text(f"Correct! Your current score is {user_scores[user_id]}.")
    else:
        update.message.reply_text(f"Sorry, the correct answer is {correct_answer}. Your current score is {user_scores[user_id]}.")

    return ask_question(update, context)

# End the quiz
def end_quiz(update, context):
    user_id = update.effective_user.id
    score = user_scores[user_id]
    update.message.reply_text(f"Quiz ended. Your final score is {score}.")
    del user_scores[user_id]

    return ConversationHandler.END

# Define the main function
def main():
    # Initialize the bot
    updater = Updater('YOUR_BOT_TOKEN', use_context=True)
    dp = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, check_answer)],
            ANSWER: [MessageHandler(Filters.text & ~Filters.command, ask_question)]
        },
        fallbacks=[MessageHandler(Filters.command, end_quiz)]
    )
    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
