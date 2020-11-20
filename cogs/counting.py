# --------------------------JoyBot - Python Branch-------------------------#
# --------------------------------Counting---------------------------------#

import os
import discord
from discord.ext import commands

from data.bot.bot_functions import guild_settings, counting_channel, determine_prefix
from data.bot.bot_config import config


# TODO: check if user edits message in counting channel

# ---------------------------------Code------------------------------------#

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        total_guilds = 0
        total_counts = 0
        client.countDict = {}
        for guildid in os.listdir("./data"):
            if len(guildid) != 18:
                continue
            try:
                with open(f"./data/{guildid}/count.txt", 'r') as fp:
                    try:
                        amount = int(fp.read())
                    except ValueError:
                        if fp.read() == "":
                            os.remove(f"./data/{guildid}/count.txt")
                            continue
                    client.countDict[str(guildid)] = amount
                    total_guilds += 1
                    total_counts += amount
            except FileNotFoundError:
                continue

        print(f"Loaded {total_counts} counts from {total_guilds} guilds")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.id == config["BOTID"]:
            return
        cursettings = await guild_settings(message.guild.id, message.channel, "counting_channel")
        if cursettings is None or cursettings != message.channel.id:
            return

        try:
            if not message.content.isnumeric():
                await message.delete()
                await message.author.send("That's not a number!")
                return

            curnum = await counting_channel(self.client, "get_val", message.guild.id)
            try:
                if int(message.content) != curnum+1:
                    await message.delete()
                    await message.author.send(f"That's not the next number!\nHint: it's `{curnum+1}`!")
                    return
            except ValueError:
                await message.delete()
                await message.author.send("That's not a number!")
                return

            lastid = await counting_channel(self.client, "get_id", message.guild.id)
            if lastid == message.author.id:
                await message.delete()
                await message.author.send("You can't count twice in a row!")
                return

            await counting_channel(self.client, "add", message.guild.id, 1, message.author.id, channel=message.channel)
        except discord.errors.HTTPException:
            return

def setup(client):
    client.add_cog(Counting(client))
