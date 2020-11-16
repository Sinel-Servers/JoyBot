# --------------------------JoyBot - Python Branch-------------------------#
# --------------------------------Settings---------------------------------#

import os
from discord.ext import commands
from data.bot.bot_functions import guild_settings, get_id_mention, text_pretty_mid_end, gen_settings, \
                                   format_member_pretty, get_id_channel, counting_channel
from data.bot.bot_config import config


# ---------------------------------Code------------------------------------#

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def listsettings(self, ctx):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator:
            await ctx.send("Hey, you can't use this command!")
            return

        settings = await guild_settings(ctx.guild.id, ctx)
        if not settings:
            await gen_settings(ctx.guild.id)

        sendstring = ""
        for setting in list(settings.keys()):
            sendstring += f"{await text_pretty_mid_end(setting, settings[setting])}\n"

        await ctx.send(f"Here are the settings:```\n{sendstring}```")

    @commands.command()
    async def changesetting(self, ctx, setting, value=None):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator:
            await ctx.send("Hey, you can't use this command!")
            return

        if setting == "admins_list":
            if value is None:
                await ctx.send("Please use this command with a mention!")
                return

            user = self.client.get_user(await get_id_mention(value))
            if user is None:
                await ctx.send("Please use this command with a mention!")
                return

            curadmins = await guild_settings(ctx.guild.id, ctx, "admins_list")

            if user.id in curadmins:
                curadmins.remove(user.id)
                await ctx.send(f"Removed {await format_member_pretty(user)} from the admins list")
                await guild_settings(ctx.guild.id, ctx, "admins_list", curadmins)
                return

            curadmins.append(user.id)
            await guild_settings(ctx.guild.id, ctx, "admins_list", curadmins)
            await ctx.send(f"Added {await format_member_pretty(user)} to the admins list")
            return

        elif setting == "global_randomface":
            curface = await guild_settings(ctx.guild.id, ctx, "global_randomface")
            if curface is False:
                await guild_settings(ctx.guild.id, ctx, "global_randomface", True)
                await ctx.send("Made randomface get pictures from everyone")
                return
            else:
                await guild_settings(ctx.guild.id, ctx, "randomface_global", False)
                await ctx.send("Made randomface get pictures from the specified user")
                return

        elif setting == "global_addface":
            curface = await guild_settings(ctx.guild.id, ctx, "global_addface")
            if curface is False:
                await guild_settings(ctx.guild.id, ctx, "global_addface", True)
                await ctx.send("Made addface usable by anyone")
                return
            else:
                await guild_settings(ctx.guild.id, ctx, "global_addface", False)
                await ctx.send("Made addface admins only")
                return

        elif setting == "counting_channel":
            channel_id = await get_id_channel(value)
            if value is None:
                cursetting = await guild_settings(ctx.guild.id, ctx, "counting_channel")
                if cursetting is None:
                    await ctx.send("The setting is already reset!")
                    return
                curnum = await counting_channel(self.client, "get_val", ctx.guild.id)
                await guild_settings(ctx.guild.id, ctx, "counting_channel", "None")
                channel = self.client.get_channel(cursetting)
                await channel.send(f"The counting is over! You got to a total of `{curnum}`!\n——————————")
                await ctx.send("Reset the counting channel setting!")
                return

            channel = self.client.get_channel(channel_id)
            if channel is None:
                await ctx.send("That's not a valid channel in this guild!")
                return

            try:
                os.remove(f"./data/{ctx.guild.id}/count.txt")
            except FileNotFoundError:
                pass
            try:
                os.remove(f"./data/{ctx.guild.id}/count_id.txt")
            except FileNotFoundError:
                pass

            await guild_settings(ctx.guild.id, ctx, "counting_channel", channel_id)
            await channel.send("——————————\nThis channel has been set up as the counting channel! It starts from 0!\nHere, i'll go first:")
            await channel.send("0")
            await counting_channel(self.client, "set", ctx.guild.id, 0, "", channel=channel)
            await ctx.send("Counting channel is set up!")

        else:
            await ctx.send(f"That's not a valid setting, you can use `{config['PREFIX']}listsettings` to get the settings list.")


def setup(client):
    client.add_cog(Settings(client))
