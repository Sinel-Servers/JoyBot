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


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.custom_prefixes = {}


    @client.command
    async def prefix(self, ctx, prefix):
    	if not ctx.author.guild_permissions.administrator or not ctx.author.id in config["SUPERADMINIDS"] or not ctx.author.id in await guild_settings(ctx.guild.id, "adminslist"):

    
def setup(client):
    client.add_cog(Prefix(client))
