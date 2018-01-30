#!/usr/bin/python3
# coding=utf8
'''
zyzy blog bot
'''
import logging
import os
import blog
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
            Filters, RegexHandler, ConversationHandler)


TOKEN = os.getenv("TG_BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, PHOTO, WORDS, TAGS, WRITE = range(5)

post = dict()

user_photo = 'user_photo.jpg'

CHOICE = ['Photo', 'Words', 'Both']
DEFAULT_KEYBOARD = [["/new", "/cancel"], CHOICE]
COMMON_TAGS = ["碎碎念", "日记", "胡言乱语", "语录", "随想"]
TAGS_KEYBOARD = [COMMON_TAGS, ["/skip", "/cancel", "done"]]

def prepare():
    post.clear()
    try:
        os.remove(user_photo)
    except Exception as e:
        pass

def end(update):
    update.message.reply_text('Bye~~',
        reply_markup=ReplyKeyboardMarkup(DEFAULT_KEYBOARD, one_time_keyboard=False))


def write(update):
    logger.info("content: %s; tags: %s; photo: %s",
        post.get("words"), post.get("tags"), post.get("photo"))
    update.message.reply_text('Write done.', reply_markup=ReplyKeyboardRemove())
    b = blog.blog(post.get("words"), post.get("tags"), image=post.get("photo"))
    b.write_post()
    # b.print_post()
    end(update)
    return ConversationHandler.END


def new_post(bot, update):
    prepare()
    update.message.reply_text('What can I do for you, my lord?',
        reply_markup=ReplyKeyboardMarkup(DEFAULT_KEYBOARD, one_time_keyboard=True))

    return START


def start(bot, update):
    logger.info("start")
    choice = update.message.text
    if choice not in DEFAULT_KEYBOARD[1]:
        update.message.reply_text("Sorry my lord, I don't understand...")
        end(update)
        return ConversationHandler.END

    logger.info("user choice %s", choice)
    if choice == "Words":
        post["type"] = "words"
        logger.info("get into words")
        update.message.reply_text('Please send me some words.')
        return WORDS

    if choice == "Photo":
        post["type"] = "photo"
    else:
        post["type"] = "both"

    logger.info("here is photo")
    post["photo"] = False
    update.message.reply_text("Send me a photo.")
    return PHOTO

def photo(bot, update):
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download(user_photo)
    post["photo"] = user_photo
    logger.info("Got photo: %s", user_photo)
    if post["type"] == "both":
        logger.info("get into words")
        update.message.reply_text('Please send me some words.')
        return WORDS

    logger.info("come into tags")
    update.message.reply_text('Any tags?',
        reply_markup=ReplyKeyboardMarkup(TAGS_KEYBOARD, one_time_keyboard=False))

    return TAGS


def skip_photo(bot, update):
    logger.info("skip photo")
    if post["type"] == "both":
        logger.info("get into words")
        update.message.reply_text('Please send me some words.')
        return WORDS
    

    logger.info("come into tags")
    update.message.reply_text('Any tags?',
        reply_markup=ReplyKeyboardMarkup(TAGS_KEYBOARD, one_time_keyboard=False))

    return TAGS

def words(bot, update):
    user = update.message.from_user
    got_words = update.message.text
    logger.info("words of %s: %s", user.first_name, got_words)
    post["words"] = got_words

    logger.info("come into tags")
    update.message.reply_text('Any tags?',
        reply_markup=ReplyKeyboardMarkup(TAGS_KEYBOARD, one_time_keyboard=False))

    return TAGS

def skip_words(bot, update):
    logger.info("come into tags")
    update.message.reply_text('Any tags?',
        reply_markup=ReplyKeyboardMarkup(TAGS_KEYBOARD, one_time_keyboard=False))

    return TAGS

def tags(bot, update):
    if not post.get("tags"):
        post["tags"] = []

    tag = update.message.text
    if tag != "done":
        if tag not in post["tags"]:
            logger.info("get new tag %s", tag)
            update.message.reply_text("Got tag " + tag)
            post["tags"].append(tag)
        else:
            update.message.reply_text("Already have " + tag)
        return TAGS

    update.message.reply_text('Tags: {}'.format(post["tags"]))
    return write(update)

def skip_tags(bot, update):
    update.message.reply_text('Skip tags. As you wish.')
    return write(update)

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    end(update)
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
        entry_points=[CommandHandler('new', new_post)],

        states={
            START: [MessageHandler(Filters.text, start)],

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
    updater.start_polling(timeout=60)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
