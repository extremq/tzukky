import os


class env:
    discord_token = os.getenv('discord_token')
    cfm_site = os.getenv('cfm_site')
    command_prefix = "~"  # MUST not have any whitespace.

    ADMIN = 1
    PUBLIC = 2

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
        'search': {
            'name': command_prefix + "search",
            'desc': "Search for a player. Accepts `name` as parameter.",
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
        }
    }

    channels = {
        'debug': 832310385741660180
    }

