# --------------------------JoyBot - Python Branch------------------------- #
# ---------------------------------Other----------------------------------- #

import re
import os
import sys
import shutil
import discord
from discord.ext import commands
from data.bot.bot_config import config
from data.bot.bot_functions import function_backwords, spacify_function, random_gif, inch_cm, message_data_mod, determine_prefix


# ---------------------------------Code------------------------------------ #


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def backwords(self, ctx, *, text):
        convert = await function_backwords(text)
        if convert != "":
            await ctx.send(f"{ctx.author.mention}, here is your backwords string: {convert}")
        else:
            await ctx.send(f"{ctx.author.mention}, please provide something to return backwords!")

    @commands.command()
    async def reversecaps(self, ctx, *, text=None):
        if text is None:
            await ctx.send(f"{ctx.author.mention}, please suppy an argument to reversecaps!")
            return

        await ctx.send(f"{ctx.author.mention}, here is your reversecaps:\n{text.swapcase()}")

    @commands.command()
    async def convert(self, ctx, text=None):
        if text is None:
            await ctx.send(
                f"Please convert either:\nFeet'inches to CM `{await determine_prefix(self.client, ctx, 'r')}convert 6'2`\nCM to Feet'inches `{await determine_prefix(self.client, ctx, 'r')}convert 188`\nMetres to CM `{await determine_prefix(self.client, ctx, 'r')}convert 1.88`")
            return

        convert = await inch_cm(text)
        if convert is not False:
            await ctx.send(f"{ctx.author.mention}, here is your conversion: {convert}")
        else:
            await ctx.send(f"{ctx.author.mention}, that's not a valid conversion!")

    @commands.command()
    async def spacify(self, ctx, *, text):
        spacedText = await spacify_function(text)
        await ctx.send(f"{ctx.author.mention}, here is your message:\n{spacedText}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        msgmod = await message_data_mod(self.client, "remove", reaction.user_id, reaction.message_id)
        try:
            if msgmod[0] == "guild ban":
                if reaction.user_id not in config["SUPERADMINIDS"]:
                    await message_data_mod(self.client, "add", reaction.user_id, reaction.message_id, ("guild ban", msgmod[0][1]))
                    return

                ctx_guild = self.client.get_guild(reaction.guild_id)
                ctx_channel = ctx_guild.get_channel(reaction.channel_id)
                if str(reaction.emoji) == config["CHAR_TICK"]:
                    msg = await ctx_channel.send("Deleting all data for that guild...")
                    try:
                        shutil.copytree(f"./data/{msgmod[1]}", f"./data/backups/{msgmod[1]}")
                    except FileExistsError:
                        shutil.rmtree(f"./data/backups/{msgmod[1]}")
                        shutil.copytree(f"./data/{msgmod[1]}", f"./data/backups/{msgmod[1]}")
                    shutil.rmtree(f"./data/{msgmod[1]}")
                    await msg.edit(content="All data has been deleted, and they have been blacklisted.")
                elif str(reaction.emoji) == config["CHAR_CROSS"]:
                    await ctx_channel.send("Cancelled server deletion")

        except TypeError:
            return

    @commands.command()
    async def guildban(self, ctx, guild_id=None):
        if ctx.author.id not in config["SUPERADMINIDS"]:
            await ctx.send("You can't use this command!")
            return
        if guild_id is None:
            await ctx.send(f"Please use this command with a guild id!\nExample: `{await determine_prefix(self.client, ctx, 'r')}guildban 753463761704321034`")
            return
        elif re.match(r"[0-9]{18}?", guild_id) is None:
            await ctx.send("That's not a valid guild!")
            return
        elif guild_id not in os.listdir("./data"):
            await ctx.send("I have no data on that guild!")
            return
        guild = self.client.get_guild(int(guild_id))
        if guild is None:
            msg = await ctx.send("Seems this guild was deleted!\nWould you like to remove it's data?")
            await message_data_mod(self.client, "add", ctx.author.id, msg.id, ("guild ban", guild_id))
            await msg.add_reaction(config["CHAR_TICK"])
            await msg.add_reaction(config["CHAR_CROSS"])
            return

        msg = await ctx.send(f"Are you sure you want to remove all the guild data for `{guild.name}`?")
        await message_data_mod(self.client, "add", ctx.author.id, msg.id, ("guild ban", guild_id))
        await msg.add_reaction(config["CHAR_TICK"])
        await msg.add_reaction(config["CHAR_CROSS"])

    @commands.command()
    async def invite(self, ctx):
        # link = f"https://discord.com/api/oauth2/authorize?client_id={config['BOTID']}&permissions={config['PERMINT']}&scope=bot"
        link = "https://sinelservers.xyz/stuff-made/JoyBot/invite.php"
        await ctx.send(f"{ctx.author.mention}, here's an invite link to add JoyBot to your own server:\n{link}")

    @commands.command()
    async def info(self, ctx):
        blurb = f"""
Hey, i'm JoyBot! I was made by Joyte as a small project, and am currently just maintained and worked on by him!
I like long walks on the beach and watching the sunset :)

If you ever need help, just use the `{await determine_prefix(self.client, ctx, 'r')}help` command, and i'll answer any and all questions you have!
If you've got a more serious problem with me, you can always visit my discord at https://sinelservers.xyz/discord.php where you can ask more in depth questions or report that there's something wrong with me
You can also make suggestions which you'd like added (although keep in mind my creator is just one person and is busy with school and other life-related things)

Hope you enjoy using me!
- JoyBot
        """
        await ctx.send(blurb)


def setup(client):
    client.add_cog(Other(client))
