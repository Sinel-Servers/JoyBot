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

import discord
import traceback
import io
import contextlib	
from typing import Optional
from discord.ext import commands
from config import config


class evalClass(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["eval"])
	async def evaluate(self, ctx, awa: Optional[bool], *, code=None):
		if ctx.author.id not in config["SUPERADMINIDS"]:
			await ctx.send(f"{ctx.author.mention}, you can't use this command!")
			return
		if code is None:
			await ctx.send(f"Please supply some code!")
			return

		try:
			if awa:
				result = await eval(code)
			else:
				result = eval(code)
			if result == "":
				await ctx.send("No output")
			else:
				await ctx.send(result)
		except Exception as e:
			await ctx.send(f"Exception: `{e.__class__.__name__}: {e}`")

	@commands.command(aliases=["e", "exec"])
	async def execute(self, ctx, awa: Optional[bool], *, code=None):
		if ctx.author.id not in config["SUPERADMINIDS"]:
			await ctx.send(f"{ctx.author.mention}, you can't use this command!")
			return
		if code is None:
			await ctx.send(f"Please supply some code!")
			return

		str_obj = io.StringIO()  # Retrieves a stream of data
		try:
			with contextlib.redirect_stdout(str_obj):
				await exec(code) if awa else exec(code)
		except Exception as e:
			formatted_exception_list = traceback.format_exception(type(e), e, e.__traceback__)
			formatted_exception_list.pop(1)
			formatted_exception = ""
			for line in formatted_exception_list:
				formatted_exception += line
			return await ctx.send(f"{ctx.author.mention}, An exception occured!\n```{formatted_exception}```")
		if str_obj.getvalue() == "":
			await ctx.send(f'{ctx.author.mention}, the run completed succesfully with no output!')
		else:
			try:
				await ctx.send(f'{ctx.author.mention}, the run completed succesfully, heres the output:\n```{str_obj.getvalue()}```')
			except discord.errors.HTTPException:
				await ctx.send(f"{ctx.author.mention}, the run completed succesfully but the output was too long to send!")


def setup(bot):
	bot.add_cog(evalClass(bot))
