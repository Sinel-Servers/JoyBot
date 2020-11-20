# --------------------------JoyBot - Python Branch------------------------- #
# ---------------------------------Bump------------------------------------ #

import discord
import json
import os

from discord.ext import commands
from data.bot.bot_functions import string_pop, get_top_dict, bump_total_mod, get_id_mention, format_member_pretty, determine_prefix
from data.bot.bot_config import config


# ---------------------------------Code------------------------------------ #

class Bump(commands.Cog):
    def __init__(self, client):
        total_guilds = 0
        total_people = 0
        total_bumps = 0
        self.client = client
        self.client.bumpDict = {}
        for guildid in os.listdir("./data"):
            if len(guildid) != 18:
                continue
            try:
                with open(f"./data/{guildid}/bumptotals.json", 'r') as fp:
                    client.bumpDict[str(guildid)] = json.load(fp)
                    total_guilds += 1
                    total_people += len(self.client.bumpDict[str(guildid)])
                    for person in list(self.client.bumpDict[str(guildid)].keys()):
                        total_bumps += self.client.bumpDict[str(guildid)][person]
            except FileNotFoundError:
                continue

        print(f"Loaded {total_bumps} bumps from {total_people} people from {total_guilds} guilds")

    @commands.Cog.listener()
    async def on_message(self, message):
        firstbump = False
        if message.author.id == config['DISBOARDID']:
            for embed in message.embeds:
                if "Bump done" in embed.description:
                    bumpID = await get_id_mention(embed.description)

                    try:
                        oldtop = str(await get_top_dict(self.client.bumpDict[str(message.guild.id)], 1, "raw"))
                        if oldtop is None:
                            raise KeyError
                    except KeyError:
                        firstbump = True
                        oldtop = 0

                    await bump_total_mod(self.client, "add", str(bumpID), str(message.guild.id), 1)
                    top = str(await get_top_dict(self.client.bumpDict[str(message.guild.id)], 1, "raw"))

                    send_msg = f"<@{bumpID}>, your bump total has been increased by one!\nType `.bumptotal` to view your current bump total!"
                    if not firstbump:
                        if oldtop != top:
                            send_msg += "\nYou also managed to get the top spot! Nice!"

                            try:
                                with open(f"./data/{message.guild.id}/roletop.txt", 'r') as fp:
                                    oldID = int(fp.read().replace('\n', ''))
                                skip = False

                            except FileNotFoundError:
                                skip = True
                                oldID = 0

                            with open(f"./data/{message.guild.id}/roletop.txt", "w") as fp:
                                fp.write(str(bumpID))

                            if not skip:
                                oldMember = message.guild.get_member(int(oldID))
                                try:
                                    send_msg += f"\n\n{oldMember.mention}, you've lost your top spot!"
                                except AttributeError:
                                    print(f"Top spot error, here's the deets:\nOldMember object: {oldMember}\nBumpID: {bumpID}\noldtop: {oldtop}\ntop: {top}\noldid: {oldID}\nbumpID: {bumpID}")
                    else:
                        send_msg += "\n\nYou were also the first to bump the server. Congrats!"

                    await message.channel.send(send_msg)

    @commands.command()
    async def bumptotal(self, ctx, person: discord.Member = None):
        if person is None or person.id == ctx.author.id:
            curScore = await bump_total_mod(self.client, "one", ctx.author.id, ctx.guild.id)

            if curScore == 0:
                await ctx.send("You haven't bumped disboard yet")
            else:
                await ctx.send(f"Here is your total times bumped: `{curScore}`")

        else:
            curScore = await bump_total_mod(self.client, "one", person.id, ctx.guild.id)

            if curScore == 0:
                await ctx.send(f"{person} hasn't bumped disboard yet!")
            else:
                await ctx.send(f"{person} has bumped disboard `{curScore}` times")

    @commands.command()
    async def topbumptotal(self, ctx):
        try:
            topbumps = await get_top_dict(self.client.bumpDict[str(ctx.guild.id)], 10)
        except KeyError:
            await ctx.send(content=f"{ctx.author.mention}, looks like nobody has bumped disboard yet")
            return
        printstring = ""

        message = await ctx.send("Getting the top 10 total times bumped...")

        for num, raw_bumpID_bumpTotal in enumerate(topbumps):
            user = await self.client.fetch_user(raw_bumpID_bumpTotal[0])
            username = f"{user.name}#{user.discriminator}"

            endstring = ""
            for funny in config['BUMP_FUNNIES']:
                if raw_bumpID_bumpTotal[1] == funny[0]:
                    endstring = f" — {funny[1]}"

            else:
                if num >= 9:
                    printstring += f"{num + 1})   {username} — {raw_bumpID_bumpTotal[1]}{endstring}\n"
                else:
                    printstring += f"{num + 1})    {username} — {raw_bumpID_bumpTotal[1]}{endstring}\n"

        await message.edit(
            content=f"{ctx.author.mention}, here are the top 10 total times bumped:\n```{printstring}```")

    @commands.command()
    async def changebumptotal(self, ctx, person: discord.Member = None, amount=None):
        if ctx.author.id not in config["SUPERADMINIDS"]:
            await ctx.send(f"{ctx.author.mention}, you can't use this command!")
            return

        if person is None:
            await ctx.send(f"{ctx.author.mention}, Please supply a person!")
            return

        if amount is None:
            await ctx.send(f"{ctx.author.mention}, Please supply an amount to change by!")
            return

        if person.id == ctx.author.id:
            person_name = "your"
            person_id = ctx.author.id
        else:
            person_name = f"{await format_member_pretty(person)}'s"
            person_id = person.id

        if str(amount)[0] == "-":
            amount = await string_pop(amount, 0)
            if amount.isnumeric():
                await bump_total_mod(self.client, "minus", person_id, ctx.guild.id, int(amount))
                await ctx.send(f"Changed {person_name} bump total by -{amount}")
            else:
                await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")
        else:
            if amount.isnumeric():
                await bump_total_mod(self.client, "add", person_id, ctx.guild.id, int(amount))
                await ctx.send(f"Changed {person_name} bump total by {amount}")
            else:
                await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")


def setup(client):
    client.add_cog(Bump(client))
