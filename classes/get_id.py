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

import re
from data.bot.bot_functions import string_pop


class get_id:
    async def channel(self, text: str):
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

    async def member(self, text: str):
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
