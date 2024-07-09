import asyncio
import time
import os
import subprocess
import requests
from devgagan import app
from devgagan import sex as gf
import pymongo
from pyrogram import filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from devgagan.core.func import progress_bar, video_metadata, screenshot
from devgagan.core.mongo import db
from pyrogram.types import Message
from config import MONGO_DB as MONGODB_CONNECTION_STRING, LOG_GROUP
import cv2
from telethon import events, Button
    
    
def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None

async def get_msg(userbot, sender, edit_id, msg_link, i, message):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' not in msg_link:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        else:
            chat = msg_link.split("/")[-2]       
        file = ""
        try:
            chatx = message.chat.id
            msg = await userbot.get_messages(chat, msg_id)

            if msg.service is not None:
                return None 
            if msg.empty is not None:
                return None                          
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(target_chat_id, edit_id, "Cloning...")
                    devggn = await app.send_message(sender, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devggn.pin(both_sides=True)
                        except Exception as e:
                            await devggn.pin()
                    await devggn.copy(LOG_GROUP)                  
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(target_chat_id, edit_id, "Cloning...")
                    devggn = await app.send_message(sender, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devggn.pin(both_sides=True)
                        except Exception as e:
                            await devggn.pin()
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
            
            edit = await app.edit_message_text(sender, edit_id, "Trying to Download...")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("**__Downloading: __**\n",edit,time.time()))
            
            await edit.edit('Preparing to Upload...')
            
            if msg.media == MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:

                metadata = video_metadata(file)      
                width= metadata['width']
                height= metadata['height']
                duration= metadata['duration']

                if duration <= 300:
                    devggn = await app.send_video(chat_id=sender, video=file, caption=caption, height=height, width=width, duration=duration, thumb=None, progress=progress_bar, progress_args=('**UPLOADING:**\n', edit, time.time())) 
                    if msg.pinned_message:
                        try:
                            await devggn.pin(both_sides=True)
                        except Exception as e:
                            await devggn.pin()
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
                
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                lines = final_caption.split('\n')
                processed_lines = []
                for line in lines:
                    for word in delete_words:
                        line = line.replace(word, '')
                    if line.strip():
                        processed_lines.append(line.strip())
                final_caption = '\n'.join(processed_lines)
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                
                thumb_path = await screenshot(file, duration, chatx)              
                try:
                    devggn = await app.send_video(
                        chat_id=target_chat_id,
                        video=file,
                        caption=caption,
                        supports_streaming=True,
                        height=height,
                        width=width,
                        duration=duration,
                        thumb=thumb_path,
                        progress=progress_bar,
                        progress_args=(
                        '**__Uploading...__**\n',
                        edit,
                        time.time()
                        )
                       )
                    if msg.pinned_message:
                        try:
                            await devggn.pin(both_sides=True)
                        except Exception as e:
                            await devggn.pin()
                    await devggn.copy(LOG_GROUP)
                except:
                    await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.")

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("**`Uploading photo...`")
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                lines = final_caption.split('\n')
                processed_lines = []
                for line in lines:
                    for word in delete_words:
                        line = line.replace(word, '')
                    if line.strip():
                        processed_lines.append(line.strip())
                final_caption = '\n'.join(processed_lines)
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(sender, sender)
                devggn = await app.send_photo(chat_id=target_chat_id, photo=file, caption=caption)
                if msg.pinned_message:
                    try:
                        await devggn.pin(both_sides=True)
                    except Exception as e:
                        await devggn.pin()                
                await devggn.copy(LOG_GROUP)
            else:
                thumb_path = thumbnail(chatx)
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                lines = final_caption.split('\n')
                processed_lines = []
                for line in lines:
                    for word in delete_words:
                        line = line.replace(word, '')
                    if line.strip():
                        processed_lines.append(line.strip())
                final_caption = '\n'.join(processed_lines)
                replacements = load_replacement_words(chatx)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                try:
                    devggn = await app.send_document(
                        chat_id=target_chat_id,
                        document=file,
                        caption=caption,
                        thumb=thumb_path,
                        progress=progress_bar,
                        progress_args=(
                        '**`Uploading...`**\n',
                        edit,
                        time.time()
                        )
                    )
                    if msg.pinned_message:
                        try:
                            await devggn.pin(both_sides=True)
                        except Exception as e:
                            await devggn.pin()

                    await devggn.copy(LOG_GROUP)
                except:
                    await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.") 
                
                os.remove(file)
                        
            await edit.delete()
        
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await app.edit_message_text(sender, edit_id, "Have you joined the channel?")
            return
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')       
        
    else:
        edit = await app.edit_message_text(sender, edit_id, "Cloning...")
        try:
            chat = msg_link.split("/")[-2]
            await copy_message_with_chat_id(app, sender, chat, msg_id) 
            await edit.delete()
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')


async def copy_message_with_chat_id(client, sender, chat_id, message_id):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    target_chat_id = user_chat_ids.get(sender, sender)
    
    try:
        # Fetch the message using get_message
        msg = await client.get_messages(chat_id, message_id)
        
        # Modify the caption based on user's custom caption preference
        custom_caption = get_user_caption_preference(sender)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
        
        delete_words = load_delete_words(sender)
        for word in delete_words:
            final_caption = final_caption.replace(word, '  ')
        
        replacements = load_replacement_words(sender)
        for word, replace_word in replacements.items():
            final_caption = final_caption.replace(word, replace_word)
        
        caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
        
        if msg.media:
            if msg.media == MessageMediaType.VIDEO:
                result = await client.send_video(target_chat_id, msg.video.file_id, caption=caption)
            elif msg.media == MessageMediaType.DOCUMENT:
                result = await client.send_document(target_chat_id, msg.document.file_id, caption=caption)
            elif msg.media == MessageMediaType.PHOTO:
                result = await client.send_photo(target_chat_id, msg.photo.file_id, caption=caption)
            else:
                # Use copy_message for any other media types
                result = await client.copy_message(target_chat_id, chat_id, message_id)
        else:
            # Use copy_message if there is no media
            result = await client.copy_message(target_chat_id, chat_id, message_id)

        # Attempt to copy the result to the LOG_GROUP
        try:
            await result.copy(LOG_GROUP)
        except Exception:
            pass
            
        if msg.pinned_message:
            try:
                await result.pin(both_sides=True)
            except Exception as e:
                await result.pin()

    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {target_chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {target_chat_id} and restart the process after /cancel")

# ------------------------ Button Mode Editz FOR SETTINGS ----------------------------

# MongoDB database name and collection name
DB_NAME = "smart_users"
COLLECTION_NAME = "super_user"

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_authorized_users():
    """
    Load authorized user IDs from the MongoDB collection
    """
    authorized_users = set()
    for user_doc in collection.find():
        if "user_id" in user_doc:
            authorized_users.add(user_doc["user_id"])
    return authorized_users

def save_authorized_users(authorized_users):
    """
    Save authorized user IDs to the MongoDB collection
    """
    collection.delete_many({})
    for user_id in authorized_users:
        collection.insert_one({"user_id": user_id})

SUPER_USERS = load_authorized_users()

# Define a dictionary to store user chat IDs
user_chat_ids = {}

# MongoDB database name and collection name
MDB_NAME = "logins"
MCOLLECTION_NAME = "stringsession"

# Establish a connection to MongoDB
m_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
mdb = m_client[MDB_NAME]
mcollection = mdb[MCOLLECTION_NAME]

def load_delete_words(user_id):
    """
    Load delete words for a specific user from MongoDB
    """
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return set(words_data.get("delete_words", []))
        else:
            return set()
    except Exception as e:
        print(f"Error loading delete words: {e}")
        return set()

def save_delete_words(user_id, delete_words):
    """
    Save delete words for a specific user to MongoDB
    """
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"delete_words": list(delete_words)}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving delete words: {e}")

def load_replacement_words(user_id):
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return words_data.get("replacement_words", {})
        else:
            return {}
    except Exception as e:
        print(f"Error loading replacement words: {e}")
        return {}

def save_replacement_words(user_id, replacements):
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"replacement_words": replacements}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving replacement words: {e}")

# Initialize the dictionary to store user preferences for renaming
user_rename_preferences = {}

# Initialize the dictionary to store user caption
user_caption_preferences = {}

# Function to load user session from MongoDB
def load_user_session(sender_id):
    user_data = collection.find_one({"user_id": sender_id})
    if user_data:
        return user_data.get("session")
    else:
        return None  # Or handle accordingly if session doesn't exist

# Function to handle the /setrename command
async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

# Function to get the user's custom renaming preference
def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to '@devggn'
    return user_rename_preferences.get(str(user_id), '@devggn')

# Function to set custom caption preference
async def set_caption_command(user_id, custom_caption):
    # Update the user_caption_preferences dictionary
    user_caption_preferences[str(user_id)] = custom_caption

# Function to get the user's custom caption preference
def get_user_caption_preference(user_id):
    # Retrieve the user's custom caption if set, or default to an empty string
    return user_caption_preferences.get(str(user_id), '')

# Initialize the dictionary to store user sessions

sessions = {}

SET_PIC = "settings.jpg"
MESS = "Customize by your end and Configure your settings ..."

setting_buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Set Chat ID", callback_data="set"),
            InlineKeyboardButton("Remove Chat ID", callback_data="remove")
        ],
        [
            InlineKeyboardButton("Set Caption", callback_data="scap"),
            InlineKeyboardButton("Delete Caption", callback_data="dcap")
        ],
        [
            InlineKeyboardButton("Create Batch", callback_data="batch"),
            InlineKeyboardButton("Cancel Batch", callback_data="cancel")
        ],
        [
            InlineKeyboardButton("Add Thumbnail", callback_data="add"),
            InlineKeyboardButton("Remove Thumbnail", callback_data="clear")
        ],
        [
            InlineKeyboardButton("Login", callback_data="login")
        ],
        [
            InlineKeyboardButton("Logout", callback_data="logout")
        ]
    ]
)


@app.on_message(filters.command("settings"))
async def user_help(app, message):
    await app.send_file(chat_id=message.chat.id, file=SET_PIC, caption=MESS, reply_markup=setting_buttons)


@app.on_message(
    filters.command(["set", "remove", "scap", "dcap", "batch", "cancel", "save", "clear", "login", "logout"])
)
@app.on_callback_query(
)
async def callback_query_handler(_, callback_query):
    user_id = callback_query.message.chat.id
    
    try:
        if isinstance(callback_query, Message):
            C = callback_query.command
            if "set" in C:
                await callback_query.reply("Send the chat ID that you want to set.")
                sessions[user_id] = "set"
            elif "remove" in C:
                await callback_query.reply("Send YES REMOVE to confirm.")
                sessions[user_id] = "remove"
            elif "scap" in C:
                await callback_query.reply("Send the caption that you want to set.")
                sessions[user_id] = "scap"
            elif "dcap" in C:
                await callback_query.reply("Send YES DELETE to confirm.")
                sessions[user_id] = "dcap"
            elif "batch" in C:
                await batch_link(_, callback_query)
            elif "cancel" in C:
                await stop_batch(_, callback_query)
            elif "save" in C:
                await callback_query.reply("Send the photo you want to set as thumbnail.")
                sessions[user_id] = "save"
            elif "clear" in C:
                await callback_query.reply("Send YES CLEAR to confirm.")
                sessions[user_id] = "clear"
            elif "login" in C:
                await generate_session(_, callback_query)
            elif "logout" in C:
                result = mcollection.delete_one({"user_id": user_id})
                if result.deleted_count > 0:
                      await event.respond("Logged out and deleted session successfully.")
                else:
                      await event.respond("You are not logged in")
                
        elif isinstance(callback_query, CallbackQuery):
            Q = callback_query.data
            if str(Q) == "set":
                await callback_query.message.reply_text("Send the chat ID that you want to set.")
                sessions[user_id] = "set"
            elif str(Q) == "remove":
                await callback_query.message.reply_text("Send YES REMOVE to confirm.")
                sessions[user_id] = "remove"
            elif str(Q) == "scap":
                await callback_query.message.reply_text("Send the caption that you want to set.")
                sessions[user_id] = "scap"
            elif str(Q) == "dcap":
                await callback_query.message.reply_text("Send YES DELETE to confirm.")
                sessions[user_id] = "dcap"
            elif str(Q) == "batch":
                await batch_link(_, callback_query.message)
            elif str(Q) == "cancel":
                await stop_batch(_, callback_query.message)
            elif str(Q) == "save":
                await callback_query.message.reply_text("Send the photo you want to set as thumbnail.")
                sessions[user_id] = "save"
            elif str(Q) == "clear":
                await callback_query.reply("Send YES CLEAR to confirm.")
                sessions[user_id] = "clear"
            elif str(Q) == "login":
                await generate_session(_, callback_query.message)
            elif str(Q) == "logout":
                result = mcollection.delete_one({"user_id": user_id})
                if result.deleted_count > 0:
                      await event.respond("Logged out and deleted session successfully.")
                else:
                      await event.respond("You are not logged in")
                
    except Exception as e:
        await callback_query.reply(f"ERROR : {str(e)}")


@app.on_message(group=10)
async def handle_user_input(app, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass

    user_id = message.chat.id

    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == "set":
            try:
                chat_id = int(message.text)
                await set_channel(user_id, chat_id)
                await message.reply("Chat ID set successfully!")
            except ValueError:
                await message.reply("Invalid chat ID!")
            except: 
                await message.reply("Chat ID set request failed.")
        
        elif session_type == "remove":
            if message.text == "YES REMOVE":
                try:
                    await remove_channel(user_id)
                    await message.reply("Chat ID removed successfully!")
                except:
                    await message.reply("Chat ID remove request failed!")
            else:
                await message.reply("Cancelled your request.")
            
        elif session_type == "scap":
            try:
                caption = message.text
                await set_caption(user_id, caption)
                await message.reply("Caption set successfully!")
            except:
                await message.reply("Caption failed.")
                
        elif session_type == "dcap":
            if message.text == "YES DELETE":
                try:
                    await remove_caption(user_id)
                    await message.reply("Caption deleted successfully!")
                except:
                    await message.reply("Caption delete request failed.")
            else:
                await message.reply("Cancelled your request.")
        
        elif session_type == "save":
            if message.photo:
                thumb = message.photo.file_id
                await set_thumbnail(user_id, thumb)
                await message.reply("Thumbnail added successfully!")
            else:
                await message.reply("Please send a photo... Retry")

        elif session_type == "clear":
            try:
                await remove_thumbnail(user_id)
                await message.reply("Thumbnail cleared successfully!")
            except:
                await message.reply("No thumbnail found to clear.")

        del sessions[user_id]
