import os

from aiotfm import enums

class env:
    discord_token = os.getenv('discord_token')
    cfm_site = os.getenv('cfm_site')
    tfm_user = "Extremq2#0000"
    tfm_pass = os.getenv('tfm_pass')
    tfm_id = 11760142
    tfm_token = os.getenv('tfm_token')
    heroku_api = os.getenv('heroku_api')
    starting_room = "@#shobi"
    get_xml = """xml=''function eventNewGame()xml=tfm.get.room.xmlMapInfo.xml;printXML()end;function printXML()local a=math.ceil(xml:len()/2000)for b=0,math.ceil(xml:len()/2000)-1 do print(xml:sub(xml:len()*b/a+1,xml:len()*(b+1)/a))end end;tfm.exec.newGame("{}")"""

    command_prefix = "~"  # MUST not have any whitespace.

    ADMIN = 1
    PUBLIC = 2

    commu_list = [
        'en',
        'int',
        'xx',
        'fr',
        'ru',
        'br',
        'es',
        'cn',
        'tr',
        'vk',
        'pl',
        'hu',
        'nl',
        'ro',
        'id',
        'de',
        'e2',
        'ar',
        'ph',
        'lt',
        'jp',
        'fi',
        'cz',
        'hr',
        'bg',
        'lv',
        'he',
        'it',
        'et',
        'pt',
    ]

    gamemodes_list = [
        'NORMAL',
        'BOOTCAMP',
        'VANILLA',
        'SURVIVOR',
        'RACING',
        'DEFILANTE',
        'VILLAGE',
        'MODULES',
    ]

    gamemodes_values = {
        'NORMAL': enums.GameMode.NORMAL,
        'BOOTCAMP': enums.GameMode.BOOTCAMP,
        'VANILLA': enums.GameMode.VANILLA,
        'SURVIVOR': enums.GameMode.SURVIVOR,
        'RACING': enums.GameMode.RACING,
        'DEFILANTE': enums.GameMode.DEFILENTE,  # !!!!
        'VILLAGE': enums.GameMode.VILLAGE,
        'MODULES': enums.GameMode.MODULES,
    }

    commands = {
        'tribe': {
            'name': command_prefix + "tribe",
            'desc': "Get information about a tribe. Accepts `name` or `tribe_id` as parameters.",
            'access': PUBLIC
        },
        'profile': {
            'name': command_prefix + "profile",
            'desc': "Get information about a player. Accepts `name` or `player_id` as parameters.",
            'access': PUBLIC
        },
        'searchplayer': {
            'name': command_prefix + "searchplayer",
            'desc': "Search for a player. Accepts `name` as parameter.",
            'access': PUBLIC
        },
        'searchtribe': {
            'name': command_prefix + "searchtribe",
            'desc': "Search for a tribe. Accepts `name` as parameter.",
            'access': PUBLIC
        },
        'dressroom': {
            'name': command_prefix + "dressroom",
            'desc': "Generate a mouse look. Accepts `name` or `outfit` as parameters.",
            'access': PUBLIC
        },
        'help': {
            'name': command_prefix + "help",
            'desc': "Displays available commands.",
            'access': PUBLIC
        },
        'restart': {
            'name': command_prefix + "restart",
            'desc': "Restarts the dyno.",
            'access': ADMIN
        },
        'isonline': {
            'name': command_prefix + "isonline",
            'desc': "Check if an user is online. Accepts `name` as parameter.",
            'access': PUBLIC
        },
        'roomlist': {
            'name': command_prefix + "roomlist",
            'desc': "Retrieves a gamemode's roomlist on a community. Requires `gamemode` and `community` as parameter.",
            'access': PUBLIC
        },
        'unbusy': {
            'name': command_prefix + "unbusy",
            'desc': "Makes bot not busy.",
            'access': ADMIN
        },
        'mod': {
            'name': command_prefix + "mod",
            'desc': "Shows connected mod list.",
            'access': PUBLIC
        },
        'mapcrew': {
            'name': command_prefix + "mapcrew",
            'desc': "Shows connected mapcrew list.",
            'access': PUBLIC
        },
        'xml': {
            'name': command_prefix + "xml",
            'desc': "Get the xml of a map. Needs a mapcode.",
            'access': PUBLIC
        },
        'rendermap': {
            'name': command_prefix + "rendermap",
            'desc': "Renders a map. Needs a mapcode.",
            'access': PUBLIC
        }
    }

    channels = {
        'debug': 832310385741660180
    }

