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
from discord.ext import commands

from config import config
from classes.exceptions import NoDataError
from classes.database.message import Message
from classes.database.guild import Bump, Pictures, Settings, Counting, Ban
from functions import inch_cm, determine_prefix


# ---------------------------------Code------------------------------------ #


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def backwords(self, ctx, *, text):
        text = f"{ctx.author.mention}, here's your backwords string: {text[::-1]}" if text != "" else f"{ctx.author.mention}, please provide something to return backwords!"
        await ctx.send(text)

    @commands.command()
    async def reversecaps(self, ctx, *, text=None):
        if text is None:
            await ctx.send(f"{ctx.author.mention}, please suppy an argument to reversecaps!")
            return

        await ctx.send(f"{ctx.author.mention}, here is your reversecaps:\n{text.swapcase()}")

    @commands.command()
    async def convert(self, ctx, text=None):
        if text is None:
            await ctx.send(f"Please convert either:\nFeet'inches to CM `{await determine_prefix(self.bot, ctx, True)}"
                           f"convert 6'2`\nCM to Feet'inches `{await determine_prefix(self.bot, ctx, True)}convert 188"
                           f"`\nMetres to CM `{await determine_prefix(self.bot, ctx, True)}convert 1.88`")
            return

        convert = await inch_cm(text)
        if convert is not False:
            await ctx.send(f"{ctx.author.mention}, here is your conversion: {convert}")
        else:
            await ctx.send(f"{ctx.author.mention}, that's not a valid conversion!")

    @commands.command()
    async def spacify(self, ctx, *, text):
        text = list(text)
        text = " ".join(text)
        await ctx.send(f"{ctx.author.mention}, here is your message:\n{text}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        message = Message(reaction.user_id, reaction.message_id)
        try:
            msgmod = message.get()
        except NoDataError:
            return
        try:
            if msgmod[0] == "guild ban":
                if str(reaction.emoji) == config["CHAR_TICK"]:
                    await msgmod[1].edit(content="Deleting all data for that guild...")
                    Bump(msgmod[2]).reset_guild_total()
                    Settings(msgmod[2]).reset_settings(False)
                    Pictures(msgmod[2]).delete_all()
                    Counting(msgmod[2]).reset()

                    Ban(msgmod[2]).ban()
                    await msgmod[1].edit(content="All data has been deleted, and the guild has been banned!")
                    message.remove()

                elif str(reaction.emoji) == config["CHAR_CROSS"]:
                    await msgmod[1].edit(content="Cancelled server ban")
                    message.remove()

            elif msgmod[0] == "delete":
                if str(reaction.emoji) == config["CHAR_CROSS"]:
                    ctx_guild = self.bot.get_guild(reaction.guild_id)
                    ctx_channel = ctx_guild.get_channel(reaction.channel_id)
                    message = await ctx_channel.fetch_message(reaction.message_id)
                    await message.delete()
                    message.remove()

        except TypeError:
            return

    @commands.command()
    async def guildban(self, ctx, guild_id=None):
        if ctx.author.id not in config["SUPERADMINIDS"]:
            await ctx.send("You can't use this command!")
            return
        if guild_id is None:
            await ctx.send(f"Please use this command with a guild id!\nExample: `{await determine_prefix(self.bot, ctx, True)}guildban 753463761704321034`")
            return
        elif re.match(r"[0-9]{18}?", guild_id) is None:
            await ctx.send("That's not a valid guild!")
            return

        guild_ids = []
        for guild in self.bot.guilds:
            guild_ids.append(guild.id)

        if guild_id not in guild_ids:
            await ctx.send("I have no data on that guild!")
            return

        guild = self.bot.get_guild(int(guild_id))
        if guild is None:
            msg = await ctx.send("Seems this guild was deleted!\nWould you like to remove it's data?")
            Message(ctx.author.id, msg.id).add(("guild ban", msg, guild_id))
            await msg.add_reaction(config["CHAR_TICK"])
            await msg.add_reaction(config["CHAR_CROSS"])
            return

        msg = await ctx.send(f"Are you sure you want to remove all the guild data for `{guild.name}`?")
        Message(ctx.author.id, msg.id).add(("guild ban", msg, guild_id))
        await msg.add_reaction(config["CHAR_TICK"])
        await msg.add_reaction(config["CHAR_CROSS"])

    @commands.command()
    async def invite(self, ctx):
        link = "https://sinelservers.xyz/stuff-made/JoyBot/invite.php"
        await ctx.send(f"{ctx.author.mention}, here's an invite link to add JoyBot to your own server:\n{link}")

    @commands.command()
    async def info(self, ctx):
        blurb = f"""
Hey, i'm JoyBot! I was made by Joyte as a small project, and am currently just maintained and worked on by him!
I like long walks on the beach and watching the sunset :)

If you ever need help, just use the `{await determine_prefix(self.bot, ctx, True)}help` command, and i'll answer any and all questions you have!
If you've got a more serious problem with me, you can always visit my discord at https://sinelservers.xyz/discord.php where you can ask more in depth questions or report that there's something wrong with me
You can also make suggestions which you'd like added (although keep in mind my creator is just one person and is busy with school and other life-related things)

Hope you enjoy using me!
- JoyBot
        """
        await ctx.send(blurb)

    @commands.command()
    async def privacy(self, ctx):
        blurb = f"""
Hi, you're probably wondering what data we store on you, and that's okay! Everybody has a right to privacy. Check out our privacy policy here:
https://sinelserve8rs.xyz/stuff-made/JoyBot/privacy.php
        """
        await ctx.send(blurb)


def setup(bot):
    bot.add_cog(Other(bot))
