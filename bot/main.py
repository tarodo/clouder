import logging
import os
from functools import partial

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_release_info(release_url) -> dict:
    res = requests.get(release_url)
    if res.ok:
        return res.json()


async def show_release(
    release_url, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    release = get_release_info(release_url)
    version = release["name"]
    await update.message.reply_text(f"Актуальный релиз :: {version}")


def main() -> None:
    """Run the bot."""
    bot_token = os.getenv("BOT_TOKEN")
    release_url = os.getenv("RELEASE_URL")
    application = Application.builder().token(bot_token).build()
    application.add_handler(
        CommandHandler("release", partial(show_release, release_url))
    )

    application.run_polling()


if __name__ == "__main__":
    main()
