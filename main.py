# --------------------------JoyBot - Python Branch------------------------- #
# ---------------------------------License--------------------------------- #

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

# ---------------------------------Main------------------------------------ #
# ---------------------------------Intro----------------------------------- #

# JoyBot! A bot managed by Joyte#0001,
# filled with different features and random
# things that I wanted to add to my friends' servers.
# Enjoy using it! If you need to contact me, you
# can use my discord id up there, or look at my
# contact page: https://sinelservers.xyz/contact

# ---------------------------------Code------------------------------------ #

# All imports
import discord
import os
import sys
import re
from discord.ext import commands
from data.bot.bot_functions import return_all_faces_formatted, message_data_mod, gen_settings
from data.bot.bot_config import config

# Enable colors on windows
if os.name == "nt":
    os.system("color")

# ----------------------Generate structure-------------------- #

# Defaults
DEFAULTNONE = ""
DEFAULTGIF = "Put some .png files or .gif files into this folder, and they will be used when running the .kiss, .hug and .marry commands!"
DEFAULTFUNCTION = """# Functions file, put functions that you use in other files in here.\ndef add_string(string1, string2):\n\tprint(f"Adding strings '{string1}' and '{string2}'")\n\treturn string1 + string2"""
DEFAULTCONFIG = """config = {\n\t# The things at the top is stuff you will most likely want to change, whereas the \n\t# things at the bottom are things that you'll probably want to keep the same.\n\n\n\t#--------Important things----------#\n\n\t# Discord token to log in\n\t"TOKEN": "",\n\n\t# The ID of your bot\n\t"BOTID": 000000000000000000,\n\n\t# The permissions integer for your bot\n\t"PERMINT": 8,\n\n\t# Prefix for the bot\n\t"PREFIX": "!bot",\n\n\t# Put your id here\n\t"BOTOWNER": 000000000000000000,\n\n\t# The discord ids of all the super admins\n\t"SUPERADMINIDS": [\n\t\t000000000000000000,\n\t\t000000000000000000,\n\t\t000000000000000000\n\t],\n\n\t# ID of the channel which errors shall be put\n\t"ERRORLOG": 000000000000000000,\n\n\t#-----Less important things---------#\n\t\n\t# Aftertext and the number that someone must have in\n\t# order for the text to appear\n\t"BUMP_FUNNIES": [(69, "Nice."), (420, "Blaze it")],\n\n\t# Space goal, used for the help command\n\t# MUST BE BIGGER THAN HELP_NAME_LIMIT or your program will go in a infinite loop\n\t"SPACEGOAL": 30,\n\n\t# Limit for the name of the commands, also how many spaces to even out to\n\t"HELP_NAME_LIMIT": 24,\n\n\t# Characters for the polls\n\t# General cross, used in both\n\t"CHAR_CROSS": "❌",\n\n\t# General tick, used in guildban\n\t"CHAR_TICK": "✅",\n\n\t# Yes/No poll\n\t"CHAR_YES": "👍",\n\t"CHAR_NO": "👎",\n\n\t# Number poll\n\t"CHAR_ONE": "1️⃣",\n\t"CHAR_TWO": "2️⃣",\n\t"CHAR_THREE": "3️⃣",\n\t"CHAR_FOUR": "4️⃣",\n\t"CHAR_FIVE": "5️⃣",\n\t"CHAR_SIX": "6️⃣",\n\t"CHAR_SEVEN": "7️⃣",\n\t"CHAR_EIGHT": "8️⃣",\n\t"CHAR_NINE": "9️⃣",\n\t"CHAR_TEN": "🔟",\n\n\t"CONSOLECOLORS": {\n\t\t"RESET": "\\033[0m",\n\n\t\t"BLACK": "\\033[0;30m",\n\t\t"RED": "\\033[0;31m",\n\t\t"GREEN": "\\033[0;32m",\n\t\t"BROWN": "\\033[0;33m",\n\t\t"BLUE": "\\033[0;34m",\n\t\t"PURPLE": "\\033[0;35m",\n\t\t"CYAN": "\\033[0;36m",\n\t\t"GRAY": "\\033[0;37m",\n\n\t\t"DARK_GRAY": "\\033[1;30m",\n\t\t"LIGHT_RED": "\\033[1;31m",\n\t\t"LIGHT_GREEN": "\\033[1;32m",\n\t\t"YELLOW": "\\033[1;33m",\n\t\t"LIGHT_BLUE": "\\033[1;34m",\n\t\t"LIGHT_PURPLE": "\\033[1;35m",\n\t\t"LIGHT_CYAN": "\\033[1;36m",\n\t\t"WHITE": "\\033[1;37m"\n\t},\n\n\t"ALLGIFS": ["hugs", "kisses", "marry"],\n\n\t# Disboard ID, doesn't need to be changed\n\t"DISBOARDID": 302050872383242240,\n\n\t# Valid picture extensions, used for addface\n\t"PICEXT": [".png", ".jpg", ".jpeg", ".gif"],\n\n\t# The help command\n\t# "": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}\n\t# Example command:\n\t# {"command_name": {"flavor_text": "the flavor text", "format": "the way your command should be used (should be false if no arguments)", "long_text": "the text that appears when someone runs 'help command_name'", "extra_info": "Info to put at the bottom as a side note, should be 'False' if none",  "aliases": ["c_n", "(this list should be empty if no aliases", "name_command"]}\n\t#\n\t# "Others" is for adding your own categories, it's essentially the same except you name the group also, and put each command under a group. Should be None if none.\n\t# Template:\n\t#\n\t#  "OTHERS": {\n\t#\t\t"Command Category": {\n\t#\t\t\t"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []},\n\t#\t\t\t"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}\n\t#\t\t},\n\t#\t\t"Second category": {\n\t#\t\t\t"": {"flavor_text": "", "format": False, "long_text": "", "extra_info": False, "aliases": []}\n\t#\t\t}\n\t#\n\t#\t},\n\n\t"CMD_HELP": {\n\n\t\t# The character to use as a seperator\n\t\t"MID": "———",\n\n\t\t# Commands everyone can use.\n\t\t"EVERYONE": {\n\t\t\t"help": {"flavor_text": "This!", "format": "[command]", "long_text": "The command you're using now!", "extra_info": "When you see <> in an argument, it means the argument is required! If you see a [], that means it's optional.", "aliases": []},\n\t\t\t"invite": {"flavor_text": "JoyBot invite link", "format": False, "long_text": "Gives you the invite link, so you can use JoyBot in your own server", "extra_info": False, "aliases": []},\n\t\t\t"bumptotal": {"flavor_text": "Shows your bumptotal", "format": "[member]", "long_text": "Shows you the bumptotal of the guild you're in, either you or the supplied member", "extra_info": False, "aliases": []},\n\t\t\t"topbumptotal": {"flavor_text": "Shows the top bumpers", "format": False, "long_text": "Shows the top ten bumpers of the guild you're in", "extra_info": False, "aliases": []},\n\t\t\t"randomface": {"flavor_text": "Gets a random face", "format": "<member>", "long_text": "Gets a random face from a member of your guild, faces must be added by an admin!", "extra_info": "You can use `list` as an argument to get a list of members who have added a face", "aliases": []},\n\t\t\t"hug": {"flavor_text": "Hug someone!", "format": "<member>", "long_text": "Hug someone, shows a related gif!", "extra_info": False, "aliases": []},\n\t\t\t"kiss": {"flavor_text": "Kiss someone!", "format": "<member>", "long_text": "Kiss someone, shows a related gif!", "extra_info": False, "aliases": []},\n\t\t\t"spacify": {"flavor_text": "Spacifies text", "format": "<message>", "long_text": "Sends the message back with a space inbetween every letter", "extra_info": False, "aliases": []},\n\t\t\t"convert": {"flavor_text": "Converts height values", "format": "<height>", "long_text": "Converts height values", "extra_info": "Works with feet'inches (6'2), centimetres (188), and metres (1.88)", "aliases": []},\n\t\t\t"reversecaps": {"flavor_text": "Reverses the caps", "format": "<message>", "long_text": "Sends the message back, with the caps reversed", "extra_info": False, "aliases": []},\n\t\t\t"backwords": {"flavor_text": "Sends the message backwords", "format": "<message>", "long_text": "Sends the message back, but backwords", "extra_info": False, "aliases": []}\n\t\t},\n\n\t\t# Set your own custom categories\n\t\t"OTHERS": None,\n\n\t\t# Only people with the Administrator permission can use\n\t\t"ADMIN": {\n\t\t\t"addface": {"flavor_text": "Adds a face", "format": "<member>", "long_text": "Adds a face to a particular member's faces list (for use with randomface)", "extra_info": False, "aliases": []},\n\t\t\t"delface": {"flavor_text": "Removes a face", "format": "<member> <faceid>", "long_text": "Removes the face of a particular member", "extra_info": False, "aliases": []}\n\t\t},\n\n\t\t# Only people in the ADMINSIDS list can use\n\t\t"SUPERADMIN": {\n\t\t\t"load": {"flavor_text": "Load a cog", "format": "<cog>", "long_text": "Loads a cog into the discord bot", "extra_info": False, "aliases": []},\n\t\t\t"unload": {"flavor_text": "Unload a cog", "format": "<cog>", "long_text": "Unloads a cog from the discord bot", "extra_info": False, "aliases": []},\n\t\t\t"reload": {"flavor_text": "Reload a cog", "format": "<cog>", "long_text": "Reloads a cog already loaded into the bot", "extra_info": False, "aliases": []},\n\t\t\t"evaluate": {"flavor_text": "Runs python code", "format": "<raw python code>", "long_text": "Runs some python code, is admin only because this command is not sandboxed!", "extra_info": "A sandboxed version is being developed", "aliases": []},\n\t\t\t"changebumptotal": {"flavor_text": "Changes bumptotal of a user", "format": "<member> <amount>", "long_text": "This command changes a user's bumptotal by a certain amount", "extra_info": False, "aliases": []},\n\t\t\t"guildban": {"flavor_text": "Ban a guild from JoyBot", "format": "<guild id>", "long_text": "Used to ban a guild from using JoyBot, purges their data.", "extra_info": False, "aliases": []}\n\t\t}\n\n\t}\n\n}\n"""
DEFAULTCOG = """#Examplecog\n\nclass Example(commands.Cog):\n\tdef __init__(self, client):\n\t\tself.client = client\n\n\t@commands.command()\n\tasync def nothing(self, ctx):\n\t\tawait ctx.send("Okay, i did nothing!")\n\n\ndef setup(client):\n\tclient.add_cog(Example(client))\n"""

TEMP_COLORS = {"YELLOW": "\033[1;33m", "RESET": "\033[0m"}

# Directory structure
# (Path, Type, Default value, required, required conditions (path that generated before))
STRUCTURE = [
    ("./cogs", "folder", DEFAULTNONE, True),
    ("./cogs/defaultcog.py", "file", DEFAULTCOG, False, "./cogs"),
    ("./data", "folder", DEFAULTNONE, True),
    ("./data/backups", "folder", DEFAULTNONE, True),
    ("./data/bot", "folder", DEFAULTNONE, True),
    ("./data/bot/pics", "folder", DEFAULTNONE, True),
    ("./data/bot/pics/hugs", "folder", DEFAULTNONE, True),
    ("./data/bot/pics/hugs/readme.txt", "file", DEFAULTGIF, False, "./data/bot/pics/hugs"),
    ("./data/bot/pics/marry", "folder", DEFAULTNONE, True),
    ("./data/bot/pics/marry/readme.txt", "file", DEFAULTGIF, False, "./data/bot/pics/marry"),
    ("./data/bot/pics/kisses", "folder", DEFAULTNONE, True),
    ("./data/bot/pics/kisses/readme.txt", "file", DEFAULTGIF, False, "./data/bot/pics/kisses"),
    ("./data/bot/bot_functions.py", "file", DEFAULTFUNCTION, True),
    ("./data/bot/bot_config.py", "file", DEFAULTCONFIG, True)
]

generated_list = []
for filetype in STRUCTURE:
    if not os.path.exists(filetype[0]):

        if filetype[1] == "folder":
            os.mkdir(filetype[0])

        elif filetype[1] == "file":
            if filetype[3]:
                with open(filetype[0], "w", encoding="utf-8") as fp:
                    fp.write(filetype[2])

            elif filetype[4] in generated_list:
                with open(filetype[0], "w", encoding="utf-8") as fp:
                    fp.write(filetype[2])
            else:
                continue

        generated_list.append(filetype[0])
        print(f"{TEMP_COLORS['YELLOW']}Made the {filetype[1]} {filetype[0]}{TEMP_COLORS['RESET']}")

del DEFAULTNONE, DEFAULTGIF, DEFAULTCONFIG, DEFAULTFUNCTION, DEFAULTCOG, STRUCTURE, TEMP_COLORS, generated_list

# -----------------------Set up Variables--------------------- #

# Set up the bot object
client = commands.Bot(command_prefix=config['PREFIX'])
client.msg_data = {}

# Remove the help command, as we have our own custom one
client.remove_command("help")


# --------------------------------Events-------------------------------- #

# Triggers on any command
# Stops the error from appearing if it's any command not found error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Please use all required arguments!")
        return
    elif "403" in str(error):
        try:
            await ctx.send(f"Looks like i'm missing a permission, make sure you invited me with the right permissions integer and selected all the parts!\nIf you think you removed some permissions, you can re-invite me by running the `{config['PREFIX']}invite` command.\n(make sure to kick me before you re-invite me!)")
        except discord.errors.Forbidden:
            pass
        return

    elif isinstance(error, commands.errors.MemberNotFound):
        if ctx.message.content == f"{config['PREFIX']}randomface list":
            try:
                _ = client.facesDict[str(ctx.guild.id)]
                del _
            except KeyError:
                await ctx.send("This guild doesn't have any faces, ask an admin to add some!")
                return

            msg = await ctx.send("Getting faces list...")
            await msg.edit(content=await return_all_faces_formatted(client, ctx))
            return

        await ctx.send("That's not a valid member!")
        return

    guild = client.get_guild(config["ERRORGUILD"])
    channel = guild.get_channel(config["ERRORCHANNEL"])
    await channel.send(f"Hey <@{config['BOTOWNER']}>, there was an error!\n```\n{error}\n```")
    raise error


@client.event
async def on_guild_join(guild):
    print(f"Joined the guild '{guild.name}'")
    await gen_settings(guild.id)


@client.event
async def on_message(message):
    if message.content == f"<@!{config['BOTID']}>":
        if message.author.id != config["BOTID"]:
            await message.channel.send(f"My prefix is `{config['PREFIX']}`!\nType `{config['PREFIX']}help` to get a list of commands!\nType `{config['PREFIX']}info` to get some info about me and my creator!")
    await client.process_commands(message)


# Updates the presence and prints to console we've connected
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Just JoyBot things :)"))
    print(f"Logged in as the bot ({client.user})!")


# --------------------------Cog management------------------------------- #

# Load cogs on program start
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# Load a cog
@client.command()
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send(f"Please specify a cog!")
        return

    try:
        client.load_extension(f"cogs.{extension}")

    except discord.ext.commands.errors.ExtensionNotFound:
        await ctx.send(f"Could not find the cog '{extension}'!")
        return

    except discord.ext.commands.errors.ExtensionAlreadyLoaded:
        await ctx.send(f"The cog '{extension}' is already loaded!")
        return

    except discord.ext.commands.errors.MissingAnyRole:
        await ctx.send("You can't use this command!")
        return

    await ctx.send(f"The cog '{extension}' has been loaded!")


@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.errors.ExtensionFailed):
        await ctx.send(f"An error occured while loading this extension!\n`{error}`")


# Unload a cog
@client.command()
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send(f"Please specify a cog!")
        return
    try:
        client.unload_extension(f"cogs.{extension}")
    except commands.errors.ExtensionNotLoaded:
        await ctx.send(f"The cog '{extension}' has not been loaded!")
        return
    await ctx.send(f"The cog '{extension}' has been unloaded!")


# Reload a cog
@client.command()
async def reload(ctx, extension=None):
    if extension is None:
        await ctx.send(f"Please specify a cog!")
        return

    try:
        client.reload_extension(f"cogs.{extension}")

    except commands.errors.ExtensionNotLoaded:
        await ctx.send(f"The cog '{extension}' has not been loaded!")
        return

    await ctx.send(f"The cog '{extension}' has been reloaded!")


@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.errors.ExtensionFailed):
        await ctx.send(f"An error occoured while loading this extension!\n`{error}`")


# ------------------------------------Main function------------------------------------- #

def main():
    print("Logging into discord...")
    try:
        client.run(config["TOKEN"])

    except discord.errors.LoginFailure:
        print(
            f"{config['CONSOLECOLORS']['RED']}The provided token was invalid, please supply a valid one in './data/bot/config.json'!{config['CONSOLECOLORS']['RESET']}")
        input("\nPress the enter key to exit...")
        sys.exit()


if __name__ == '__main__':
    main()
