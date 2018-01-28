#!/usr/bin/python3
# coding=utf8
'''
zyzy blog bot
'''
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
            Filters, RegexHandler, ConversationHandler)

import logging
import os

TOKEN = os.getenv("TG_BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PHOTO, WORDS, TAGS = range(3)

def start(bot, update):
    # reply_keyboard = [['Boy', 'Girl', 'Other']]

    # update.message.reply_text(
    #     'Hi! My name is Professor Bot. I will hold a conversation with you. '
    #     'Send /cancel to stop talking to me.\n\n'
    #     'Are you a boy or a girl?',
    #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    update.message.reply_text("Send me a photo or /cancel or /skip")
    return PHOTO

def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me some words, '
                              'or send /skip if you don\'t want to.')

    return WORDS


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me some words, '
                              'or send /skip.')

    return WORDS


def words(bot, update):
    user = update.message.from_user
    logger.info("words of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('And tags:')

    return TAGS

def skip_words(bot, update):
    user = update.message.from_user
    logger.info("skip words")
    update.message.reply_text('Bye')

    return TAGS

def tags(bot, update):
    user = update.message.from_user
    logger.info("Tags of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I got it, bye')

    return ConversationHandler.END

def skip_tags(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a tag.", user.first_name)
    update.message.reply_text('Bye')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', start)],

        states={
            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            WORDS: [MessageHandler(Filters.text, words),
                    CommandHandler('skip', skip_words)],

            TAGS: [MessageHandler(Filters.text, tags),
                    CommandHandler('skip', skip_tags)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
