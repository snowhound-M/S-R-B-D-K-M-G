from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.user_data
dc = db.users_data_db


async def get_data(user_id):
    x = await dc.find_one({"user_id": user_id})
    return x


async def set_thumbnail(user_id, thumb):
    data = await get_data(user_id)
    if data and data.get("user_id"):
        await dc.update_one({"user_id": user_id}, {"$set": {"thumb": thumb}})
    else:
        await dc.insert_one({"user_id": user_id, "thumb": thumb})


async def set_caption(user_id, caption):
    data = await get_data(user_id)
    if data and data.get("user_id"):
        await dc.update_one({"user_id": user_id}, {"$set": {"caption": caption}})
    else:
        await dc.insert_one({"user_id": user_id, "caption": caption})


async def set_session(user_id, session):
    data = await get_data(user_id)
    if data and data.get("user_id"):
        await dc.update_one({"user_id": user_id}, {"$set": {"session": session}})
    else:
        await dc.insert_one({"user_id": user_id, "session": session})

async def remove_session(user_id):
    await dc.update_one({"user_id": user_id}, {"$set": {"session": None}})

async def set_channel(user_id, chat_id):
    data = await get_data(user_id)
    if data and data.get("user_id"):
        await dc.update_one({"user_id": user_id}, {"$set": {"chat_id": chat_id}})
    else:
        await dc.insert_one({"user_id": user_id, "chat_id": chat_id})


async def remove_thumbnail(user_id):
    await dc.update_one({"user_id": user_id}, {"$set": {"thumb": None}})

async def remove_caption(user_id):
    await dc.update_one({"user_id": user_id}, {"$set": {"caption": None}})
    
async def remove_channel(user_id):
    await dc.update_one({"user_id": user_id}, {"$set": {"chat_id": None}})
