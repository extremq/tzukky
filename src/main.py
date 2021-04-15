import asyncio
import os

from env_class import env
from discord_class import discord_client

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    discord_bot = discord_client(loop=loop)
    loop.create_task(discord_bot.start(env.discord_token))

    loop.run_forever()
