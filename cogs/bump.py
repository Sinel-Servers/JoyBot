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
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            if Ban(message.guild.id).is_banned():
                return
        except AttributeError:
            return

        if Counting(message.guild.id).channel_get_id() == message.channel.id:
            return

        if message.author.id == config['DISBOARDID']:
            for embed in message.embeds:
                if ":thumbsup:" in embed.description:
                    bumpID = await get_id().member(embed.description)
                    bump = Bmp(message.guild.id, bumpID)
                    oldtop = bump.get_top(raw=True)
                    firstbumpid = bump.get_first_bump()

                    bump.add_total()
                    newtop = bump.get_top(raw=True)

                    send_msg = f"<@{bumpID}>, your bump total has been increased by one!\nType `.bumptotal` to view your current bump total!"
                    if firstbumpid is None:
                        send_msg += "\n\nYou were also the first to bump the server. Congrats!"
                        if oldtop is not None:
                            send_msg += "\n(I moved to a new way of tracking the first bump, so sorry that you got this message again!)"

                    else:
                        if oldtop != newtop:
                            send_msg += "\nYou also managed to get the top spot! Nice!"
                            send_msg += f"\n\n<@{oldtop}>, you've lost your top spot!"

                    await message.channel.send(send_msg)

    @commands.command()
    async def bumptotal(self, ctx: commands.Context, person: discord.Member = None):
        if person is None:
            person = ctx.author

        bump = Bmp(ctx.guild.id, person.id)

        e = discord.Embed()
        e.title = f"`{person}`'s bump stats"

        if bump.get_pos() is None:
            e.add_field(name="Bump Stats", value="This person has not bumped this discord server yet!")
        else:
            e.add_field(name="Bump Stats",
                        value=f"Bump total: `{bump.get_total()}\n`"
                              f"Bump position: `{bump.get_pos()}`\n"
                              f"Current streak: `{bump.get_streak()[0]}`\n"
                              f"Highest streak: `{bump.get_streak()[1]}`\n"
                        )

        special_badges = ""

        if bump.get_first_bump() == person.id:
            badgename = f"badge_first_bump"
            badgeid = config["EMOJI_IDS"][badgename]
            special_badges += f"<:{badgename}:{badgeid}>"

        pos = bump.get_pos()
        if pos in range(1, 4):
            badgename = f"badge_{pos}_place"
            badgeid = config["EMOJI_IDS"][badgename]
            special_badges += f"<:{badgename}:{badgeid}>"

        if special_badges:
            e.add_field(name="Special Badges", value=special_badges, inline=False)

        normal_badges_nums = [key for key in config["BUMP_FUNNIES"] if key <= bump.get_total()]
        normal_badges = ""
        for value in normal_badges_nums:
            value = config["BUMP_FUNNIES"][value][1]
            if value.startswith("!"):
                value = await string_pop(value, 0)
                normal_badges += f":{value}: "
            else:
                badgeid = config["EMOJI_IDS"][value]
                normal_badges += f"<:{value}:{badgeid}>"

        if normal_badges:
            e.add_field(name="Normal Badges", value=normal_badges, inline=False)

        # TODO: Events?
        event_badges = ""
        if event_badges:
            e.add_field(name="Event Badges", value=event_badges, inline=False)

        e.set_thumbnail(url=person.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def topbumptotal(self, ctx: commands.Context, tnum: int = 10):
        if tnum == 1:
            bump = Bmp(ctx.guild.id)
            await self.bumptotal(ctx, ctx.guild.get_member(int(bump.get_top(1, raw=True))))
            return

        if tnum < 1:
            await ctx.send("Please make the number more than 0!")
            return

        elif tnum > 50:
            await ctx.send("Please keep the number less than 51!")
            return

        bump = Bmp(ctx.guild.id, ctx.author.id)
        try:
            topbumps = bump.get_top(tnum)
            if not topbumps:
                raise NoDataError

        except NoDataError:
            await ctx.send(content=f"{ctx.author.mention}, looks like nobody has bumped disboard yet")
            return

        sendstring = ""
        message = await ctx.send(f"Getting the top {tnum} total times bumped...")

        for num, bump_data in enumerate(topbumps):
            num += 1
            user = await self.bot.fetch_user(bump_data[0])

            endstring = ""
            try:
                endstring = " — " + config["BUMP_FUNNIES"][bump_data[1]][0]
            except KeyError:
                pass

            try:
                badge = ""
                if num in range(1, 4):
                    badgename = f"badge_{num}_place"
                    badgeid = config["EMOJI_IDS"][badgename]
                    badge = f"<:{badgename}:{badgeid}>"

                if badge == "":
                    badgename = config["BUMP_FUNNIES"][bump_data[1]][1]
                    if badgename.startswith("!"):
                        badgename = await string_pop(badgename, 0)
                        badge = f":{badgename}:"

                    else:
                        badgeid = config["EMOJI_IDS"][badgename]
                        badge = f"<:{badgename}:{badgeid}>"

                if badge == "":
                    if user.id == bump.get_first_bump():
                        badgename = "badge_first_bump"
                        badgeid = config["EMOJI_IDS"][badgename]
                        f"<:{badgename}:{badgeid}>"

            except KeyError:
                badge = "\u200e \u200e \u200e \u200e \u200e \u200e \u200e"

            if num >= 9:
                sendstring += f"{badge} {num})  {user} — {bump_data[1]} {endstring}\n"
            else:
                sendstring += f"{badge} {num})   {user} — {bump_data[1]} {endstring}\n"

        top = discord.Embed(
                title=f"Top {tnum} bump totals for `{ctx.guild.name}`",
                description="These are the top bump totals for this guild. `!d bump` to try and get on the leaderboard!"
            )
        top.add_field(name="Leaderboard", value=sendstring, inline=False)
        top.set_thumbnail(url=ctx.guild.icon_url)

        try:
            await message.edit(embed=top, content=None)

        except discord.errors.HTTPException:
            top = discord.Embed(
                title=f"Top {tnum} bump totals for `{ctx.guild.name}`",
                description="These are the top bump totals for this guild. `!d bump` to try and get on the leaderboard!"
            )
            top.set_thumbnail(url=ctx.guild.icon_url)

            sendstring = [string+"\n" for string in sendstring.split("\n")]

            sendstring_1, sendstring_2 = sendstring[:len(sendstring)//2], sendstring[len(sendstring)//2:]
            sendstring_1, sendstring_2 = "".join(sendstring_1), "".join(sendstring_2)

            top.add_field(name="Leaderboard", value=sendstring_1, inline=False)
            top.add_field(name="\u200e", value=sendstring_2, inline=False)

            try:
                await message.edit(embed=top, content=None)

            except discord.errors.HTTPException:
                await message.edit(content="Sorry, the embed was too big to send :(\nTry a smaller number!")

    @commands.command()
    async def changebumptotal(self, ctx: commands.Context, person: discord.Member = None, amount: Union[int, str] = None):
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
    async def resetbumptotal(self, ctx: commands.Context, person: Union[discord.Member, str]):
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
