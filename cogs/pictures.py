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
import json
import os
import random

from discord.ext import commands
from typing import Union

from config import config
from classes.database.guild import Settings
from classes.database.guild import Pictures as Pic
from functions import determine_prefix


# ---------------------------------Code------------------------------------#

class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randomface(self, ctx, member: Union[discord.Member, str] = None):
        try:
            guild_faces = self.bot.facesDict[str(ctx.guild.id)]
        except KeyError:
            await ctx.send("This guild doesn't have any faces, ask an admin to add some!")
            return

        if member is not discord.Member:
            if member.lower() == "list":
                msg = await ctx.send("Getting faces list...")
                pic = Pic(ctx.guild.id)
                await msg.edit(content=pic.list())
                return

            await ctx.send("That's not a valid member!")
            return

        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.bot, ctx, True)}help randomface` if you're stuck!")
            return
        try:
            chosen_face_id = random.choice(list(guild_faces[str(member.id)].keys()))
            chosen_face = guild_faces[str(member.id)][chosen_face_id]
        except KeyError:
            await ctx.send(f"This person doesn't have any faces!")
            return

        e = discord.Embed(title=f"Random face from {member}", description=f"Picture ID: `{chosen_face_id}`")
        e.set_footer(text=f"Requested by {ctx.author} ({ctx.author.id})")
        e.set_image(url=chosen_face)

        await ctx.send(embed=e)

    @commands.command()
    async def addface(self, ctx, member: discord.Member = None):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator and ctx.author.id not in await Settings(ctx.guild.id).get_setting("adminslist"):
            await ctx.send("You're not an admin!")
            return

        try:
            guild_faces = self.bot.facesDict[str(ctx.guild.id)]
        except KeyError:
            guild_faces = {}

        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.bot, ctx, True)}help randomface` if you're stuck!")
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
            await ctx.send("Bots don't have faces!")
            return

        if str(member.id) in list(guild_faces.keys()):
            toadd = len(guild_faces[str(member.id)]) + 1
            guild_faces[str(member.id)][str(toadd)] = file.url
            await ctx.send(f"Added `{member}`'s picture number `{toadd}`!")

        else:
            guild_faces[str(member.id)] = {}
            guild_faces[str(member.id)]["1"] = file.url
            await ctx.send(f"Added `{member}`'s first picture!")

        self.bot.facesDict[str(ctx.guild.id)] = guild_faces
        try:
            with open(f"./data/{ctx.guild.id}/faces.json", "w") as fp:
                json.dump(self.bot.facesDict[str(ctx.guild.id)], fp)
        except FileNotFoundError:
            os.mkdir(f"./data/{ctx.guild.id}/")
            with open(f"./data/{ctx.guild.id}/faces.json", "w") as fp:
                json.dump(self.bot.facesDict[str(ctx.guild.id)], fp)

    @commands.command()
    async def delface(self, ctx):
        await ctx.send("Hi, unfortunately due to code corruption this command is gone! The team behind this are working hard to build it all from scratch, but for now you can join the support server (`.info`), and have someone remove any faces manually.\n\nThanks for the understanding!")


def setup(bot):
    bot.add_cog(Pictures(bot))
