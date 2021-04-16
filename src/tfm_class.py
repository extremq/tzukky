import aiotfm
import asyncio

from env_class import env


class tfm_client(aiotfm.Client):
    async def on_login_ready(self, *a):
        print('Logging in ...')
        await self.login(username=env.tfm_user, password=env.tfm_pass,
                         encrypted=False, room=env.starting_room)

    async def on_ready(self):
        print(f'Connected to the community platform')

    async def get_profile(self, username, timeout=1):

        username = username.lower()

        def check(p):
            if '#' not in username:
                return p.username.split('#')[0].lower() == username
            return p.username.lower() == username

        try:
            await self.sendCommand('profile {}'.format(username))
            return await self.wait_for('on_profile', check, timeout=timeout)
        except asyncio.TimeoutError:
            return None
