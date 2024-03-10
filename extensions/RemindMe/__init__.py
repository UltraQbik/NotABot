"""
The extension to 'NotABot' discord not a bot client, which adds '!remindme' command.
"""

import discord
from discord.ext import commands
from discord import app_commands


class Cog(commands.Cog, name="RemindMe"):
    """
    This is the 'remind me' command cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="remindme",
        description="Reminds you"
    )
    @app_commands.describe(
        timestamp="Time after which the reminder is sent. "
                  "(Y - Year, M - month, d - day, h - hour, m - minute, s - second)",
        message="Message that needs to be reminded"
    )
    async def remindme(
        self,
        interaction: discord.Interaction,

        timestamp: str,
        message: str
    ) -> None:
        """
        This is the 'remind me' command implementation
        """

        time = timestamp
        decoded_time = {
            "Y": 0,     # year
            "M": 0,     # month
            "d": 0,     # day
            "h": 0,     # hour
            "m": 0,     # minute
            "s": 0      # second (I don't think it's needed?)
        }
        token = ""
        for char in time:
            if char.isdigit():
                token += char
            elif char in "YMDhms":
                try:
                    decoded_time[char] = int(token)
                except ValueError:
                    raise discord.ext.commands.BadArgument
            elif char == " " and token != "":
                token = ""

        # basically, if the entered time is bigger than 100 years
        total_years = decoded_time["Y"]
        total_years += decoded_time["M"] / 12
        total_years += decoded_time["d"] / 365.2422
        total_years += decoded_time["h"] / 8766
        total_years += decoded_time["m"] / 525960
        total_years += decoded_time["s"] / 31557600

        if total_years > 10:
            await interaction.response.send_message("Я не думаю что Discord будет существовать через 10 лет.")
            return

        await interaction.response.send_message("yes")
