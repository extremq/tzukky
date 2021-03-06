import os
import asyncio
import aiotfm

from env_class import env
from discord_class import discord_client
from tfm_class import tfm_client

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    discord_bot = discord_client()
    tfm_bot = tfm_client(community=aiotfm.enums.Community.en, bot_role=True)

    # Establish communication between the bots
    discord_bot.set_tfm_bot(tfm_bot)

    loop.create_task(discord_bot.start(env.discord_token))
    tfm_bot.set_discord_bot(discord_bot)
    loop.create_task(tfm_bot.start(env.tfm_user, env.tfm_pass))

    loop.run_forever()
