# --------------------------JoyBot - Python Branch-------------------------#
# ----------------------------------Help-----------------------------------#

import json
import os

from discord.ext import commands
from data.bot.bot_functions import text_pretty_mid_end, guild_settings, determine_prefix
from data.bot.bot_config import config


# ---------------------------------Code------------------------------------#

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        for guildid in os.listdir("./data"):
            try:
                with open(f"./data/{guildid}/faces.json", 'r') as fp:
                    client.facesDict[guildid] = json.load(fp)
            except FileNotFoundError:
                continue

    # Custom help command
    @commands.command()
    async def help(self, ctx, req_cmd=None):
        sendstring = "```\n"
        try:

            if req_cmd is None:
                # Add the everyone can use commands
                sendstring += "Everyone:\n"
                for command in config["CMD_HELP"]["EVERYONE"]:
                    command_name = command
                    command = config["CMD_HELP"]["EVERYONE"][command]
                    sendstring += f"\t{await text_pretty_mid_end(command_name, command['flavor_text'])}\n"

                if config["CMD_HELP"]["OTHERS"] is not None:
                    for command_cat in config["CMD_HELP"]["OTHERS"]:
                        sendstring += f"\n{command_cat}:\n"
                        for command in config["CMD_HELP"]["OTHERS"][command_cat]:
                            command_name = command
                            command = config["CMD_HELP"]["OTHERS"][command_cat][command_name]
                            sendstring += f"\t{await text_pretty_mid_end(command_name, command['flavor_text'])}\n"

                # Add the administrator only commands
                if ctx.author.guild_permissions.administrator or ctx.author.id in config["SUPERADMINIDS"] or ctx.author.id in await guild_settings(ctx.guild.id, "adminslist"):
                    sendstring += "\nAdmins:\n"
                    for command in config["CMD_HELP"]["ADMIN"]:
                        command_name = command
                        command = config["CMD_HELP"]["ADMIN"][command]
                        sendstring += f"\t{await text_pretty_mid_end(command_name, command['flavor_text'])}\n"

                if ctx.author.guild_permissions.administrator or ctx.author.id in config["SUPERADMINIDS"]:
                    sendstring += "\nAdministrators:\n"
                    for command in config["CMD_HELP"]["ADMINISTATOR"]:
                        command_name = command
                        command = config["CMD_HELP"]["ADMINISTATOR"][command]
                        sendstring += f"\t{await text_pretty_mid_end(command_name, command['flavor_text'])}\n"

                # Add the superadmin only commands
                if ctx.author.id in config["SUPERADMINIDS"]:
                    sendstring += "\nSuperadmins:\n"
                    for command in config["CMD_HELP"]["SUPERADMIN"]:
                        command_name = command
                        command = config["CMD_HELP"]["SUPERADMIN"][command]
                        sendstring += f"\t{await text_pretty_mid_end(command_name, command['flavor_text'])}\n"

                sendstring += f"\nYou can run '{await determine_prefix(self.client, ctx, 'r')}help <command>' to get a more in-depth explanation of a command!\nExample: '{await determine_prefix(self.client, ctx, 'r')}help help'\n"

            else:
                if config["CMD_HELP"]["OTHERS"] is not None:
                    cats = list(config["CMD_HELP"]["OTHERS"].keys())
                    other_cat = []
                    other_cmds = []

                    for cat in cats:
                        for cmd in config["CMD_HELP"]["OTHERS"][cat]:
                            if req_cmd == cmd:
                                other_cat = cat
                            other_cmds.append(cmd)
                else:
                    other_cmds = []
                    other_cat = ""

                if req_cmd in list(config["CMD_HELP"]["EVERYONE"].keys()):
                    group = "EVERYONE"
                elif req_cmd in other_cmds:
                    group = "OTHERS"
                elif req_cmd in list(config["CMD_HELP"]["ADMIN"].keys()):
                    group = "ADMIN"
                elif req_cmd in list(config["CMD_HELP"]["ADMINISTATOR"].keys()):
                    group = "ADMINISTATOR"
                elif req_cmd in list(config["CMD_HELP"]["SUPERADMIN"].keys()):
                    group = "SUPERADMIN"
                else:
                    await ctx.send(
                        f"That isn't a valid command, type `{await determine_prefix(self.client, ctx, 'r')}help` to get a list of all the commands!")
                    return

                if group != "OTHERS":
                    command = config["CMD_HELP"][group][req_cmd]
                else:

                    command = config["CMD_HELP"][group][other_cat][req_cmd]

                sendstring += f"{req_cmd}:\n\t{command['long_text']}\n\n"

                if command['format']:
                    cmd_format = command['format']
                else:
                    cmd_format = ""

                sendstring += f"\tUsage: {await determine_prefix(self.client, ctx, 'r')}{req_cmd}  {cmd_format}\n"

                if command['aliases']:
                    aliaseslist = ""
                    for alias in command['aliases']:
                        aliaseslist += f"'{await determine_prefix(self.client, ctx, 'r')}{alias}', "
                    sendstring += f"\tAliases: {aliaseslist[:-2]}\n"

                if command['extra_info']:
                    sendstring += f"\tExtra info: {command['extra_info']}\n"

        except KeyError as e:
            await ctx.send("There's an error with the help command, contact the dev!")
            raise e

        await ctx.send(f"{sendstring[:-1]}```")


def setup(client):
    client.add_cog(Help(client))
