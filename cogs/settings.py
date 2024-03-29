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


from discord.ext import commands

from classes.errors import UnauthorizedUserException
from functions import text_pretty_mid_end, determine_prefix
from classes.database.guild import Settings as Sttngs
from classes.database.guild import Counting
from classes.get_id import get_id
from config import config


# ---------------------------------Code------------------------------------#

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def listsettings(self, ctx: commands.Context):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator:
            raise UnauthorizedUserException

        settings = Sttngs(ctx.guild.id)
        cur_settings = settings.get_all_settings()

        sendstring = ""
        for setting in cur_settings:
            sendstring += f"{await text_pretty_mid_end(setting, cur_settings[setting])}\n"

        counting_channel = Counting(ctx.guild.id).channel_get_id()
        sendstring += f"{await text_pretty_mid_end('counting_channel', str(counting_channel))}\n"

        await ctx.send(f"Here are the settings:```\n{sendstring}```")

    @commands.command()
    async def changesetting(self, ctx: commands.Context, setting_name: str, setting_value=None):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator:
            raise UnauthorizedUserException

        settings = Sttngs(ctx.guild.id)

        if setting_name == "admins_list":
            if setting_value is None:
                await ctx.send("Please use this command with a mention!")
                return

            user = self.bot.get_user(await get_id().member(setting_value))
            if user is None:
                await ctx.send("Please use this command with a mention!")
                return

            admins_list = settings.get_setting("admins_list")

            if user.id in admins_list:
                admins_list.remove(user.id)
                await ctx.send(f"Removed {user} from the admins list")
                settings.set_setting("admins_list", admins_list)
                return

            admins_list.append(user.id)
            settings.set_setting("admins_list", admins_list)
            await ctx.send(f"Added {user} to the admins list")
            return

        elif setting_name == "global_randompic":
            global_randompic = settings.get_setting("global_randompic")
            if global_randompic == "False":
                settings.set_setting("global_randompic", "True")
                await ctx.send("Made randompic get pictures from everyone")
                return
            else:
                settings.set_setting("global_randompic", "False")
                await ctx.send("Made randompic get pictures from the specified user")
                return

        elif setting_name == "global_addpic":
            global_addpic = settings.get_setting("global_addpic")
            if global_addpic == "False":
                settings.set_setting("global_addpic", "True")
                await ctx.send("Made addpic usable by anyone")
                return
            else:
                settings.set_setting("global_addpic", "False")
                await ctx.send("Made addpic admins only")
                return

        elif setting_name == "counting_channel":
            if setting_value is None:
                counting_channel = settings.get_setting("counting_channel")
                if counting_channel is None:
                    await ctx.send("The setting_name is already reset!")
                    return

                counting = Counting(ctx.guild.id)

                curnum = counting.get()
                settings.set_setting("counting_channel", "None")
                channel = self.bot.get_channel(counting_channel)
                await channel.send(f"The counting is over! You got to a total of `{curnum}`!\n——————————")
                await ctx.send("Reset the counting channel setting_name!")
                return

            counting_channel = await get_id().channel(setting_value)
            channel = self.bot.get_channel(counting_channel)
            if channel is None:
                await ctx.send("That's not a valid channel in this guild!")
                return

            settings.set_setting("counting_channel", counting_channel)

            await channel.send("——————————\nThis channel has been set up as the counting channel! It starts from 0!\nHere, i'll go first:")
            await channel.send("0")
            Counting(ctx.guild.id).channel_set(counting_channel)
            await ctx.send("Counting channel is set up!")

        elif setting_name == "prefix":
            if not ctx.author.guild_permissions.administrator or ctx.author.id not in config["SUPERADMINIDS"]:
                pass

            if setting_value is None:
                await ctx.send("Please specify what the new prefix is!")
                return

            if len(setting_value) > 10:
                await ctx.send("Please keep the prefix under 10 characters!")
                return

            settings.set_setting("prefix", setting_value)
            await ctx.send("Successfully set the new prefix!")

        else:
            await ctx.send(f"That's not a valid setting, you can use `{await determine_prefix(self.bot, ctx, True)}listsettings` to get the settings list.")


def setup(bot):
    bot.add_cog(Settings(bot))
