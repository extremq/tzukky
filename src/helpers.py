import aiohttp
import discord

from env_class import env


def convert_name_for_get(name):
    if name.find('#') == -1:
        name = name + "%230000"
    else:
        name = name.replace("#", "%23")
    return name


async def request_profile(param):
    name = convert_name_for_get(name=param)
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "players/{}".format(name)) as resp:
            result = await resp.json()
    if resp.status == 200:
        return result
    else:
        return


async def request_mouse_outfit(param):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "dressroom/mouse/{}".format(param)) as resp:
            result = await resp.read()
    if resp.status == 200:
        return result
    else:
        return


async def request_tribe(param):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "tribes/{}".format(param)) as resp:
            result = await resp.read()
    if resp.status == 200:
        return result
    else:
        return


async def request_tribe_members(param, get):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "tribes/{}/members".format(param) + get) as resp:
            result = await resp.read()
    if resp.status == 200:
        return result
    else:
        return


def generate_tribe(tribe, tribe_members):
    shaman = tribe['stats']['shaman']
    defilante = tribe['stats']['shaman']
    survivor = tribe['stats']['shaman']
    racing = tribe['stats']['shaman']
    embed = discord.Embed(title=tribe['name'], url="https://atelier801.com/tribe?tr={}".format(tribe['id']))
    embed.set_thumbnail(url="http://logostribu.atelier801.com/879/1160879.jpg")
    embed.add_field(name="ID", value=str(tribe['id']), inline=True)
    embed.add_field(name="Total stats", value="", inline=False)
    embed.add_field(name="Shaman", value="{} / {} / {}".format(shaman['saves_normal'], shaman['saves_hard'], shaman['saves_divine']), inline=True)
    embed.add_field(name="Defilante", value="{} / {} / {}".format(defilante['rounds'], defilante['finished'], defilante['points']), inline=True)
    embed.add_field(name="Racing", value="{} / {} / {} / {}".format(racing['rounds'], racing['finished'], racing['first'], racing['podium']), inline=True)
    embed.add_field(name="Survior", value="{} / {} / {} / {}".format(survivor['rounds'], survivor['killed'], survivor['shaman'], survivor['survivor']), inline=True)
    embed.add_field(name="Members", value=str(tribe['members']), inline=False)
    member_list = ""
    for member in tribe_members:
        member_list += member['name'] + ', '
    member_list = member_list[:-2]
    embed.add_field(name=member_list, value="", inline=False)


def generate_profile(profile):
    sham = profile['stats']['shaman']
    racing = profile['stats']['racing']
    normal = profile['stats']['normal']
    survivor = profile['stats']['survivor']
    defilante = profile['stats']['defilante']
    embed = discord.Embed(title=profile['name'], url="https://atelier801.com/profile?pr=" + str(profile['id']))
    embed.set_thumbnail(url="http://avatars.atelier801.com/{}/{}.jpg".format(profile['id'] % 10000, profile['id']))
    embed.add_field(name="ID", value=str(profile['id']), inline=True)
    if profile['tfm_roles']:
        embed.add_field(name="Role", value=", ".join(profile["tfm_roles"]), inline=True)
    else:
        embed.add_field(name="Role", value="None.", inline=True)
    embed.add_field(name="Tribe", value=profile['tribe']['name'], inline=True)
    embed.add_field(name="Saves", value="{} / {} / {}".format(sham['saves_normal'], sham['saves_hard'], sham['saves_divine']), inline=True)
    embed.add_field(name="Shaman cheese", value=str(sham['cheese']), inline=True)
    embed.add_field(name="Rounds", value=str(normal['rounds']), inline=True)
    embed.add_field(name="Experience", value=str(sham['experience']), inline=True)
    embed.add_field(name="Level", value=str(level(sham['experience'])), inline=True)
    embed.add_field(name="Gathered cheese", value=str(normal['cheese']), inline=True)
    embed.add_field(name="Firsts", value=str(normal['first']), inline=True)
    embed.add_field(name="Bootcamp", value=str(normal['bootcamp']), inline=True)
    embed.add_field(name="Soulmate", value=profile['soulmate']['name'], inline=True)
    embed.add_field(name="Survivor", value="{} / {} / {} / {}".format(survivor['rounds'], survivor['killed'], survivor['shaman'], survivor['survivor']), inline=True)
    embed.add_field(name="Racing", value="{} / {} / {} / {}".format(racing['rounds'], racing['finished'], racing['first'], racing['podium']), inline=True)
    embed.add_field(name="Defilante", value="{} / {} / {}".format(defilante['rounds'], defilante['finished'], defilante['points']), inline=True)
    embed.add_field(name="Look", value=profile['shop']['look'], inline=True)
    return embed


def level(exp):
    total = 0
    for lvl in range(1000):
        total += formula(lvl)
        if total > exp:
            return lvl


def formula(n):
    if n < 30:
        return 32 + (n - 1) * (n + 2)
    elif n < 60:
        return 600 + 5 * (n - 29) * (n + 30)
    return 14250 + (15 * (n - 59) * (n + 60)) / 2
