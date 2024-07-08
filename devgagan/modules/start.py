from pyrogram import filters
from devgagan import app
from devgagan.core import script
from devgagan.core.func import subscribe
from config import OWNER_ID
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Join Channel", url="https://t.me/+pK1Eu44q7ugyYTM9")],
        [InlineKeyboardButton("Buy Premium", url="tg://openmessage?user_id=1303122772")]
    ]
)

CONTACT_URL = "tg://openmessage?user_id=6621306807"

HELP_TEXT = """Here are the available commands:

/batch - Download bulk links one by one.

/login - Login to access bot session.

/set - Set your channel for forwarding files.

/save - Add a custom thumbnail.

/clear - Remove your thumbnail.

/logout - Logout from bot session.

/settings - Open settings to set your requirements.

/cancel - Stop batch processing.

/auth [Admin Only] - Update a user for premium authorization.

/remove [Admin Only] - Delete a user from premium.

/stats [Admin Only] - Know your Bot status.

/broadcast [Admin Only] - Broadcast a message (with forwarding).

/announce [Admin Only] - Broadcast a message (without forwarding).

/check [Admin Only] - Search a premium user.

[Contact Admin Here](%s)
""" % CONTACT_URL


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(f"IDs : {OWNER_ID}")
    join = await subscribe(_, message)
    if join == 1:
        return
    await message.reply_photo(photo="https://graph.org/file/4e80dc2f4f6f2ddadb4d2.jpg",
                              caption=script.START_TXT.format(message.from_user.mention), 
                              reply_markup=buttons)

@app.on_message(filters.command("/help"))
async def user_help(_, message):
    await app.send_message(message.chat.id, HELP_TEXT)
