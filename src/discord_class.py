import discord
import aiohttp
import re
import asyncio
import io
import helpers
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from env_class import env


# Discord bot class
class discord_client(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Transformice (prefix ~)"))
        await self.get_channel(env.channels['debug']).send("Ready.")
        print("Connected.")

    async def on_message(self, msg):
        author = msg.author
        if author.id == self.user.id:
            return

        args = msg.content.split(" ")
        cmd = args.pop(0).lower()
        commands = env.commands

        # Compute author access
        author_access = env.PUBLIC

        cfmbot_role = discord.utils.find(lambda r: r.name == 'cfmbot', msg.guild.roles)
        if cfmbot_role in author.roles:
            author_access |= env.ADMIN

        if helpers.check_command(cmd, commands, author_access, 'help'):
            await msg.reply(embed=helpers.generate_help(author_access))
        # DEPRECATED FOR NOW, if you know how to render a png from a svg easily, pr it :]
        # Uploads the svg instead.
        elif helpers.check_command(cmd, commands, author_access, 'dressroom'):
            if len(args) < 1:
                await msg.reply("Provide a name or an outfit.")
                return

            if args[0].find(';') != -1:
                outfit = await helpers.request_mouse_outfit(args[0])
                if outfit:
                    # svg2rlg does not support line gradients.
                    # Also, reportLab always has a Division by Zero error
                    # drawing = svg2rlg(io.BytesIO(outfit))
                    # result = renderPM.drawToString(drawing, fmt="PNG")
                    await msg.reply("Download the file by clicking on the `download icon`.\nOpen the file to see "
                                    "the result.",
                                    file=discord.File(filename="mouse.svg", fp=io.BytesIO(outfit)))
                else:
                    await msg.reply('Failed to generate look. Invalid outfit.')
                    return
            else:
                profile = await helpers.request_profile(args[0])
                if profile is None:
                    await msg.reply('Could not retrieve player.')
                    return

                look = profile['shop']['look']

                outfit = await helpers.request_mouse_outfit(look)
                if outfit:
                    # svg2rlg does not support line gradients.
                    # Also, reportLab always has a Division by Zero error
                    # drawing = svg2rlg(io.BytesIO(outfit))
                    # result = renderPM.drawToString(drawing, fmt="PNG")
                    await msg.reply("Download the file by clicking on the `download icon`.\nOpen the file to see "
                                    "the result.",
                                    file=discord.File(filename="mouse.svg", fp=io.BytesIO(outfit)))
                else:
                    await msg.reply('Failed to generate look. Invalid outfit.')
                return
        elif helpers.check_command(cmd, commands, author_access, 'profile'):
            if len(args) < 1:
                await msg.reply("Provide a name or an id.")
                return

            profile = await helpers.request_profile(args[0])
            if profile:
                await msg.reply(embed=helpers.generate_profile(profile))
            else:
                await msg.reply('Could not retrieve player.')
                return
        elif helpers.check_command(cmd, commands, author_access, 'tribe'):
            if len(args) < 1:
                await msg.reply("Provide a name or an id.")
                return
            elif len(args) > 1:
                param = " ".join(args)
            else:
                param = args[0]

            tribe = await helpers.request_tribe(param)
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
        elif helpers.check_command(cmd, commands, author_access, 'search'):
            if len(args) < 1:
                await msg.reply("Provide a name.")
                return

            search_result = await helpers.request_player_search(args[0])
            if len(search_result) == 0:
                await msg.reply("Couldn't find anybody.")
                return

            await msg.reply(embed=helpers.generate_search_result(search_result))
