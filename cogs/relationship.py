# --------------------------JoyBot - Python Branch------------------------- #
# ---------------------------------Other----------------------------------- #

import discord
from discord.ext import commands
from data.bot.bot_config import config
from data.bot.bot_functions import function_backwords, spacify_function, random_gif, inch_cm


# ---------------------------------Code------------------------------------ #


class Relationship(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kiss(self, ctx, person: discord.Member = None):
        if person is None:
            await ctx.send("I need to know who you are kissing!")
            return
        if person.id == ctx.author.id:
            await ctx.send("You can't kiss yourself!")
            return
        if person.id == config['BOTID']:
            await ctx.send("Awwh, i aprreciate you trying but i don't want you to freeze!")
            return
        if person.bot is True:
            await ctx.send("You can't kiss a bot, you'll get stuck to it! (we have no hearts, so we're very cold)")
            return

        gif_choice = await random_gif("kisses")
        fileName = f"./data/bot/pics/{gif_choice}"
        with open(fileName, 'rb') as fp:
            await ctx.send(f"{ctx.author.mention} has kissed {person.mention}", file=discord.File(fp, fileName))

    @commands.command()
    async def hug(self, ctx, person: discord.Member = None):
        if person is None:
            await ctx.send("I need to know who you are hugging!")
            return
        if person.id == ctx.author.id:
            await ctx.send("You can't hug yourself!")
            return
        if person.id == config['BOTID']:
            await ctx.send("Awwh, i aprreciate you trying but i don't want you to freeze!")
            return
        if person.bot is True:
            await ctx.send("You can't hug a bot, you'll get stuck to it! (we have no hearts, so we're very cold)")
            return

        gif_choice = await random_gif("hugs")
        fileName = f"./data/bot/pics/{gif_choice}"
        with open(fileName, 'rb') as fp:
            await ctx.send(f"{ctx.author.mention} has hugged {person.mention}", file=discord.File(fp, fileName))


def setup(client):
    client.add_cog(Relationship(client))
