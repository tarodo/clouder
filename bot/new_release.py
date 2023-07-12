import logging
import os
from functools import partial
from pathlib import Path

from pydantic import BaseModel
from read_notion import handle_release_file_from_zip
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

(INIT,) = range(1)
STATE = "State"
DONE = "Done"


class LinkModel(BaseModel):
    name: str
    domain: str
    url: str | None


class ReleaseModel(BaseModel):
    name: str
    number: str
    style: str
    mood: str
    tags: dict[str, str]
    links: list[LinkModel]


SPOTIFY_NAME = "Spotify"
YOUTUBE_NAME = "YouTube"
APPLE_NAME = "Apple"
DEEZER_NAME = "Deezer"
BEATPORT_NAME = "Beatport"

TG_NAME = "tg"
INSTA_NAME = "insta"
TWITTER_NAME = "twit"


default_tags = {
    f"dnb:melodic:{TG_NAME}": "#DNB #melodic #chart",
    f"dnb:party:{TG_NAME}": "#DNB #party #chart",
    f"dnb:melancholy:{TG_NAME}": "#DNB #melancholy #chart",
    f"dnb:redrum:{TG_NAME}": "#DNB #redrum #chart",
    f"dnb:hard:{TG_NAME}": "#DNB #hard #chart",
    f"dnb:shadowy:{TG_NAME}": "#DNB #shadowy #chart",
    f"dnb:melodic:{INSTA_NAME}": "#dnb #melodic #clouder_melodic #clouder_chart #clouder #liquid #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:party:{INSTA_NAME}": "#dnb #party #clouder_party #clouder_chart #clouder #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:melancholy:{INSTA_NAME}": "#dnb #melancholy #clouder_melancholy #clouder_chart #clouder #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:redrum:{INSTA_NAME}": "#dnb #redrum #clouder_redrum #clouder_chart #clouder #drumfunk #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:hard:{INSTA_NAME}": "#dnb #hard #clouder_hard #clouder_chart #clouder #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:shadowy:{INSTA_NAME}": "#dnb #shadowy #clouder_shadowy #clouder_chart #clouder #dnbchart #musicchart #music2023 #dnb2023",
    f"dnb:melodic:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_melodic",
    f"dnb:party:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_party",
    f"dnb:melancholy:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_melancholy",
    f"dnb:redrum:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_redrum",
    f"dnb:hard:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_hard",
    f"dnb:shadowy:{TWITTER_NAME}": "#dnb #playlist #chart #clouder_dnb_shadowy",
    f"techno:mid:{TG_NAME}": "#Techno #mid #chart",
    f"techno:low:{TG_NAME}": "#Techno #low #chart",
    f"techno:mid:{INSTA_NAME}": "#techno #melody #technomusic #clouder_techno #clouder_chart #clouder #technochart #musicchart #music2023 #techno2023",
    f"techno:low:{INSTA_NAME}": "#techno #melody #technomusic #clouder_techno #clouder_chart #clouder #technochart #musicchart #music2023 #techno2023",
    f"techno:mid:{TWITTER_NAME}": "#techno #playlist #chart #clouder_techno_mid",
    f"techno:low:{TWITTER_NAME}": "#techno #playlist #chart #clouder_techno_low",
    f"house:vocal:{TG_NAME}": "#House #vocal #chart",
    f"house:vocal:{INSTA_NAME}": "#house #vocal #housemusic #clouder_house #clouder_chart #clouder #housechart #musicchart #music2023 #house2023",
    f"house:vocal:{TWITTER_NAME}": "#house #playlist #chart #clouder_house_vocal",
}

reply_keyboard = [
    [STATE, DONE],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def get_new_links() -> list[LinkModel]:
    return [
        LinkModel(name=SPOTIFY_NAME, domain="https://open.spotify.com/playlist/"),
        LinkModel(name=YOUTUBE_NAME, domain="https://music.youtube.com/playlist?list="),
        LinkModel(name=APPLE_NAME, domain="https://music.apple.com/rs/playlist/"),
        LinkModel(name=DEEZER_NAME, domain="https://deezer.page.link/"),
        LinkModel(name=BEATPORT_NAME, domain="https://www.beatport.com/chart/"),
    ]


async def show_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply state of release"""
    release_state: ReleaseModel = context.user_data["release"]
    text = f"Release name : {release_state.name}\n"
    for link in release_state.links:
        text += f"{link.name} :: {link.url}\n"
    await update.message.reply_text(text, reply_markup=markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    context.user_data["release"] = ReleaseModel(
        name="", tags={}, links=get_new_links(), number="", style="", mood=""
    )
    await update.message.reply_text(
        "Hi! Let's start to create new release.\n"
        "Send me all 5 links and I'll give you posts for social media with tags and links.\n"
        "You can cancel process in any time just by using /cancel",
        reply_markup=markup,
    )
    await show_state(update, context)

    return INIT


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Have fun!",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    context.user_data["release"] = None
    return ConversationHandler.END


def update_release_name(release: ReleaseModel) -> bool:
    style = release.style.capitalize()
    if style == "Dnb":
        style = style.upper()
    mood = release.mood.capitalize()
    new_name = f"cLoudER {release.number} : {style} : {mood}"
    release.name = new_name
    return True


def update_release_tags(release: ReleaseModel) -> bool:
    for platform in [TG_NAME, INSTA_NAME, TWITTER_NAME]:
        release.tags[platform] = default_tags[
            f"{release.style}:{release.mood}:{platform}"
        ]
    return True


async def finish_release(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    release: ReleaseModel = context.user_data.get("release")
    for tag in release.tags:
        if tag == TG_NAME:
            text = f"*{release.name}*"
            tags_mark2 = release.tags[tag].replace("#", r"\#")
            text += f"\n{tags_mark2}"
            for link in release.links:
                text += f"\n[{link.name}]({link.url})"
            await update.message.reply_text(text, parse_mode="MarkdownV2")
        if tag == INSTA_NAME:
            text = release.name
            text += f"\n{release.tags[tag]}"
            text += f"\nPlaylist is in Stories or by the link in the account profile"
            await update.message.reply_text(text)
        if tag == TWITTER_NAME:
            text = release.name
            text += f"\n{release.tags[tag]}"
            for link in release.links:
                text += f"\n{link.name} : {link.url}"
            await update.message.reply_text(text)
    return await done(update, context)


def handle_one_link(release_state: ReleaseModel, new_link: str) -> list[str]:
    updated = []
    for link in release_state.links:
        if not new_link.startswith(link.domain):
            continue
        link.url = new_link
        updated.append(link.name)
        if link.name == APPLE_NAME:
            release_name = link.url.replace(link.domain, "")
            release_name = release_name.split("/")[0]
            release_name = release_name.split("-")
            release_state.number = release_name[1]
            release_state.style = release_name[2]
            release_state.mood = release_name[3]
            update_release_name(release_state)
            update_release_tags(release_state)
            updated.append("Release Name")
        break
    return updated


async def handle_link_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle the link of one playlist"""
    user_text = update.message.text
    release_state: ReleaseModel = context.user_data["release"]
    updated = handle_one_link(release_state, user_text)

    for one_update in updated:
        await update.message.reply_text(
            f"Update :: '{one_update}'", reply_markup=markup
        )

    is_full = True
    for link in release_state.links:
        if not link.url:
            is_full = False
            break
    if is_full:
        return await finish_release(update, context)
    return INIT


async def handle_file(
    temp_dir: str, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    file = await context.bot.get_file(update.message.document)
    Path(temp_dir).mkdir(exist_ok=True)
    file_name = update.message.document.file_name
    file_path = Path(temp_dir, file_name)
    await file.download(file_path)

    links = handle_release_file_from_zip(temp_dir, file_name)
    release_state: ReleaseModel = context.user_data["release"]
    for link in links.values():
        updated = handle_one_link(release_state, link)
        for one_update in updated:
            await update.message.reply_text(
                f"Update :: '{one_update}'", reply_markup=markup
            )

    os.remove(file_path)

    return await finish_release(update, context)


def get_new_release_conv(temp_dir: str) -> ConversationHandler:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("new", start)],
        states={
            INIT: [
                MessageHandler(filters.Regex(f"^{STATE}$"), show_state),
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    handle_link_message,
                ),
                MessageHandler(filters.Document.ALL, partial(handle_file, temp_dir)),
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^Done$"), done),
            CommandHandler("cancel", done),
        ],
    )
    return conv_handler
