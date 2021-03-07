# JoyBot - Discord Bot
# Copyright (C) 2020 - 2021 Dylan Prins
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.

# You may contact me at admin@sinelservers.xyz

config = {
    # The things at the top is stuff you will most likely want to change, whereas the
    # things at the bottom are things that you'll probably want to keep the same.


    #--------Important things----------#

    # Environment variable where discord token is
    "TOKENVAR": "DISCORD_JOYBOT_TOKEN",

    # Prefix for the bot
    "PREFIX": ".",

    # The discord ids of all the super admins
    # The first id is considered the owner
    "SUPERADMINIDS": [
        246862123328733186  # Joyte
    ],

    # ID of the error guild | ID of the error channel | ID of the DM channel
    "ERRORDATA": (775532211763544114, 777407493495455744, 813405943689379872),

    #-----Less important things---------#

    # Number required, the aftertext and the name of the emoji. Prefix with ! to use discord emojis
    "BUMP_FUNNIES": {
        1: ("Babies' first bump", "!baby"),
        4: ("The lucky number!", "!four_leaf_clover"),
        10: ("Two digits!", "!keycap_ten"),
        12: ("Neat: Part 1", "!regional_indicator_n"),
        51: ("Aliens!", "!alien"),
        69: ("Nice.", "!underage"),
        96: ("Not nice.", "!double_vertical_bar"),
        100: ("Three digits!", "!100"),
        123: ("Neat: Part 2", "!regional_indicator_e"),
        180: ("Wo-ah, we're halfway there!", "badge_n180"),
        200: ("Bump OK.", "!ok"),
        360: ("All around!", "!yellow_circle"),
        404: ("Total not found", "!warning"),
        420: ("Blaze it 🌿", "!herb"),
        500: ("Now that's dedication.", "!clock2"),
        666: ("Devil's number", "!smiling_imp"),
        777: ("Luckier than number 4!", "!slot_machine"),
        1000: ("Four digits!", "!regional_indicator_a"),
        1234: ("1234!", "!1234"),
        9001: ("Over 9000!", "!rosette"),
        12345: ("Neat: The Finale", "!regional_indicator_t"),
    },

    # All the emojis and their corresponding IDS
    "EMOJI_IDS": {
        "badge_first_bump": 814419207118782475,
        "badge_1_place": 814419207080378379,
        "badge_2_place": 814419206879313961,
        "badge_3_place": 814419207012876289,

        "badge_n180": 814425080566251530
    },

    # Space goal, used for the help command
    # MUST BE BIGGER THAN HELP_NAME_LIMIT or your program will go in a infinite loop
    "SPACEGOAL": 30,

    # Limit for the name of the commands, also how many spaces to even out to
    "HELP_NAME_LIMIT": 24,

    # Characters for the polls
    # General cross, used in both
    "CHAR_CROSS": "❌",

    # General tick, used in guildban
    "CHAR_TICK": "✅",

    # Yes/No poll
    "CHAR_YES": "👍",
    "CHAR_NO": "👎",

    "numpoll": {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟"
    },

    # Colors for console
    "CONSOLECOLORS": {
        "RESET": "\033[0m",

        "BLACK": "\033[0;30m",
        "RED": "\033[0;31m",
        "GREEN": "\033[0;32m",
        "BROWN": "\033[0;33m",
        "BLUE": "\033[0;34m",
        "PURPLE": "\033[0;35m",
        "CYAN": "\033[0;36m",
        "GRAY": "\033[0;37m",

        "DARK_GRAY": "\033[1;30m",
        "LIGHT_RED": "\033[1;31m",
        "LIGHT_GREEN": "\033[1;32m",
        "YELLOW": "\033[1;33m",
        "LIGHT_BLUE": "\033[1;34m",
        "LIGHT_PURPLE": "\033[1;35m",
        "LIGHT_CYAN": "\033[1;36m",
        "WHITE": "\033[1;37m"
    },

    # Disboard ID, doesn't need to be changed
    "DISBOARDID": 302050872383242240,

    # Valid picture extensions, used for addface
    "PICEXT": [".png", ".jpg", ".jpeg", ".gif"],

    # The help command
    # "": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}
    # Example command:
    # {"command_name": {"flavor_text": "the flavor text", "format": "the way your command should be used (should be false if no arguments)", "long_text": "the text that appears when someone runs 'help command_name'", "extra_info": "Info to put at the bottom as a side note, should be 'False' if none",  "aliases": ["c_n", "(this list should be empty if no aliases", "name_command"]}
    #
    # "Others" is for adding your own categories, it's essentially the same except you name the group also, and put each command under a group. Should be None if none.
    # Template:
    #
    #  "OTHERS": {
    #		"CommandCategory": {
    #			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []},
    #			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}
    #		},
    #		"SecondCategory": {
    #			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}
    #		}
    #
    #	},

    "CMD_HELP": {

        # The character to use as a seperator
        "MID": "———",

        # Commands everyone can use.
        "EVERYONE": {
            "help": {"flavor_text": "This!", "format": "[command]", "long_text": "The command you're using now!", "extra_info": "When you see `<>` in an argument, it means the argument is required! If you see a `[]`, that means it's optional, and a `|` means or.", "aliases": []},
            "info": {"flavor_text": "Get some info", "format": False, "long_text": "Get some information about JoyBot and it's creator", "extra_info": False, "aliases": []},
            "privacy": {"flavor_text": "View the privacy policy", "format": False, "long_text": "View the privacy policy on JoyBot", "extra_info": False, "aliases": []},
            "invite": {"flavor_text": "JoyBot invite link", "format": False, "long_text": "Gives you the invite link, so you can use JoyBot in your own server", "extra_info": False, "aliases": []},
            "bumptotal": {"flavor_text": "Shows your bumptotal", "format": "[member]", "long_text": "Shows you the bumptotal of the guild you're in, either you or the supplied member", "extra_info": False, "aliases": []},
            "topbumptotal": {"flavor_text": "Shows the top bumpers", "format": False, "long_text": "Shows the top ten bumpers of the guild you're in", "extra_info": False, "aliases": []},
            "randompic": {"flavor_text": "Gets a random picture", "format": "<member | 'list'>", "long_text": "Gets a random picture from a member of your guild, pictures must be added by an admin!", "extra_info": "You can use `list` as an argument to get a list of members who have added a picture", "aliases": []},
            "hug": {"flavor_text": "Hug someone!", "format": "<member>", "long_text": "Hug someone, shows a related gif!", "extra_info": False, "aliases": []},
            "kiss": {"flavor_text": "Kiss someone!", "format": "<member>", "long_text": "Kiss someone, shows a related gif!", "extra_info": False, "aliases": []},
            "yesnopoll": {"flavor_text": "Makes a yes/no poll", "format": "<question>", "long_text": "Makes a yes/no poll", "extra_info": False, "aliases": ["yesnovote"]},
            "numberpoll": {"flavor_text": "Multiple choice poll", "format": "<args>", "long_text": "Makes a multiple choice poll, give it the values seperated by a comma. For example, to make a question with three answers, you should: `numberpoll question, answer one, answer two, answer three`.", "extra_info": "Limited to ten answers", "aliases": ["numbervote"]},
            "spacify": {"flavor_text": "Spacifies text", "format": "<message>", "long_text": "Sends the message back with a space inbetween every letter", "extra_info": False, "aliases": []},
            "convert": {"flavor_text": "Converts height values", "format": "<height>", "long_text": "Converts height values", "extra_info": "Works with feet'inches (6'2), centimetres (188), and metres (1.88)", "aliases": []},
            "reversecaps": {"flavor_text": "Reverses the caps", "format": "<message>", "long_text": "Sends the message back, with the caps reversed", "extra_info": False, "aliases": []},
            "backwords": {"flavor_text": "Sends the message backwords", "format": "<message>", "long_text": "Sends the message back, but backwords", "extra_info": False, "aliases": []}
        },

        # Set your own custom categories
        "OTHERS": None,

        # Only people with the Administrator permission and people authorized can use
        "ADMIN": {
            "addpic": {"flavor_text": "Adds a picture", "format": "<member>", "long_text": "Adds a picutre to a particular member's pictures list (for use with randompic)", "extra_info": False, "aliases": []},
            "delpic": {"flavor_text": "Removes a picture", "format": "<member> <picid>", "long_text": "Removes the picture of a particular member", "extra_info": False, "aliases": []}
        },

        # Only people with the Administrator permission can use
        "ADMINISTATOR": {
            "changesetting": {"flavor_text": "Change a setting", "format": "<depends on setting>", "long_text": "Change a particular setting", "extra_info": False, "aliases": []},
            "changebumptotal": {"flavor_text": "Changes bumptotal of a user", "format": "<member> <amount>", "long_text": "This command changes a user's bumptotal by a certain amount", "extra_info": False, "aliases": []},
            "resetbumptotal": {"flavor_text": "Resets the bumptotal of a user / everyone", "format": "<[member | 'server'>", "long_text": "This command will reset everyone's bump total, or just a user.", "extra_info": False, "aliases": []},
            "listsettings": {"flavor_text": "List settings", "format": False, "long_text": "List all the settings and their values", "extra_info": False, "aliases": []}
        },

        # Only people in the ADMINSIDS list can use
        "SUPERADMIN": {
            "cogload": {"flavor_text": "Load a cog", "format": "<cog>", "long_text": "Loads a cog into the discord bot", "extra_info": False, "aliases": []},
            "cogunload": {"flavor_text": "Unload a cog", "format": "<cog>", "long_text": "Unloads a cog from the discord bot", "extra_info": False, "aliases": []},
            "cogreload": {"flavor_text": "Reload a cog", "format": "<cog>", "long_text": "Reloads a cog already loaded into the bot", "extra_info": False, "aliases": []},
            "execute": {"flavor_text": "Runs python code", "format": "<raw python code>", "long_text": "Runs some python code, is admin only because this command is not sandboxed!", "extra_info": False, "aliases": ["e", "exec"]},
            "evaluate": {"flavor_text": "Evaluates python code", "format": "<raw python code>", "long_text": "Evaluates some python code, is admin only because this command is not sandboxed!", "extra_info": False, "aliases": ["eval"]},
            "guildban": {"flavor_text": "Ban a guild from JoyBot", "format": "<guild id>", "long_text": "Used to ban a guild from using JoyBot, purges their data.", "extra_info": False, "aliases": []}
        }

    }

}

# Default guild settings
config["DEFAULT_SETTINGS"] = {
    "admins_list": [],
    "global_randompic": False,
    "global_addpic": False,
    "prefix": config["PREFIX"]
}
