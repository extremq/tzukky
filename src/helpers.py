import math

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
            result = await resp.json()
    if resp.status == 200:
        return result
    else:
        return


async def request_tribe_members(param, get):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "tribes/{}/members".format(param) + get) as resp:
            result = await resp.json()
    if resp.status == 200:
        return result
    else:
        return


async def request_player_search(param):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "players?search={}&limit=60".format(param)) as resp:
            result = await resp.json()
    if resp.status == 200:
        return result
    else:
        return


async def request_tribe_search(param):
    async with aiohttp.ClientSession() as session:
        async with session.get(env.cfm_site + "tribes?search={}&limit=60".format(param)) as resp:
            result = await resp.json()
    if resp.status == 200:
        return result
    else:
        return


def generate_search_result(search_result, _type):
    if _type == "profile":
        url = "https://atelier801.com/profile?pr={}"
    else:
        url = "https://atelier801.com/tribe?tr={}"

    search_list = ['', '', '', '', '', '']

    count = 0
    column = math.ceil(len(search_result) / len(search_list))
    for result in search_result:
        search_list[count // column] += '[{}]({})\n'.format(" ".join(result['name'].splitlines()), url.format(result['id']))
        count += 1

    embed = discord.Embed(title="Search result", description="Showing the first {} {}(s).".format(len(search_result), _type))

    for i in range(len(search_list)):
        if search_list[i] != '':
            embed.add_field(name="Column {}".format(i + 1), value=search_list[i], inline=True)
    return embed


def generate_tribe(tribe, tribe_members):
    url = "https://atelier801.com/profile?pr={}"

    shaman = tribe['stats']['total']['shaman']
    defilante = tribe['stats']['total']['defilante']
    survivor = tribe['stats']['total']['survivor']
    racing = tribe['stats']['total']['racing']
    normal = tribe['stats']['total']['normal']

    embed = discord.Embed(title=tribe['name'], url="https://atelier801.com/tribe?tr={}".format(tribe['id']))
    embed.set_thumbnail(url="http://logostribu.atelier801.com/{}/{}.jpg".format(tribe['id'] % 10000, tribe['id']))
    embed.add_field(name="ID", value=str(tribe['id']), inline=True)
    embed.add_field(name="Total stats", value="for this tribe", inline=False)
    embed.add_field(name="Rounds", value=normal['rounds'], inline=True)
    embed.add_field(name="Firsts", value=normal['first'], inline=True)
    embed.add_field(name="Cheese gathered", value=normal['cheese'], inline=True)
    embed.add_field(name="Bootcamp", value=normal['bootcamp'], inline=True)
    embed.add_field(name="Shaman", value="{} / {} / {}".format(shaman['saves_normal'], shaman['saves_hard'], shaman['saves_divine']), inline=True)
    embed.add_field(name="Defilante", value="{} / {} / {}".format(defilante['rounds'], defilante['finished'], defilante['points']), inline=True)
    embed.add_field(name="Racing", value="{} / {} / {} / {}".format(racing['rounds'], racing['finished'], racing['first'], racing['podium']), inline=True)
    embed.add_field(name="Survior", value="{} / {} / {} / {}".format(survivor['rounds'], survivor['killed'], survivor['shaman'], survivor['survivor']), inline=True)
    embed.add_field(name="Members", value=str(tribe['members']), inline=False)

    member_list = ""
    count = 0
    for member in tribe_members:
        count += 1
        if count > 15:
            break
        member_list += '[{}]({}), '.format(member['name'], url.format(member['id']))
    member_list = member_list[:-2]

    embed.add_field(name="Member list (15 max)", value=member_list, inline=False)
    return embed


def generate_profile(profile):
    tribe_url = "https://atelier801.com/tribe?tr={}"
    profile_url = "https://atelier801.com/profile?pr={}"
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
    if profile['tribe']:
        embed.add_field(name="Tribe", value="[{}]({})".format(" ".join(profile['tribe']['name'].splitlines()),
                                                              tribe_url.format(profile['tribe']['id'])), inline=True)
    else:
        embed.add_field(name="Tribe", value="None.", inline=True)
    embed.add_field(name="Saves", value="{} / {} / {}".format(sham['saves_normal'], sham['saves_hard'],
                                                              sham['saves_divine']), inline=True)
    embed.add_field(name="Shaman cheese", value=str(sham['cheese']), inline=True)
    embed.add_field(name="Rounds", value=str(normal['rounds']), inline=True)
    embed.add_field(name="Experience", value=str(sham['experience']), inline=True)
    embed.add_field(name="Level", value=str(level(sham['experience'])), inline=True)
    embed.add_field(name="Gathered cheese", value=str(normal['cheese']), inline=True)
    embed.add_field(name="Firsts", value=str(normal['first']), inline=True)
    embed.add_field(name="Bootcamp", value=str(normal['bootcamp']), inline=True)
    if profile['soulmate']:
        embed.add_field(name="Soulmate", value="[{}]({})".format(profile['soulmate']['name'],
                                                                 profile_url.format(profile['soulmate']['id'])), inline=True)
    else:
        embed.add_field(name="Soulmate", value="None.", inline=True)
    embed.add_field(name="Survivor", value="{} / {} / {} / {}".format(survivor['rounds'], survivor['killed'], survivor['shaman'], survivor['survivor']), inline=True)
    embed.add_field(name="Racing", value="{} / {} / {} / {}".format(racing['rounds'], racing['finished'], racing['first'], racing['podium']), inline=True)
    embed.add_field(name="Defilante", value="{} / {} / {}".format(defilante['rounds'], defilante['finished'], defilante['points']), inline=True)
    embed.add_field(name="Look", value=profile['shop']['look'], inline=True)
    return embed


def generate_help(author_access):
    embed = discord.Embed(title="Commands")
    for key in env.commands:
        if author_access & env.commands[key]['access']:
            embed.add_field(name=key, value=env.commands[key]['desc'], inline=True)
    return embed


def generate_roomlist(roomlist, gamemode, commu):
    embed = discord.Embed(title=f"{capitalize_name(gamemode)} rooms in `{commu}`")
    for room in roomlist.rooms:
        if commu != "int" and room.name[0] == "*":
            continue
        playerword = "players"
        if room.player_count == 1:
            playerword = "player"
        embed.add_field(name=room.name, value=str(room.player_count) + " " + playerword, inline=True)
    return embed


def generate_mod_list(msg):
    embed = discord.Embed(title="Online moderators", description=msg)
    return embed


def generate_mapcrew_list(msg):
    embed = discord.Embed(title="Online mapcrews", description=msg)
    return embed


def capitalize_name(name):
    if name[0] == '+':
        return '+' + name[1].upper() + name[2:].lower()
    else:
        return name[0].upper() + name[1:].lower()


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


def check_command(cmd, author_access, name):
    return cmd == env.commands[name]['name'] and env.commands[name]['access'] & author_access
