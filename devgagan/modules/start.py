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


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(f"IDs : {OWNER_ID}")
    join = await subscribe(_, message)
    if join == 1:
        return
    await message.reply_photo(photo="https://graph.org/file/4e80dc2f4f6f2ddadb4d2.jpg",
                              caption=script.START_TXT.format(message.from_user.mention), 
                              reply_markup=buttons)
    
