config = {
	# The things at the top is stuff you will most likely want to change, whereas the 
	# things at the bottom are things that you'll probably want to keep the same.


	#--------Important things----------#

	# Discord token to log in
	"TOKEN": "NTA0MDMwNzAzMjY0OTg5MTk0.W841LA.Am1bOYbxAqIdHX5tdSPijAOIXJc",

	# The ID of your bot
	"BOTID": 504030703264989194,

	# The permissions integer for your bot
	"PERMINT": 1878916311,

	# Prefix for the bot
	"PREFIX": ".",

	# Put your id here
	"BOTOWNER": 246862123328733186,

	# The discord ids of all the super admins
	"SUPERADMINIDS": [
		246862123328733186,  # Joyte
		202513952406503425,  # Blue
		253059354331316224   # Ben
	],

	# ID of the guild in which the error channel is
	"ERRORGUILD": 775532211763544114,

	# ID of the channel which errors shall be put
	"ERRORCHANNEL": 777407493495455744,

	#-----Less important things---------#
	
	# Aftertext and the number that someone must have in
	# order for the text to appear | format: (num, text)
	"BUMP_FUNNIES": [(69, "Nice."), (420, "Blaze it"), (9001, "Over 9000!")],

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

	# Number poll
	"CHAR_ONE": "1️⃣",
	"CHAR_TWO": "2️⃣",
	"CHAR_THREE": "3️⃣",
	"CHAR_FOUR": "4️⃣",
	"CHAR_FIVE": "5️⃣",
	"CHAR_SIX": "6️⃣",
	"CHAR_SEVEN": "7️⃣",
	"CHAR_EIGHT": "8️⃣",
	"CHAR_NINE": "9️⃣",
	"CHAR_TEN": "🔟",

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

	"ALLGIFS": ["hugs", "kisses", "marry"],

	# Disboard ID, doesn't need to be changed
	"DISBOARDID": 302050872383242240,

	"DEFAULT_SETTINGS": {"admins_list": [], "global_randomface": False, "global_addface": False, "counting_channel": None},

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
	#		"Command Category": {
	#			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []},
	#			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}
	#		},
	#		"Second category": {
	#			"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}
	#		}
	#
	#	},

	"CMD_HELP": {

		# The character to use as a seperator
		"MID": "———",

		# Commands everyone can use.
		"EVERYONE": {
			"help": {"flavor_text": "This!", "format": "[command]", "long_text": "The command you're using now!", "extra_info": "When you see <> in an argument, it means the argument is required! If you see a [], that means it's optional.", "aliases": []},
			"info": {"flavor_text": "Get some info", "format": False, "long_text": "Get some information about JoyBot and it's creator", "extra_info": False, "aliases": []},
			"invite": {"flavor_text": "JoyBot invite link", "format": False, "long_text": "Gives you the invite link, so you can use JoyBot in your own server", "extra_info": False, "aliases": []},
			"bumptotal": {"flavor_text": "Shows your bumptotal", "format": "[member]", "long_text": "Shows you the bumptotal of the guild you're in, either you or the supplied member", "extra_info": False, "aliases": []},
			"topbumptotal": {"flavor_text": "Shows the top bumpers", "format": False, "long_text": "Shows the top ten bumpers of the guild you're in", "extra_info": False, "aliases": []},
			"randomface": {"flavor_text": "Gets a random face", "format": "<member>", "long_text": "Gets a random face from a member of your guild, faces must be added by an admin!", "extra_info": "You can use `list` as an argument to get a list of members who have added a face", "aliases": []},
			"hug": {"flavor_text": "Hug someone!", "format": "<member>", "long_text": "Hug someone, shows a related gif!", "extra_info": False, "aliases": []},
			"kiss": {"flavor_text": "Kiss someone!", "format": "<member>", "long_text": "Kiss someone, shows a related gif!", "extra_info": False, "aliases": []},
			"spacify": {"flavor_text": "Spacifies text", "format": "<message>", "long_text": "Sends the message back with a space inbetween every letter", "extra_info": False, "aliases": []},
			"convert": {"flavor_text": "Converts height values", "format": "<height>", "long_text": "Converts height values", "extra_info": "Works with feet'inches (6'2), centimetres (188), and metres (1.88)", "aliases": []},
			"reversecaps": {"flavor_text": "Reverses the caps", "format": "<message>", "long_text": "Sends the message back, with the caps reversed", "extra_info": False, "aliases": []},
			"backwords": {"flavor_text": "Sends the message backwords", "format": "<message>", "long_text": "Sends the message back, but backwords", "extra_info": False, "aliases": []}
		},

		# Set your own custom categories
		"OTHERS": None,

		# Only people with the Administrator permission and people authorized can use
		"ADMIN": {
			"addface": {"flavor_text": "Adds a face", "format": "<member>", "long_text": "Adds a face to a particular member's faces list (for use with randomface)", "extra_info": False, "aliases": []},
			"delface": {"flavor_text": "Removes a face", "format": "<member> <faceid>", "long_text": "Removes the face of a particular member", "extra_info": False, "aliases": []}
		},

		# Only people with the Administrator permission can use
		"ADMINISTATOR": {
			"changesettings": {"flavor_text": "Change a setting", "format": "<depends on setting>", "long_text": "Change a particular setting", "extra_info": False, "aliases": []},
			"listsettings": {"flavor_text": "List settings", "format": False, "long_text": "List all the settings and their values", "extra_info": False, "aliases": []}
		},

		# Only people in the ADMINSIDS list can use
		"SUPERADMIN": {
			"load": {"flavor_text": "Load a cog", "format": "<cog>", "long_text": "Loads a cog into the discord bot", "extra_info": False, "aliases": []},
			"unload": {"flavor_text": "Unload a cog", "format": "<cog>", "long_text": "Unloads a cog from the discord bot", "extra_info": False, "aliases": []},
			"reload": {"flavor_text": "Reload a cog", "format": "<cog>", "long_text": "Reloads a cog already loaded into the bot", "extra_info": False, "aliases": []},
			"evaluate": {"flavor_text": "Runs python code", "format": "<raw python code>", "long_text": "Runs some python code, is admin only because this command is not sandboxed!", "extra_info": "A sandboxed version is being developed", "aliases": []},
			"changebumptotal": {"flavor_text": "Changes bumptotal of a user", "format": "<member> <amount>", "long_text": "This command changes a user's bumptotal by a certain amount", "extra_info": False, "aliases": []},
			"guildban": {"flavor_text": "Ban a guild from JoyBot", "format": "<guild id>", "long_text": "Used to ban a guild from using JoyBot, purges their data.", "extra_info": False, "aliases": []}
		}

	}

}
