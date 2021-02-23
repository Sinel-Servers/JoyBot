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


import discord
from typing import Union
from discord.ext import commands

from functions import string_pop, determine_prefix
from classes.exceptions import NoDataError
from classes.database.guild import Settings, Counting, Ban
from classes.database.guild import Bump as Bmp
from classes.get_id import get_id
from config import config


# ---------------------------------Code------------------------------------ #

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if Ban(message.guild.id).is_banned():
                return
        except AttributeError:
            return

        counting = Counting(message.guild.id)
        if counting.channel_get_id() == message.channel.id:
            return

        firstbump = False
        if message.author.id == config['DISBOARDID']:
            for embed in message.embeds:
                if ":thumbsup:" in embed.description:
                    bumpID = await get_id().member(embed.description)
                    bump = Bmp(message.guild.id, bumpID)
                    oldtop = str(bump.get_top(raw=True))

                    if oldtop is None:
                        firstbump = True
                        oldtop = 0

                    bump.add_total()
                    newtop = str(bump.get_top(raw=True))

                    send_msg = f"<@{bumpID}>, your bump total has been increased by one!\nType `.bumptotal` to view your current bump total!"
                    if not firstbump:
                        if oldtop != newtop:
                            send_msg += "\nYou also managed to get the top spot! Nice!"
                            send_msg += f"\n\n<@{oldtop}>, you've lost your top spot!"

                    else:
                        send_msg += "\n\nYou were also the first to bump the server. Congrats!"

                    await message.channel.send(send_msg)

    @commands.command()
    async def bumptotal(self, ctx, person: discord.Member = None):
        if person is None or person.id == ctx.author.id:
            bump = Bmp(ctx.guild.id, ctx.author.id)
            curScore = bump.get_total()

            if curScore == 0:
                await ctx.send("You haven't bumped disboard yet")
            else:
                await ctx.send(f"Here is your total times bumped: `{curScore}`")

        else:
            bump = Bmp(ctx.guild.id, ctx.person.id)
            curScore = bump.get_total()

            if curScore == 0:
                await ctx.send(f"{person} hasn't bumped disboard yet!")
            else:
                await ctx.send(f"{person} has bumped disboard `{curScore}` times")

    @commands.command()
    async def topbumptotal(self, ctx):
        bump = Bmp(ctx.guild.id, ctx.author.id)
        try:
            topbumps = bump.get_top(10)
            if not topbumps:
                raise NoDataError

        except NoDataError:
            await ctx.send(content=f"{ctx.author.mention}, looks like nobody has bumped disboard yet")
            return

        printstring = ""
        message = await ctx.send(f"Getting the top 10 total times bumped...")

        for num, bump_data in enumerate(topbumps):
            user = await self.bot.fetch_user(bump_data[0])

            endstring = ""
            for funny in config['BUMP_FUNNIES']:
                if bump_data[1] == funny[0]:
                    endstring = f" — {funny[1]}"

            else:
                if num >= 9:
                    printstring += f"{num + 1})   {user} — {bump_data[1]}{endstring}\n"
                else:
                    printstring += f"{num + 1})    {user} — {bump_data[1]}{endstring}\n"

        await message.edit(
            content=f"{ctx.author.mention}, here are the top 10 total times bumped:\n```{printstring}```")

    @commands.command()
    async def changebumptotal(self, ctx, person: discord.Member = None, amount: Union[int, str] = None):
        if ctx.author.id not in config["SUPERADMINIDS"]:
            await ctx.send(f"{ctx.author.mention}, you can't use this command!")
            return

        if person is None:
            await ctx.send(f"{ctx.author.mention}, Please supply a person!")
            return

        if amount is None:
            await ctx.send(f"{ctx.author.mention}, Please supply a numeric amount to change by!")
            return

        if not str(amount).isnumeric():
            if str(amount)[0] == "-":
                test_amount = await string_pop(str(amount), 0)
                if not test_amount.isnumeric():
                    await ctx.send(f"{ctx.author.mention}, Please supply a ***numeric*** amount to change by!")
                    return

        if person.id == ctx.author.id:
            person_name = "your"
            person_id = ctx.author.id
        else:
            person_name = f"{person}'s"
            person_id = person.id

        bump = Bmp(ctx.guild.id, person_id)
        if str(amount)[0] == "-":
            amount = await string_pop(str(amount), 0)
            bump.remove_total(int(amount))
            await ctx.send(f"Changed {person_name} bump total by -{amount}")
        else:
            bump.add_total(int(amount))
            await ctx.send(f"Changed {person_name} bump total by {amount}")

    @commands.command()
    async def resetbumptotal(self, ctx, person: Union[discord.Member, str]):
        if ctx.author.id not in config["SUPERADMINIDS"] and ctx.author.id not in Settings(ctx.guild.id).get_setting("admins_list") and not ctx.author.guild_permissions.administrator:
            await ctx.send(f"{ctx.author.mention}, you can't use this command!")
            return

        if person is discord.Member:
            if person.id == ctx.author.id:
                person_name = "your"
                person_id = ctx.author.id
            else:
                person_name = f"{person}'s"
                person_id = person.id

            bump = Bmp(ctx.guild.id, person_id)
            bump.reset_total()
            await ctx.send(f"Reset {person_name} bump total!")

        elif person == "server":
            bump = Bmp(ctx.guild.id)
            bump.reset_guild_total()
            await ctx.send(f"Reset everyone's bump total!")

        else:
            await ctx.send(f"That's not a valid argument! Type `{await determine_prefix(self.bot, ctx, True)}help resetbumptotal` for help!")


def setup(bot):
    bot.add_cog(Bump(bot))
