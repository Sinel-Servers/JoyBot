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

import re
from discord.ext import commands
import discord
from config import config
from classes.database.message import Message
from classes.exceptions import AlreadyBannedError, NoDataError
from classes.database.guild import Bump, Pictures, Settings, Counting, Ban
from functions import inch_cm, determine_prefix

# ---------------------------------Code------------------------------------ #


class Other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def backwords(self, ctx: commands.Context, *, text: str = None):
        if text is None:
            await ctx.send(f"{ctx.author.mention}, please suppy an argument to backwords!")
            return
        text = f"{ctx.author.mention}, here's your backwords string: {text[::-1]}" if text != "" else f"{ctx.author.mention}, please provide something to return backwords!"
        await ctx.send(text)

    @commands.command()
    async def reversecaps(self, ctx: commands.Context, *, text: str = None):
        if text is None:
            await ctx.send(f"{ctx.author.mention}, please suppy an argument to reversecaps!")
            return

        await ctx.send(f"{ctx.author.mention}, here is your reversecaps:\n{text.swapcase()}")

    @commands.command()
    async def convert(self, ctx: commands.Context, text: str = None):
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
    async def spacify(self, ctx: commands.Context, *, text: str = None):
        if text is None:
            await ctx.send(f"{ctx.author.mention}, please suppy an argument to spacify!")
            return
        text = list(text)
        text = " ".join(text)
        await ctx.send(f"{ctx.author.mention}, here is your message:\n{text}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        # TODO: Switch to using wait_for
        #       https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for
        messagedb = Message(reaction.user_id, reaction.message_id)
        try:
            msgmod = messagedb.get()
        except NoDataError:
            return
        try:
            if msgmod[0] == "guild ban":
                guild = self.bot.get_guild(reaction.guild_id)
                channel = guild.get_channel(reaction.channel_id)
                msg = await channel.fetch_message(msgmod[1])
                if str(reaction.emoji) == config["CHAR_TICK"]:
                    previous_content = msg.content
                    await msg.edit(content=f"~~{previous_content}~~\nDeleting all data for that guild...")
                    Bump(msgmod[2]).reset_guild_total()
                    Settings(msgmod[2]).reset_settings(False)
                    Pictures(msgmod[2]).delete_all()
                    Counting(msgmod[2]).reset()

                    try:
                        Ban(msgmod[2]).ban()
                    except AlreadyBannedError:
                        pass
                    previous_content = msg.content.split("\n")
                    previous_content[1] = f"~~{previous_content[1]}"
                    previous_content = "\n".join(previous_content)
                    await msg.edit(content=f"{previous_content}~~\nAll data has been deleted, and the guild has been banned!")
                    await msg.clear_reactions()
                    messagedb.remove()

                elif str(reaction.emoji) == config["CHAR_CROSS"]:
                    previous_content = msg.content
                    await msg.edit(content=f"~~{previous_content}~~\nCancelled server ban")
                    await msg.clear_reactions()
                    messagedb.remove()

            elif msgmod == "delete":
                if str(reaction.emoji) == config["CHAR_CROSS"]:
                    ctx_guild = self.bot.get_guild(reaction.guild_id)
                    ctx_channel = ctx_guild.get_channel(reaction.channel_id)
                    message = await ctx_channel.fetch_message(reaction.message_id)
                    await message.delete()
                    messagedb.remove()

        except TypeError:
            return

    @commands.command()
    async def guildban(self, ctx: commands.Context, guild_id: int = None):
        # TODO: Switch to using wait_for
        #       https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.wait_for

        if ctx.author.id not in config["SUPERADMINIDS"]:
            await ctx.send("You can't use this command!")
            return
        if guild_id is None:
            await ctx.send(f"Please use this command with a guild id!\nExample: `{await determine_prefix(self.bot, ctx, True)}guildban 753463761704321034`")
            return
        elif re.match(r"[0-9]{18}?", str(guild_id)) is None:
            await ctx.send("That's not a valid guild!")
            return

        guild_ids = [guild.id for guild in self.bot.guilds]

        if guild_id not in guild_ids:
            await ctx.send("I have no data on that guild!")
            return

        guild = self.bot.get_guild(guild_id)
        if guild is None:
            msg = await ctx.send("Seems this guild was deleted!\nWould you like to remove it's data?")
            Message(ctx.author.id, msg.id).add(("guild ban", msg.id, guild_id))
            await msg.add_reaction(config["CHAR_TICK"])
            await msg.add_reaction(config["CHAR_CROSS"])
            return

        msg = await ctx.send(f"Are you sure you want to remove all the guild data for `{guild.name}`?")
        Message(ctx.author.id, msg.id).add(("guild ban", msg.id, guild_id))
        await msg.add_reaction(config["CHAR_TICK"])
        await msg.add_reaction(config["CHAR_CROSS"])

    @commands.command()
    async def invite(self, ctx: commands.Context):
        e = discord.Embed()
        e.title = "Invite"
        e.description = """
            Oh, you want to add me? That's nice, here's an invite link to add JoyBot to your own server:
            [Just click here!](https://sinelservers.xyz/stuff-made/JoyBot/invite.php?utm_source=invite_cmd)
        """.replace("    ", "")
        await ctx.send(embed=e)

    @commands.command()
    async def info(self, ctx: commands.Context):
        e = discord.Embed()
        e.title = "Info"
        e.description = f"""
            Hey, i'm JoyBot! I was made by Joyte as a small project, and am currently just maintained and worked on by him!
            I like long walks on the beach and watching the sunset :)
            
            If you ever need help, just use the `{await determine_prefix(self.bot, ctx, True)}help` command, and i'll answer any and all questions you have!
            If you've got a more serious problem with me, you can always visit my discord [Right here](https://sinelservers.xyz/discord.php?utm_source=info_cmd) where you can ask more in depth questions or report that there's something wrong with me
            You can also make suggestions which you'd like added (although keep in mind my creator is just one person and is busy with school and other life-related things)
            
            Hope you enjoy using me!
            - JoyBot
        """.replace("    ", "")
        await ctx.send(embed=e)

    @commands.command()
    async def privacy(self, ctx: commands.Context):
        e = discord.Embed()
        e.title = "Privacy"
        e.description = """
            Hi, you're probably wondering what data we store on you, and that's okay! Everybody has a right to privacy. Check out our privacy policy here:
            https://sinelservers.xyz/stuff-made/JoyBot/privacy.php
        """.replace("    ", "")
        await ctx.send(embed=e)

    @commands.command()
    async def source(self, ctx: commands.Context):
        e = discord.Embed()
        e.title = "Source"
        e.description = """
            Ah okay, so you're wondering how i look like? Well, that's fine, just don't shame me i'm a bit messy 🥺
            https://github.com/Sinel-Servers-Limited/JoyBot
        """.replace("    ", "")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Other(bot))
