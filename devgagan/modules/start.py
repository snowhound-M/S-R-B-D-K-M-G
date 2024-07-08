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

command_buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Admin Commands", callback_data="ac"),
            InlineKeyboardButton("User Commands", callback_data="uc")
        ]
    ]
)

COMMAND_TEXT = f"`CHECK BOT COMMANDS USING THE BUTTONS GIVEN BELOW.`"

ADMIN_COMMANDS_LIST = """/auth - Update a user for premium authorization.

/remove - Delete a user from premium.

/stats - Know your Bot status.

/broadcast - Broadcast a message (with forwarding).

/announce - Broadcast a message (without forwarding).

/check - Search a premium user."""


USER_COMMANDS_LIST = """Here are the available commands:

/batch - Download bulk links one by one.

/login - Login to access bot session.

/set - Set your channel for forwarding files.

/save - Add a custom thumbnail.

/clear - Remove your thumbnail.

/logout - Logout from bot session.

/settings - Open settings to set your requirements.

/cancel - Stop batch processing."""


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(f"IDs : {OWNER_ID}")
    join = await subscribe(_, message)
    if join == 1:
        return
    await message.reply_photo(photo="https://graph.org/file/4e80dc2f4f6f2ddadb4d2.jpg",
                              caption=script.START_TXT.format(message.from_user.mention), 
                              reply_markup=buttons)

@app.on_message(filters.command("commands"))
async def user_help(_, message):
    await app.send_message(chat_id=message.chat.id, text=COMMAND_TEXT, reply_markup=command_buttons)

@app.on_callback_query()
async def callback_query_handler(_, callback_query):
    user_id = callback_query.from_user.id
    
    if callback_query.data == "ac":
        if user_id in OWNER_ID:
             return await callback_query.message.edit_text(ADMIN_COMMANDS_LIST)
        else:
             return await callback_query.answer(text=f"SORRY! Only **Admin** can view these commands.", show_alert=True)
            
    elif callback_query.data == "uc":
        return await callback_query.message.edit_text(USER_COMMANDS_LIST)
    
