# --------------------------JoyBot - Python Branch-------------------------#
# ---------------------------------Faces-----------------------------------#

import discord
import json
import os
import random

from discord.ext import commands

from data.bot.bot_config import config
from data.bot.bot_functions import format_member_pretty, guild_settings, determine_prefix


# ---------------------------------Code------------------------------------#

class Faces(commands.Cog):
    def __init__(self, client):
        total_guilds = 0
        total_people = 0
        total_faces = 0
        self.client = client
        client.facesDict = {}
        for guildid in os.listdir("./data"):
            if len(guildid) != 18:
                continue
            try:
                with open(f"./data/{guildid}/faces.json", 'r') as fp:
                    client.facesDict[str(guildid)] = json.load(fp)
                    total_guilds += 1
                    total_people += len(self.client.facesDict[str(guildid)])
                    for person in list(self.client.facesDict[str(guildid)].keys()):
                        total_faces += len(self.client.facesDict[str(guildid)][person])
            except FileNotFoundError:
                continue

        print(f"Loaded {total_faces} faces from {total_people} people from {total_guilds} guilds")

    @commands.command()
    async def randomface(self, ctx, member: discord.Member = None):
        try:
            guild_faces = self.client.facesDict[str(ctx.guild.id)]
        except KeyError:
            await ctx.send("This guild doesn't have any faces, ask an admin to add some!")
            return
        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.client, ctx, 'r')}help randomface` if you're stuck!")
            return
        try:
            chosen_face_id = random.choice(list(guild_faces[str(member.id)].keys()))
            chosen_face = guild_faces[str(member.id)][chosen_face_id]
        except KeyError:
            await ctx.send(f"This person doesn't have any faces!")
            return

        e = discord.Embed(title=f"Random face from {await format_member_pretty(member)}", description=f"Picture ID: `{chosen_face_id}`")
        e.set_footer(text=f"Requested by {await format_member_pretty(ctx.author)} ({ctx.author.id})")
        e.set_image(url=chosen_face)

        await ctx.send(embed=e)

    @commands.command()
    async def addface(self, ctx, member: discord.Member = None):
        if ctx.author.id not in config["SUPERADMINIDS"] and not ctx.author.guild_permissions.administrator and ctx.author.id not in await guild_settings(ctx.guild.id, ctx, "adminslist"):
            await ctx.send("You're not an admin!")
            return

        try:
            guild_faces = self.client.facesDict[str(ctx.guild.id)]
        except KeyError:
            guild_faces = {}

        if member is None:
            await ctx.send(f"Please use the proper usage!\nType `{await determine_prefix(self.client, ctx, 'r')}help randomface` if you're stuck!")
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
            await ctx.send(f"Added `{await format_member_pretty(member)}`'s picture number `{toadd}`!")

        else:
            guild_faces[str(member.id)] = {}
            guild_faces[str(member.id)]["1"] = file.url
            await ctx.send(f"Added `{await format_member_pretty(member)}`'s first picture!")

        self.client.facesDict[str(ctx.guild.id)] = guild_faces
        try:
            with open(f"./data/{ctx.guild.id}/faces.json", "w") as fp:
                json.dump(self.client.facesDict[str(ctx.guild.id)], fp)
        except FileNotFoundError:
            os.mkdir(f"./data/{ctx.guild.id}/")
            with open(f"./data/{ctx.guild.id}/faces.json", "w") as fp:
                json.dump(self.client.facesDict[str(ctx.guild.id)], fp)


def setup(client):
    client.add_cog(Faces(client))
