import os
import logging

from .lib import (
    SpotifyAPI,
    spotify_to_apple,
    NotSpotifyException,
    UnhandledSpotifyEntity,
)

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"""Hi {user.mention_markdown_v2()}\!""",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def generate_echo(spotify_api: SpotifyAPI):
    def echo(update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        try:
            update.message.reply_text(
                spotify_to_apple(spotify_api, update.message.text)
            )
            logging.info(f"{update.effective_user.mention_markdown_v2()} translated this song: {update.message.text}")
        except NotSpotifyException as ex:
            update.message.reply_text("You did not provide a spotify URL")
            logging.info(f"{update.effective_user.mention_markdown_v2()} did not provide a spotify url: {update.message.text}")
        except UnhandledSpotifyEntity as ex:
            update.message.reply_text("Cannot convert this spotify URL")
            logging.info(f"{update.effective_user.mention_markdown_v2()} could not convert: {update.message.text}")

    return echo


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ["TELEGRAM_TOKEN"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    spotify_api = SpotifyAPI(
        refresh_token=os.environ["SPOTIFY_REFRESH_TOKEN"],
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    )

    echo = generate_echo(spotify_api)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
