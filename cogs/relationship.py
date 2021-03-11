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

# You may contact me at joybot@sinelservers.xyz


import discord
from random import choice
from discord.ext import commands
from config import config
from functions import string_pop

# ---------------------------------Code------------------------------------ #


class Relationship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx: commands.Context, person: discord.Member = None):

        if person is None:
            await ctx.send("I need to know who you are kissing!")
            return
        if person.id == ctx.author.id:
            await ctx.send("You can't kiss yourself!")
            return
        if person.id == self.bot.user.id:
            await ctx.send("Awwh, i aprreciate you trying but i don't want you to freeze!")
            return
        if person.bot is True:
            await ctx.send("You can't kiss a bot, you'll get stuck to it! (we have no hearts, so we're very cold)")
            return

        with open("kiss.txt", "r") as fp:
            url = choice(fp.readlines())
            if url.endswith("\n"):
                url = await string_pop(url, -1)

        e = discord.Embed(title=f"{ctx.author} has kissed {person}")
        e.set_image(url=url)

        await ctx.send(embed=e)

    @commands.command()
    async def hug(self, ctx: commands.Context, person: discord.Member = None):

        if person is None:
            await ctx.send("I need to know who you are hugging!")
            return
        if person.id == ctx.author.id:
            await ctx.send("You can't hug yourself!")
            return
        if person.id == self.bot.user.id:
            await ctx.send("Awwh, i aprreciate you trying but i don't want you to freeze!")
            return
        if person.bot is True:
            await ctx.send("You can't hug a bot, you'll get stuck to it! (we have no hearts, so we're very cold)")
            return

        with open("hug.txt", "r") as fp:
            url = choice(fp.readlines())
            if url.endswith("\n"):
                url = await string_pop(url, -1)

        e = discord.Embed(title=f"{ctx.author} has hugged {person}")
        e.set_image(url=url)

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Relationship(bot))
