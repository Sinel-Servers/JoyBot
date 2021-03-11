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


from discord.ext import commands

from config import config
from classes.database.message import Message
from functions import string_pop


class polls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["yesnovote"])
    async def yesnopoll(self, ctx: commands.Context, *, question: str = None):
        # TODO: Switch to using wait_for
        #       https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for
        if question is None:
            msg = await ctx.send(f"{ctx.author.mention}, Please supply arguments!\nExample:    `.numberpoll This is the question`")
            await msg.add_reaction(config["CHAR_CROSS"])
            Message(ctx.author.id, msg.id).add("delete")
            return
        await ctx.message.delete()

        msg = await ctx.send(f"{ctx.author.mention} wants to know:\n**Yes/No** `{question}`")
        reactions = [config["CHAR_CROSS"], config["CHAR_YES"], config["CHAR_NO"]]
        for reaction in reactions:
            await msg.add_reaction(reaction)
        Message(ctx.author.id, msg.id).add("delete")

    @commands.command(aliases=["numbervote"])
    async def numberpoll(self, ctx: commands.Context, *, text: str = None):
        # TODO: Switch to using wait_for
        #       https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for
        await ctx.message.delete()
        if text is None:
            msg = await ctx.send(f"{ctx.author.mention}, Please supply arguments!\nExample:\t`.numberpoll This is the question, This is answer one, This is answer two, etc`")
            await msg.add_reaction(config["CHAR_CROSS"])
            Message(ctx.author.id, msg.id).add("delete")
            return

        split = text.split(",")

        if len(split) == 1:
            error = await ctx.send(f"{ctx.author.mention}, Please supply some answers, not just the question!\n`{text}`")
            await error.add_reaction(config["CHAR_CROSS"])
            Message(ctx.author.id, error.id).add("delete")
            return

        if len(split) > 11:
            error = await ctx.send(f"{ctx.author.mention}, Please limit your poll to 10 options or less!\n`{text}`")
            await error.add_reaction(config["CHAR_CROSS"])
            Message(ctx.author.id, error.id).add("delete")
            return

        popsplit = []
        for string in split:
            while string[0] == " ":
                string = await string_pop(string, 0)

            while string[len(string)-1] == " ":
                string = await string_pop(string, len(string)-1)
            
            popsplit.append(string)

        header = popsplit[0]
        popsplit.pop(0)

        sendmessage = f"{ctx.author.mention} asks `{header}`:\n"
        curnum = 1
        for string in popsplit:
            if curnum == len(popsplit)+1:
                break
            sendmessage = sendmessage + f"{config['numpoll'][curnum]} — {string}\n"
            curnum += 1

        msg = await ctx.send(sendmessage)

        curnum = 1
        for _ in popsplit:
            if curnum == len(popsplit)+1:
                break
            await msg.add_reaction(config["numpoll"][curnum])
            curnum += 1

        await msg.add_reaction(config["CHAR_CROSS"])

        Message(ctx.author.id, msg.id).add("delete")


def setup(bot):
    bot.add_cog(polls(bot))
