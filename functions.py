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


from decimal import Decimal
from operator import itemgetter
from discord.ext.commands import Context
from discord import Message
from typing import Union
from classes.database.guild import Settings
from config import config


# --------------------------------Functions--------------------------------#

def quotify(text: str):
    return "'" + text + "'"


async def inch_cm(convert: Union[str, int]):
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


async def string_pop(string: str, topop: int):
    string = list(string)
    string.pop(topop)
    return "".join(string)


async def split_even(string: str):
    return string[:len(string) // 2], string[len(string) // 2:]


async def text_pretty(text: str, spacegoal: int = config["HELP_NAME_LIMIT"]):
    if len(text) > spacegoal - 1:
        return f"OVER {config['SPACEGOAL']}: CONTACT THE DEV"

    while len(text) != spacegoal:
        text += " "
    return text


async def function_backwords(text: str):
    return text[::-1]


# Prints a person and their total pictures nicely.
async def text_pretty_mid_end(starttext: str, endtext: str, mid: str = config["CMD_HELP"]["MID"], spacegoal: int = config["SPACEGOAL"], txtp: int = 20):
    if len(starttext) > spacegoal - 1:
        return f"OVER {config['SPACEGOAL']}: CONTACT THE DEV"

    spaces = ""
    starttext = await text_pretty(starttext, txtp)

    while len(starttext) + len(spaces) != spacegoal:
        spaces += " "

    spaces1, spaces2 = await split_even(spaces)

    return f"{starttext}{spaces1}{mid}{spaces2}{endtext}"


def sort_dict(dictionary: dict, num: int = 10000000000000000, return_type: str = "full"):
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
        if num == 1:
            return return_list[0] if len(return_list) != 0 else {}
        return return_list

    else:
        raise TypeError


# noinspection PyUnusedLocal
async def determine_prefix(bot, ctx: Union[Context, Message], raw: bool = False):
    settings = Settings(ctx.guild.id)
    if raw:
        return settings.get_setting("prefix")
    return settings.get_setting("prefix"), f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "
