import aiotfm
import asyncio
import re

from env_class import env


class tfm_client(aiotfm.Client):
    requested_xml = False
    xml = ""

    async def request_xml(self):
        xml = ""
        self.requested_xml = True

    async def get_xml(self):
        self.requested_xml = False
        return self.xml

    async def handle_packet(self, conn, packet):
        handled = await super().handle_packet(conn, packet.copy())

        if not handled:
            CCC = packet.readCode()
            if CCC == (28, 5):
                packet.read16()  # because tig
                msg = packet.readUTF()
                if msg.find('$Modo') == -1 and msg.find('$Mapcrew') == -1:
                    self.dispatch('mod_command', "Nobody is online. :'(")
                    return
                else:
                    matches = re.findall(r"(\[[a-z]{2,3}]|[+_A-Za-z#0-9]{4,})+", msg)
                    ret = ""
                    for match in matches:
                        if match == "MapcrewEnLigne" or match == "ModoEnLigne":
                            continue
                        if len(match) < 6:
                            ret = ret[:-2]
                            ret += '\n' + match + ' '
                        else:
                            ret += match + ', '
                    ret = ret[:-2]

                    if msg.find('$Modo') != -1:
                        self.dispatch('mod_command', ret)
                    else:
                        self.dispatch('mapcrew_command', ret)
                    return

    async def on_mod_command(self, msg):
        return msg

    async def on_mapcrew_command(self, msg):
        return msg

    async def on_login_ready(self, *a):
        print('Logging in ...')
        await self.login(username=env.tfm_user, password=env.tfm_pass,
                         encrypted=False, room=env.starting_room)

    async def on_ready(self):
        print(f'Connected to the community platform as {env.tfm_user}')

    async def get_profile(self, username, timeout=1):

        username = username.lower()

        def check(p):
            if '#' not in username:
                return p.username.split('#')[0].lower() == username
            return p.username.lower() == username

        try:
            await self.sendCommand(f'profile {username}')
            return await self.wait_for('on_profile', check, timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def retrieve_roomlist(self, gamemode, community):
        await self.sendCommand(f'commu {community}')
        return await self.getRoomList(gamemode)

    async def retrieve_mods(self, timeout=1):
        try:
            await self.sendCommand(f'mod')
            return await self.wait_for('on_mod_command', timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def retrieve_mapcrew(self, timeout=1):
        try:
            await self.sendCommand(f'mapcrew')
            return await self.wait_for('on_mapcrew_command', timeout=timeout)
        except asyncio.TimeoutError:
            return None

    async def on_lua_log(self, log):
        if self.requested_xml and log.find(env.tfm_user) == -1:
            self.xml += log[17:]
        else:
            self.xml = ""
