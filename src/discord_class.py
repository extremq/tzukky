import aiohttp
import discord
import asyncio
import io
import helpers

from tfm_class import tfm_client
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM

from env_class import env


# Discord bot class
class discord_client(discord.Client):
    tfm_bot = None

    def set_tfm_bot(self, bot):
        self.tfm_bot = bot

    busy = False  # to be used with transformice commands such as xml, roomlist, etc.

    def set_busy_status(self, value):
        self.busy = value

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Transformice (prefix ~)"))
        await self.get_channel(env.channels['debug']).send("Ready.")
        print("Discord connected.")
        await self.processRestarting()

    async def on_message(self, msg):
        author = msg.author
        if author.id == self.user.id:
            return

        args = msg.content.split(" ")
        cmd = args.pop(0).lower()

        # Compute author access
        author_access = env.PUBLIC

        cfmbot_role = discord.utils.find(lambda r: r.name == 'cfmbot', msg.guild.roles)
        if cfmbot_role in author.roles:
            author_access |= env.ADMIN

        """BEGIN DB COMMANDS"""
        if helpers.check_command(cmd, author_access, 'help'):
            await msg.reply(embed=helpers.generate_help(author_access))
        # DEPRECATED FOR NOW, if you know how to render a png from a svg easily, pr it :]
        # Uploads the svg instead.
        elif helpers.check_command(cmd, author_access, 'dressroom'):
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
        elif helpers.check_command(cmd, author_access, 'profile'):
            if len(args) < 1:
                await msg.reply("Provide a name or an id.")
                return

            profile = await helpers.request_profile(args[0])
            if profile:
                await msg.reply(embed=helpers.generate_profile(profile))
            else:
                await msg.reply('Could not retrieve player.')
                return
        elif helpers.check_command(cmd, author_access, 'tribe'):
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

            tribe_members = await helpers.request_tribe_members(str(tribe_id), "?limit=15")
            if not tribe_members:
                await msg.reply("Failed to retrieve members.")
                return

            await msg.reply(embed=helpers.generate_tribe(tribe, tribe_members))
        elif helpers.check_command(cmd, author_access, 'searchplayer'):
            if len(args) < 1:
                await msg.reply("Provide a name.")
                return

            search_result = await helpers.request_player_search(args[0])
            if search_result is None:
                await msg.reply("Failed searching.")
                return

            if len(search_result) == 0:
                await msg.reply("Couldn't find anybody.")
                return

            await msg.reply(embed=helpers.generate_search_result(search_result, "profile"))
        elif helpers.check_command(cmd, author_access, 'searchtribe'):
            if len(args) < 1:
                await msg.reply("Provide a name.")
                return

            search_result = await helpers.request_tribe_search(args[0])
            if search_result is None:
                await msg.reply("Failed searching.")
                return

            if len(search_result) == 0:
                await msg.reply("Couldn't find any tribe.")
                return

            await msg.reply(embed=helpers.generate_search_result(search_result, "tribe"))
        elif helpers.check_command(cmd, author_access, 'unbusy'):
            self.set_busy_status(False)
            return
        elif helpers.check_command(cmd, author_access, 'restart'):
            await self.restart_dyno()
            return
        elif helpers.check_command(cmd, author_access, 'restarttfm'):
            await self.tfm_bot.restart()
            return
        elif helpers.check_command(cmd, author_access, 'stop'):
            await self.stop_dyno()
            return
        """END DB COMMANDS"""

        """BEGIN TFM-BOT COMMANDS"""
        if helpers.check_command(cmd, author_access, 'isonline'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            if len(args) < 1:
                await msg.reply("Provide a name.")
                return

            self.set_busy_status(True)
            profile = await self.tfm_bot.get_profile(username=args[0])
            self.set_busy_status(False)
            if profile:
                args[0] = helpers.capitalize_name(profile.username)
                await msg.reply("`{}` is online!".format(args[0]))
            else:
                await msg.reply("`{}` is offline...".format(helpers.capitalize_name(args[0])))
            return
        elif helpers.check_command(cmd, author_access, 'roomlist'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            if len(args) < 2:
                await msg.reply(f"Provide a gamemode and a community.\nValid gamemodes are: "
                                f"{', '.join(env.gamemodes_list).lower()}.\nValid communities are: {', '.join(env.commu_list)}")
                return

            args[1] = args[1].lower()
            if args[0].upper() not in env.gamemodes_list or args[1] not in env.commu_list:
                await msg.reply(f"Provide a **valid** gamemode and a **valid** community.\nValid gamemodes are: "
                                f"{', '.join(env.gamemodes_list).lower()}.\nValid communities are: {', '.join(env.commu_list)}")
                return

            self.set_busy_status(True)
            roomlist = await self.tfm_bot.retrieve_roomlist(env.gamemodes_values[args[0].upper()], args[1])
            self.set_busy_status(False)

            await msg.reply(embed=helpers.generate_roomlist(roomlist, args[0], args[1]))
            return
        elif helpers.check_command(cmd, author_access, 'mod'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            result = await self.tfm_bot.retrieve_mods()
            await msg.reply(embed=helpers.generate_mod_list(result))
            return
        elif helpers.check_command(cmd, author_access, 'mapcrew'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            result = await self.tfm_bot.retrieve_mapcrew()
            await msg.reply(embed=helpers.generate_mapcrew_list(result))
            return
        elif helpers.check_command(cmd, author_access, 'xml'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            if len(args) < 1:
                await msg.reply("Specify a `@mapcode`.")
                return

            if args[0].find('@') == -1:
                args[0] = '@' + args[0]

            self.set_busy_status(True)
            await self.tfm_bot.request_xml()
            await self.tfm_bot.loadLua(env.get_xml.format(args[0]))
            await asyncio.sleep(1.5)
            xml = await self.tfm_bot.get_xml()
            await self.tfm_bot.sendCommand('module stop')
            self.set_busy_status(False)

            await msg.reply("Here you go! Triple-click to select the whole text.",
                            file=discord.File(filename=f"{args[0]}.txt", fp=io.BytesIO(xml.encode())))
            return
        elif helpers.check_command(cmd, author_access, 'rendermap'):
            if self.busy:
                await msg.reply("Bot is busy processing another request.")
                return

            if len(args) < 1:
                await msg.reply("Specify a `@mapcode`.")
                return

            if args[0].find('@') == -1:
                args[0] = '@' + args[0]

            self.set_busy_status(True)
            await self.tfm_bot.request_xml()
            await self.tfm_bot.loadLua(env.get_xml.format(args[0]))
            await asyncio.sleep(1.5)

            xml = await self.tfm_bot.get_xml()

            await self.tfm_bot.sendCommand('module stop')
            self.set_busy_status(False)

            image = await helpers.render_map(xml)

            if image is None or len(image) < 2000:
                await msg.reply("Failed to generate image...")
                return

            await msg.reply(file=discord.File(filename=f"{args[0]}.png", fp=io.BytesIO(image)))
            return

    async def restart_dyno(self):
        # The bot runs in a heroku dyno, we need to restart it.
        await self.get_channel(env.channels['debug']).send("Attempting to restart!")
        async with aiohttp.ClientSession() as session:
            await session.delete(
                "https://api.heroku.com/apps/tzukky/dynos/bot",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/vnd.heroku+json; version=3",
                    "Authorization": "Bearer " + env.heroku_api
                }
            )

    async def stop_dyno(self):
        # The bot runs in a heroku dyno, we need to stop it.
        await self.get_channel(env.channels['debug']).send("Closing application!")
        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://api.heroku.com/apps/tzukky/dynos/bot/actions/stop",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/vnd.heroku+json; version=3",
                    "Authorization": "Bearer " + env.heroku_api
                }
            )

    async def processRestarting(self):
        while True:
            await asyncio.sleep(7200)
            await self.restart_dyno()

    async def on_connection_error(self, conn):
        if conn.name == "main":
            await self.tfm_bot.restart()
        elif conn.name == "bulle":
            await self.tfm_bot.joinRoom(room_name="1")
            await asyncio.sleep(3.0)
            await self.tfm_bot.joinRoom(room_name="@#shobi")
