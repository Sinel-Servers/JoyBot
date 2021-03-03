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


from discord.ext import commands
from discord import Embed
from subprocess import check_output
import discordlists


class DiscordListsPost(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = discordlists.Client(self.bot)  # Create a Client instance

        auth_pairs = {
            "arcane-center.xyz": "jTlQ8825YS1rl9IH3ctW4J8axCRFkKLPHq213wlGJF0xc2e6oGO3ifl07w26AMlt",
            "bladebotlist.xyz": "LkffKeAFMHl9SnC.pMglwnI0cr8zr6s.qpKOVTNVrPnKeai",
            "discord-botlist.eu": "cu3v3qNgbpTKA1hwOSW9Aq3baMK6ZDXhtCmdL2C9hQ350ZUMKLcynZdKRdVZcYnfEr63hDrkdVVbAkuvOIQYa0",
            "discord.boats": "w8ssoBDS0WRszj0w8jELiAxqmJsfeOME5KiptvNzSNI6lQSMPzA2LN9PGhRP93UxGxLJzSGrDV5DUMgwVwGLq16lct0my4bvNv45sor4x2PtOve4r1BQmNugUKJlMNLDUG0SxkudifYv9imC3tTuX7IYDt6",
            "discord.bots.gg": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiMjQ2ODYyMTIzMzI4NzMzMTg2IiwiaWF0IjoxNjEwMzM5NTc1fQ.7waAj2-fluh9iKquWK8-b2yKknXAxEq0PGW18LQL9js",
            "discordbotdirectory.net": "PV0lH4vDMBWmPKAO1wCR",
            "discordbotlist.com": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjUwNDAzMDcwMzI2NDk4OTE5NCIsImlhdCI6MTYxMDMzOTgxOX0.sPsgz79tHl7QGT6SVWPIdsTjuIXFLrsoGneRiGvufYo",
            "discordbots.co": "c6c4472e4be247df5fdcf2122f28af303e0d14a896b829c26c635dcf2c61272981634829760b0f9c",
            "discordextremelist.xyz": "DELAPI_24c5a1cd025a8785cf50723f57bb95c6-504030703264989194",
            "discordlistology.com": "41bdd206a569e31dd36a51fe8952afe3b5c9b0e976ebf473da908cc58e7bf16a01260011fddc9b50706fb2b82b3bb5c6c84f626cf1ff33b3f587149bbdaa958145cc67e54743d68b5eefe7c1a09503a26176b1a7d96222a381685dc8dbae0e33197d9c83c6f7821e25b1b1ecce67be1df4822f9171491ba7dcfd1fe3fb85effa7b7bacd98a6bbb7088ec06b6c1ee77c750c61e64f0605d57c65be8ef5a4d5b0b1aab78773763b7920f21ef867638299ad0c5d1eba1a188e1df9bc8596ccf965e8cf024d59c7fa2c45973851b7e30b8a6fb8b0cbf66413bf92889ad501b42e2f52e8d08bd0994932f7f94cb91a60496ef073cc5a44e1e8f823fbd9119ebade3af27149012a835a4360076bfcb32f70826f90477132f2c5ae45c7230a33a850b3280d415422f525ac4c81ce9c982d8c815562acafb55b1b22d58f38e42ce2fdd1393fa71f12926dd5d0c19a1973f458e1b6f50df75a98511cd4ec3c2f18cb2d722602437768119701b2f5d9c71e0ffd15ef70e344ecc201e8a90a3f8c18f67909b451610c39c30e35acc7b5236c1f5648042378448dc53c2048b7cf6a37979ba090bf6b94298bec81eda27d8d734f94552f565fc4e5125768319860e9a692106745c08836d2b5ce747",
            "voidbots.net": "uJ8ri92QcgzetEt28HRPd9aGF58VcIethl5lvl3xHKjo",
            "top.gg": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUwNDAzMDcwMzI2NDk4OTE5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEzOTg3NjY2fQ.dcQOsWqONzwodCVNUC96FqImX0tTKT3Y3Av9nuufrFs"
        }

        for key in auth_pairs:
            self.api.set_auth(key, auth_pairs[key])

        self.api.start_loop()  # Posts the server count automatically every 30 minutes

    @commands.command()
    async def post(self, ctx: commands.Context):
        """
        Manually posts guild count using discordlists.py (BotBlock)
        """
        msg = await ctx.send("Posting server count...")
        try:
            result = await self.api.post_count()
        except Exception as e:
            await ctx.send(f"Request failed: `{e}`")
            return

        await msg.edit(content="Successfully manually posted server count ({:,}) to {:,} lists."
                       "\nFailed to post server count to {:,} lists.".format(self.api.server_count,
                                                                             len(result["success"].keys()),
                                                                             len(result["failure"].keys())))

    @commands.command()
    async def stats(self, ctx: commands.Context):
        cpuusage = [area for area in check_output(["mpstat"]).decode("utf-8").split("\n")[3].split(" ") if area]
        cpuusage = str(cpuusage[2]) + "%"

        memusage = [area for area in check_output(["free"]).decode("utf-8").split("\n")[1].split(" ") if area]
        memusage_free = str(round(int(memusage[-1]) / (1000 * 1000), 2))
        memusage_total = str(round(int(memusage[1]) / (1000 * 1000), 2))
        memusage_usage = str(float(memusage_total) - float(memusage_free))

        e = Embed()
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.title = "Stats for JoyBot"
        e.description = "These are the stats for JoyBot"
        e.add_field(name="Memory", value=f"Total: `{memusage_total}GB`\nUsage: `{memusage_usage}GB`\nFree: `{memusage_free}GB`", inline=False)
        e.add_field(name="CPU", value=f"Usage: {cpuusage}", inline=False)
        e.add_field(name="Guilds", value=f"Guilds: `{len(self.bot.guilds)}`\nShards: `{self.bot.shard_count}`\nPing: `{round(self.bot.latency * 1000)}ms`", inline=False)

        await ctx.send("\u200e", embed=e)


def setup(bot):
    bot.add_cog(DiscordListsPost(bot))
