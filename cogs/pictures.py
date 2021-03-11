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
import random
from discord.ext import commands
from typing import Union

from config import config
from classes.errors import UnauthorizedUserException
from classes.database.guild import Settings
from classes.database.guild import Pictures as Pic
from functions import determine_prefix, text_pretty_mid_end


# ---------------------------------Code------------------------------------#

class Pictures(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def randompic(self, ctx: commands.Context, member: Union[discord.Member, str] = None):
        pictures = Pic(ctx.guild.id)
        if not pictures.list():
            await ctx.send("This guild doesn't have any pictures, ask an admin to add some!")
            return

        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.bot, ctx, True)}help randompic` if you're stuck!")
            return

        if type(member) is not discord.Member:
            if member.lower() == "list":
                msg = await ctx.send("Getting pictures list...")
                piclist = f"Faces for `{ctx.guild.name}`\n```\n"
                for discordID in pictures.list():
                    try:
                        member = await ctx.guild.fetch_member(discordID)
                        member = f"{member.name}#{member.discriminator}"
                    except discord.errors.NotFound:
                        Pic(ctx.guild.id, discordID).delete_user()
                        continue

                    piclist += await text_pretty_mid_end(member, str(
                        len(pictures.list()[discordID])), spacegoal=40, txtp=38)
                    piclist += "\n"

                piclist += "```"
                await msg.edit(content=piclist)
                return

            await ctx.send("That's not a valid member!")
            return

        try:
            chosen_pic_url = random.choice(pictures.list()[member.id])
        except KeyError:
            await ctx.send(f"This person doesn't have any pictures!")
            return

        e = discord.Embed(title=f"Random picture from {member}")
        e.set_footer(text=f"Requested by {ctx.author} ({ctx.author.id})")
        e.set_image(url=chosen_pic_url)

        await ctx.send(embed=e)

    @commands.command()
    async def addpic(self, ctx: commands.Context, member: discord.Member = None):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator and ctx.author.id not in Settings(ctx.guild.id).get_setting("admins_list"):
            raise UnauthorizedUserException

        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.bot, ctx, True)}help addpic` if you're stuck!")
            return

        if not ctx.message.attachments:
            await ctx.send(f"{ctx.author.mention}, please use this command with an attached file!")
            return

        file = ctx.message.attachments[0]
        try:
            valid_url, _ = file.url.split("?")
        except ValueError:
            valid_url = file.url

        valid = False
        valid_url = valid_url.lower()
        for extension in config['PICEXT']:
            if valid_url.endswith(extension):
                valid = True
                break

        if not valid:
            valid_attachments = ", "
            valid_attachments.join(config['PICEXT'])
            await ctx.send(f"That's not in the valid attachments!\nValid attachments: `{valid_attachments}`")
            return

        if member.bot:
            await ctx.send("Bots don't have pictures!")
            return

        Pic(ctx.guild.id, member.id).add_picture(valid_url)
        await ctx.send("Added picture successfully!")

    @commands.command()
    async def delpic(self, ctx: commands.Context):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator and ctx.author.id not in Settings(ctx.guild.id).get_setting("admins_list"):
            raise UnauthorizedUserException

        await ctx.send(f"Hi, unfortunately due to code corruption this command is gone! The team behind this are working hard to build it all from scratch, but for now you can join the support server (`{await determine_prefix(self.bot, ctx, True)}info`), and have someone remove any pictures manually.\n\nThanks for the understanding!")


def setup(bot):
    bot.add_cog(Pictures(bot))
