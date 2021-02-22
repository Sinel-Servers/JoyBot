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

import os
import discord
from discord.ext import commands

from classes.exceptions import AlreadyCountedError
from classes.database.guild import Counting, Ban


# ---------------------------------Code------------------------------------#

class Count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.countDict = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if Ban(message.guild.id).is_banned():
            return

        counting = Counting(message.guild.id)
        if message.guild is None or message.channel.id != counting.channel_get_id():
            return

        try:
            if not message.content.isnumeric():
                await message.delete()
                await message.author.send("That's not a number!")
                return

            curnum = counting.get()
            try:
                if int(message.content) != curnum+1:
                    await message.delete()
                    await message.author.send(f"That's not the next number!\nHint: it's `{curnum+1}`!")
                    return
            except ValueError:
                await message.delete()
                await message.author.send("That's not a number!")
                return

            try:
                counting.add(message.author.id)
            except AlreadyCountedError:
                await message.author.send("You can't count twice in a row!")
                return

        except discord.errors.HTTPException:
            return


def setup(bot):
    bot.add_cog(Count(bot))
