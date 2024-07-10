from devgagan import app
from pyrogram import filters
from config import OWNER_ID
from devgagan.core.mongo.users_db import get_users, add_user, get_user
from devgagan.core.mongo.plans_db import premium_users


@app.on_message(filters.command("stats"))
async def stats(client, message):
    users = len(await get_users())
    premium = await premium_users()
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}
**Premium Users** : {len(premium)}

**__Powered by M. Player.__**
""")
  
