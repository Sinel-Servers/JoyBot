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

# ---------------------------------Main------------------------------------ #
# ---------------------------------Intro----------------------------------- #

# JoyBot! A bot managed by Joyte#0001,
# filled with different features and random
# things that I wanted to add to my friends' servers.
# Enjoy using it! If you need to contact me, you
# can use my discord id up there, or look at my
# contact page: https://sinelservers.xyz/contact.php

# ---------------------------------Code------------------------------------ #

from os import listdir, name, system, environ
from discord.errors import Forbidden
from discord.ext import commands
from discord import Message, AllowedMentions
from config import config
from functions import determine_prefix
from classes.database.guild import Counting, Ban, Bypass

# Enable colors on windows
if name == "nt":
    system("color")

# -----------------------Set up Variables--------------------- #

# Set up the bot object
bot = commands.AutoShardedBot(command_prefix=determine_prefix, allowed_mentions=AllowedMentions(roles=False, everyone=False), shard_count=2)

# Remove the help command, as we have our own custom one
bot.remove_command("help")


@bot.event
async def on_message(message: Message):
    try:
        if Ban(message.guild.id).is_banned():
            return
    except AttributeError:
        return

    if Counting(message.guild.id).channel_get_id() == message.channel.id:
        return

    if message.author.bot:
        return

    starts_with_prefix = any([message.content.startswith(prefix) for prefix in await determine_prefix(bot, message)])
    if not starts_with_prefix:
        return

    b = Bypass(message.guild.id)

    is_pb_command = any([message.content.startswith(prefix + "pb") for prefix in await determine_prefix(bot, message)])
    if is_pb_command:
        if message.author.permissions_in(message.channel).manage_guild or message.author.id in config["SUPERADMINIDS"]:
            try:
                await message.channel.send(f"Changed bypass status to `{b.change()}`")

            except Forbidden:
                await message.author.send(f"Changed bypass satus to `{b.is_bypassed}`\n\nCan you unmute me though :pleading_face:")

        else:
            try:
                await message.channel.send("You can't use this command!")

            except Forbidden:
                pass
        return

    # Check all permissions
    missing_perms = []

    permissions_list = [
        "send_messages",
        "read_messages",
        "manage_messages",
        "embed_links",
        "attach_files",
        "read_message_history",
        "add_reactions",
        "use_external_emojis"
    ]

    p = message.guild.me.permissions_in(message.channel)
    for perm in permissions_list:
        exec(f"if not p.{perm}:\n\tmissing_perms.append('{perm}')", locals())

    if not b.is_bypassed:
        if missing_perms:
            if not message.author.permissions_in(message.channel).manage_guild or message.author.id in config["SUPERADMINIDS"]:
                return

            perms_formatted = [f"• `{perm}`\n" for perm in missing_perms]

            if "send_messages" not in missing_perms:
                try:
                    await message.channel.send(f"I'm missing these permissions:\n{perms_formatted}\nPlease re-invite the bot and give it to me!\nYou may use the `{await determine_prefix(bot, message, True)}pb` command to bypass and ignore this message.")
                except Forbidden:
                    pass

            else:
                await message.author.send(f"I'm missing these permissions:\n{perms_formatted}\nPlease re-invite the bot and give it to me!\nYou may use the `{await determine_prefix(bot, message, True)}pb` command in your server to bypass and ignore this message.")

            return

    # All permissions good
    if b.is_bypassed:
        b.change()
    await bot.process_commands(message)


def main():
    print("Loading all cogs...")
    for filename in listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    print("Logging into discord...")
    bot.run(environ[config["TOKENVAR"]])


if __name__ == '__main__':
    main()
