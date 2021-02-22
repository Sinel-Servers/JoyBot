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
from discord.ext import commands
from functions import return_all_faces_formatted, determine_prefix
from classes.database.guild import Counting
from classes.database.guild import Settings
from config import config


class _important(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #----------COGS------------#

    @commands.command()
    async def cogload(self, ctx, extension=None):
        if extension is None:
            await ctx.send(f"Please specify a cog!")
            return

        try:
            self.bot.load_extension(f"cogs.{extension}")

        except commands.errors.ExtensionFailed as error:
            await ctx.send(f"An error occured while loading this extension!\n`{error}`")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"Could not find the cog '{extension}'!")
            return

        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"The cog '{extension}' is already loaded!")
            return

        await ctx.send(f"The cog '{extension}' has been loaded!")

    @commands.command()
    async def cogreload(self, ctx, extension=None):
        if extension is None:
            await ctx.send(f"Please specify a cog!")
            return

        try:
            self.bot.reload_extension(f"cogs.{extension}")

        except commands.errors.ExtensionFailed as error:
            await ctx.send(f"An error occured while loading this extension!\n`{error}`")

        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The cog '{extension}' has not been loaded!")
            return

        await ctx.send(f"The cog '{extension}' has been reloaded!")

    @commands.command()
    async def cogunload(self, ctx, extension=None):
        if extension is None:
            await ctx.send(f"Please specify a cog!")
            return

        try:
            self.bot.unload_extension(f"cogs.{extension}")

        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The cog '{extension}' has not been loaded!")
            return

        await ctx.send(f"The cog '{extension}' has been unloaded!")

    #----MENTION HELP------#
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content != f"<@!{config['BOTID']}>" or message.content != f"<@{config['BOTID']}>":
            return
        if message.author.id == config["BOTID"]:
            return
        counting = Counting(message.guild.id)
        if counting.channel_get_id() == message.channel.id:
            return

        await message.channel.send(f"My prefix here is `{await determine_prefix(self.bot, message, 'r')}`!\n(Pinging me works everywhere: `@JoyBot#7306 `)\n\n"
                                   f"Type `{await determine_prefix(self.bot, message, 'r')}help` to get a list of commands!\nType"
                                   f"`{await determine_prefix(self.bot, message, 'r')}info` to get some info about me and my creator!")

    #-------------ON ERROR-----------#
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Please use all required arguments!")
            return
        elif "403" in str(error):
            try:
                await ctx.send(  # TODO: Figure out which permissions are missing
                    f"Looks like i'm missing a permission, make sure you invited me with the right permissions integer and selected all the parts!\n"
                    f"If you think you removed some permissions, you can re-invite me by running"
                    f"the `{await determine_prefix(self.bot, ctx, 'r')}invite` command.\n(make sure to kick me before you re-invite me!)")
            except discord.errors.Forbidden:
                pass
            return

        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("That's not a valid member!")
            return

        await ctx.send("This command gave an error, it has been reported!")
        await self.bot.errchannel.send(f"Hey <@{config['BOTOWNER']}>, there was an error!\n```\n{error}\n```")
        raise error

    #------ON JOIN---------#
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined the guild '{guild.name}'")
        Settings(guild.id)
        for channel in guild.text_channels:
            try:
                await channel.send(
                    f"Hey, thanks for inviting me!\nMy default prefix is `{config['PREFIX']}`, but you can also just mention me (`@JoyBot#7306 `)\n\n"
                    f"If you'd like, you can also change my prefix by using this command: `{config['PREFIX']}changesetting prefix <the prefix you want>`"
                    )
            except discord.errors.Forbidden:
                pass
            else:
                breakp

    #----------ON BOT READY---------#
    @commands.Cog.listener()
    async def on_ready(self):
        while self.bot is None:
            pass
        await self.bot.change_presence(activity=discord.Game("Just JoyBot things :)"))
        print(f"Logged in as the bot ({self.bot.user})!")

        errguild = self.bot.get_guild(config["ERRORDATA"][0])
        self.bot.errchannel = errguild.get_channel(config["ERRORDATA"][1])
        del errguild


def setup(bot):
    bot.add_cog(_important(bot))
