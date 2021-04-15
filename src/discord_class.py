import discord
import aiohttp
import re
import asyncio
import io
import helpers

from env_class import env


# Discord bot class
class discord_client(discord.Client):

    async def on_ready(self):
        await self.get_channel(env.channels.debug).send("Ready.")
        print("Connected.")

    async def on_message(self, msg):
        author = msg.author
        args = msg.content.split(" ")
        cmd = args.pop(0).lower()

        if author.id == self.user.id:
            return

        if cmd == "~!dressroom":
            if args[0] is None:
                await msg.reply("Provide a name or an outfit.")
                return

            # Outfit provided
            if args[0].find(';'):
                outfit = await helpers.request_mouse_outfit(args[0])
                if outfit:
                    pass  # Can't generate PNG from SVG...
                else:
                    await msg.reply('Failed to generate look. Invalid outfit.')
                    return
            # Name provided
            else:
                profile = await helpers.request_profile(args[0])
                if profile:
                    await msg.reply(helpers.generate_profile(profile))
                else:
                    await msg.reply('Could not retrieve player.')
                    return

                outfit = profile['outfit']

                #  Request outfit
                outfit = await helpers.request_mouse_outfit(args[0])
                if outfit:
                    pass  # Can't generate PNG from SVG...
                else:
                    await msg.reply('Failed to generate look. Invalid outfit.')
                return
        elif cmd == "!profile":
            if args[0] is None:
                await msg.reply("Provide a name or an id.")
                return

            profile = await helpers.request_profile(args[0])
            if profile:
                await msg.reply(embed=helpers.generate_profile(profile))
            else:
                await msg.reply('Could not retrieve player.')
                return
        elif cmd == "!tribe":
            if args[0] is None:
                await msg.reply("Provide a name or an id.")
                return

            tribe = await helpers.request_tribe(args[0])
            if tribe:
                tribe_id = tribe['id']
            else:
                await msg.reply("Failed to retrieve tribe id.")
                return

            tribe_members = await helpers.request_tribe_members(str(tribe_id), "?limit=25")
            if not tribe_members:
                await msg.reply("Failed to retrieve members.")
                return

            await msg.reply(embed=helpers.generate_tribe(tribe, tribe_members))

