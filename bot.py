"""
RobotDogger's Decider Bot (RDeciderBot)

Tired of having trouble deciding what to do with your friends?
Like having a list of series or movies and not being able to decide which one to watch
Or have a list of video games and can't decide which one to play
I'm here to help you choose a totally random and unbiased option to avoid that bullshit

Author: RobotDogger
Telegram Bot: https://t.me/rdeciderbot
"""

import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from random import choice

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "1532726513:AAGan17BF5hn8lBcRMFKZY3IrqMeeWjUmo0"
PORT = int(os.environ.get('PORT', 5000))
ADDRESS = "https://safe-scrubland-23143.herokuapp.com/"

options = []

def concat(l):
    r = ""
    for e in l:
        r += e + " "
    return r[:-1]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html('Hello!\n\nI\'m ready to take note of your options\n\nUse <code>/help</code> for instructions')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_html("&#8226; Just use <code>/add 'new option'</code> to add an option into the list\n\n&#8226; When you're ready use <code>/choose</code> to pick one\n\n&#8226; Wanna see the list?\n\t\t\t\tUse <code>/list</code>\n\n&#8226; Wanna clear the list?\n\t\t\t\tUse <code>/clear</code>\n\n&#8226; Wanna delete a specific option?\n\t\t\t\tUse <code>/delete 'option to delete'</code>, please be specific")
    
def add(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(concat(context.args)+" added!")
    options.append(concat(context.args))

def choose(update: Update, context: CallbackContext) -> None:
    if(not options):
        update.message.reply_html("Please add options first, you can't choose something from nothing")
    else:
        update.message.reply_html("Congrats, "+choice(options)+" won!")

def see(update: Update, context: CallbackContext) -> None:
    if(not options):
        update.message.reply_html("List is empty, please add options first")
    else:
        l = ""
        for e in options:
            l += "&#8226; " + e + "\n"
        update.message.reply_html("<b>List:</b>\n\n"+l)

def clear(update: Update, context: CallbackContext) -> None:
    options.clear()
    update.message.reply_html("List cleared!")

def delete(update: Update, context: CallbackContext) -> None:
    td = concat(context.args)
    options.remove(td)
    update.message.reply_html(concat(context.args)+" deleted!")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("choose", choose))
    dispatcher.add_handler(CommandHandler("list", see))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CommandHandler("delete", delete))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(ADDRESS + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()