import os
import asyncio
import aiotfm

from env_class import env
from discord_class import discord_client
from tfm_class import tfm_client

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    discord_bot = discord_client(loop=loop, tfm_bot=tfm_client(community=aiotfm.enums.Community.en, bot_role=True))

    loop.create_task(discord_bot.tfm_bot.start(env.tfm_user, env.tfm_pass))
    loop.create_task(discord_bot.start(env.discord_token))

    loop.run_forever()
