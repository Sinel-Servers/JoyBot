# --------------------------JoyBot - Python Branch-------------------------#

import json
import os
import random
import re
from decimal import Decimal
from operator import itemgetter
import discord

from data.bot.bot_config import config


# --------------------------------Functions--------------------------------#


async def random_gif(whichGifs):
    if whichGifs in config["ALLGIFS"]:
        choice = random.choice(os.listdir(f"./data/bot/pics/{whichGifs}/"))
        return f"{whichGifs}/{choice}"
    else:
        return False


async def inch_cm(convert):
    # CM
    try:
        if convert.isnumeric():
            inches = int(convert) / 2.54
            feet = 0
            while inches >= 13:
                feet += 1
                inches -= 12
            return str(feet) + "'" + str(round(inches))

        # Inches
        else:
            if "'" in convert:
                split = convert.split("'")
                if split[0].isnumeric():
                    if split[1].isnumeric():
                        inches = int(split[0]) * 12
                        inches += int(split[1])
                        cm = inches * 2.54
                        return str(round(cm)) + "cm"
                    else:
                        return False
                else:
                    return False
            # Meters
            elif "." in convert:
                split = convert.split(".")
                if split[0].isnumeric():
                    if split[1].isnumeric():
                        return str(round(Decimal(convert) * 100)) + "cm"
                    else:
                        return False
                else:
                    return False

            else:
                return False

    # CM again but the provided argument was a number
    except AttributeError:
        inches = int(convert) / 2.54
        feet = 0
        while inches >= 13:
            feet += 1
            inches -= 12
        return str(feet) + "'" + str(round(inches))


async def string_pop(string, topop):
    string = list(string)
    string.pop(topop)
    return "".join(string)


async def split_even(string):
    return string[:len(string) // 2], string[len(string) // 2:]


async def spacify_function(text, num=1):
    spaces = ""
    while num != 0:
        num -= 1
        spaces += " "
    return spaces.join(list(text))


async def text_pretty(text, spacegoal=config["HELP_NAME_LIMIT"]):
    if len(text) > spacegoal - 1:
        return f"OVER {config['SPACEGOAL']}: CONTACT THE DEV"

    while len(text) != spacegoal:
        text += " "
    return text


async def function_backwords(passthrough):
    endString = ""
    for x in passthrough:
        endString = x + endString
    return endString


# Prints a person and their total pictures nicely.
async def text_pretty_mid_end(starttext, endtext, mid=config["CMD_HELP"]["MID"], spacegoal=config["SPACEGOAL"], txtp=20):
    if len(starttext) > spacegoal - 1:
        return f"OVER {config['SPACEGOAL']}: CONTACT THE DEV"

    spaces = ""
    starttext = await text_pretty(starttext, txtp)

    while len(starttext) + len(spaces) != spacegoal:
        spaces += " "

    spaces1, spaces2 = await split_even(spaces)

    return f"{starttext}{spaces1}{mid}{spaces2}{endtext}"


async def get_top_dict(dictionary, num=10000000000000000, return_type="full"):
    topx = {k: v for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True)[:num]}

    return_list = []
    for key in topx:
        return_list.append((key, dictionary[key]))

    if return_type == "raw":
        try:
            return return_list[0][0]
        except IndexError:
            return None

    elif return_type == "full":
        return return_list

    else:
        raise TypeError(f"return_type of {return_type} is not valid")


async def gen_settings(guild_id):
    if not os.path.exists(f"./data/{guild_id}"):
        os.mkdir(f"./data/{guild_id}")

    if os.path.exists(f"./data/{guild_id}/settings.json"):
        os.remove(f"./data/{guild_id}/settings.json")

    with open(f"./data/{guild_id}/settings.json", "w") as fp:
        json.dump(config['DEFAULT_SETTINGS'], fp, indent=4)


async def return_all_faces_formatted(client, ctx):
    returnString = f"Faces for `{ctx.guild.name}`\n```\n"
    for discordID in list(client.facesDict[str(ctx.guild.id)].keys()):
        try:
            member = await ctx.guild.fetch_member(int(discordID))
        except discord.errors.NotFound:
            del client.facesDict[str(ctx.guild.id)][discordID]
            continue
        returnString += await text_pretty_mid_end(f"{member.name}#{member.discriminator}", str(
            len(list(client.facesDict[str(ctx.guild.id)][str(discordID)].keys()))), spacegoal=40, txtp=38)
        returnString += "\n"

    return f"{returnString}```"


async def guild_settings(guild_id, ctx=None, setting=None, value=None):
    try:
        with open(f"./data/{guild_id}/settings.json", 'r') as fp:
            settingsDict = json.load(fp)
    except FileNotFoundError:
        await gen_settings(guild_id)
        if ctx is not None:
            await ctx.send("Generated settings for your guild")
        with open(f"./data/{guild_id}/settings.json", 'r') as fp:
            settingsDict = json.load(fp)

    for val in list(config["DEFAULT_SETTINGS"].keys()):
        if val in list(settingsDict.keys()):
            continue
        if ctx is not None:
            await ctx.send(f"A new setting `{val}` has been added")

    for val in list(settingsDict.keys()):
        if val in config['DEFAULT_SETTINGS']:
            continue
        if ctx is not None:
            await ctx.send(f"The setting `{val}` has been depreciated, it has been deleted! It's previous value was:\n{settingsDict[val]}")
        del settingsDict[val]

    if value is None:
        if setting is None:
            try:
                return settingsDict
            except KeyError:
                return None
        try:
            return settingsDict[setting]
        except KeyError:
            return None

    if value == "None":
        value = None
    settingsDict[setting] = value

    try:
        with open(f"./data/{guild_id}/settings.json", "w") as fp:
            json.dump(settingsDict, fp, indent=4)
            return True

    except FileNotFoundError:
        os.mkdir(f"./data/{guild_id}")
        with open(f"./data/{guild_id}/settings.json", "w") as fp:
            json.dump(settingsDict, fp, indent=4)
            return True


async def format_member_pretty(member):
    return f"{member.name}#{member.discriminator}"


async def bump_total_mod(client, type_, to_change_id, guild_id, amount=0):
    guild_id = str(guild_id)
    to_change_id = str(to_change_id)
    try:
        if type_ == "add":
            try:
                oldVal = client.bumpDict[guild_id][to_change_id]
            except KeyError:
                oldVal = 0

            oldVal += amount
            try:
                client.bumpDict[guild_id][to_change_id] = oldVal
            except KeyError:
                client.bumpDict[guild_id] = {}
                client.bumpDict[guild_id][to_change_id] = oldVal

        elif type_ == "minus":
            try:
                oldVal = client.bumpDict[guild_id][to_change_id]
            except KeyError:
                return

            oldVal -= amount
            if oldVal <= 0:
                client.bumpDict[guild_id].pop(to_change_id)

            else:
                client.bumpDict[guild_id][to_change_id] = oldVal
        elif type_ == "one":
            try:
                oldVal = client.bumpDict[guild_id][to_change_id]
            except KeyError:
                return 0
            return oldVal

        elif type_ == "list":
            return client.bumpDict[guild_id]

        else:
            raise TypeError(f"Invalid type of '{type_}'!")
    finally:
        try:
            try:
                with open(f"./data/{guild_id}/bumptotals.json", "w") as fp:
                    json.dump(client.bumpDict[guild_id], fp, indent=4)
            except KeyError:
                with open(f"./data/{guild_id}/bumptotals.json", "w") as fp:
                    json.dump({}, fp)
        except FileNotFoundError:
            os.mkdir(f"./data/{guild_id}")
            try:
                with open(f"./data/{guild_id}/bumptotals.json", "w") as fp:
                    json.dump(client.bumpDict[guild_id], fp, indent=4)
            except KeyError:
                with open(f"./data/{guild_id}/bumptotals.json", "w") as fp:
                    json.dump({}, fp)


async def message_data_mod(client, type_, author_id, message_id, data=None):
    if type_ == "add":
        try:
            client.msg_data[author_id].append((message_id, data))
        except KeyError:
            client.msg_data[author_id] = []
            client.msg_data[author_id].append((message_id, data))
        return True

    elif type_ == "remove":
        try:
            correct_data = ()
            for data in client.msg_data[author_id]:
                if data[0] == message_id:
                    correct_data = data
                    break
            if not correct_data:
                return False

            client.msg_data[author_id].remove(correct_data)
            return correct_data[1]
        except KeyError:
            return False

    elif type_ == "list":
        return client.msg_data[author_id]

    else:
        raise Exception(f"Invalid type of '{type_}'!")


async def counting_channel(client, type_, guild_id, val=0, lastbump_id=None, channel=None):
    guild_id = str(guild_id)
    newval = None
    returnval = None
    try:
        if type_ == "add":
            try:
                oldVal = client.countDict[guild_id]
            except KeyError:
                oldVal = 0

            if lastbump_id is not None:
                with open(f"./data/{guild_id}/count_id.txt", "w") as fp:
                    fp.write(str(lastbump_id))

            newval = val + oldVal

            if channel is not None:
                await channel.edit(topic=f"The current count is `{newval}`")
            client.countDict[guild_id] = newval

        elif type_ == "set":
            try:
                oldVal = client.countDict[guild_id]
            except KeyError:
                oldVal = 0

            if lastbump_id is not None:
                with open(f"./data/{guild_id}/count_id.txt", "w") as fp:
                    fp.write(str(lastbump_id))

            newval = val
            if channel is not None:
                await channel.edit(topic=f"The current count is `{newval}`")
            client.countDict[guild_id] = val
            return oldVal

        elif type_ == "get_val":
            newval = client.countDict[guild_id]
            return newval

        elif type_ == "get_id":
            with open(f"./data/{guild_id}/count_id.txt", 'r') as fp:
                returnval = int(fp.read())

        else:
            raise TypeError(f"Invalid type of '{type_}'!")
    finally:
        if newval is None:
            return returnval
        try:
            try:
                with open(f"./data/{guild_id}/count.txt", "w") as fp:
                    fp.write(str(client.countDict[guild_id]))
            except KeyError:
                with open(f"./data/{guild_id}/count.txt", "w") as fp:
                    fp.write("0")
        except FileNotFoundError:
            os.mkdir(f"./data/{guild_id}")
            try:
                with open(f"./data/{guild_id}/count.txt", "w") as fp:
                    fp.write(str(client.countDict[guild_id]))
            except KeyError:
                with open(f"./data/{guild_id}/count.txt", "w") as fp:
                    fp.write("0")


async def get_id_channel(text):
    try:
        match = re.search(r"<#\d{18}?>", text)
    except TypeError:
        match = None
    if match is None:
        return

    match = await string_pop(match.group(), 0)
    match = await string_pop(match, 0)
    match = await string_pop(match, len(match)-1)
    return int(match)


async def get_id_mention(text):
    try:
        match = re.search(r"<@!?\d{18}?>", text)
    except TypeError:
        match = None
    if match is None:
        return

    match = await string_pop(match.group(), 0)
    match = await string_pop(match, 0)
    match = await string_pop(match, len(match)-1)
    if match[0] == "!":
        match = await string_pop(match, 0)
    return int(match)


async def determine_prefix(client, ctx, r=None):
        if r != 'r':
            try:
                return [client.custom_prefixes[str(ctx.guild.id)], f"<@{config['BOTID']}> ", f"<@!{config['BOTID']}> "]
            except KeyError:
                return [config['PREFIX'], f"<@{config['BOTID']}> ", f"<@!{config['BOTID']}> "]
        else:
            try:
                return client.custom_prefixes[str(ctx.guild.id)]
            except KeyError:
                return config['PREFIX']