import discord
from discord import app_commands
from discord.ext import commands
import requests
import base64
import asyncio
import os
import configparser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = configparser.ConfigParser()
config.read('config.ini')
REGION = config['Settings']['REGION']

class ReplayDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="replaydl", description="Download and post a replay file by game ID.")
    @app_commands.describe(game_id="The game ID of the replay to download")
    async def replay_download(self, interaction: discord.Interaction, game_id: str):
        await interaction.response.defer()
        guild = interaction.guild
        if not guild:
            await interaction.followup.send("This command can only be used within a server.")
            return

        max_file_size = {0: 25 * 1024 * 1024, 1: 25 * 1024 * 1024, 2: 50 * 1024 * 1024, 3: 100 * 1024 * 1024}.get(guild.premium_tier, 25 * 1024 * 1024)

        api_port, api_pwd = self.read_lockfile()
        if not api_port or not api_pwd:
            await interaction.followup.send("Failed to obtain API authentication information.", ephemeral=True)
            return

        url = f"https://127.0.0.1:{api_port}/lol-replays/v1/rofls/{game_id}/download"
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'riot:{api_pwd}'.encode()).decode()}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data='{"componentType": "replay-button_match-history"}', verify=False)

        if response.status_code in (200, 204):
            filename = f"{REGION}-{game_id}.rofl"
            save_directory = os.path.expanduser("~/Documents/League of Legends/Replays")
            path = os.path.join(save_directory, filename)
            await self.wait_for_file(path)

            if os.path.exists(path) and os.path.getsize(path) > 0:
                if os.path.getsize(path) > max_file_size:
                    await interaction.followup.send(f"The file size exceeds {max_file_size // 1024 // 1024}MB and cannot be sent.")
                else:
                    file = discord.File(path, filename=filename)
                    await interaction.followup.send("The replay file has been downloaded.", file=file)
            else:
                await interaction.followup.send("The file was not downloaded properly.")
        else:
            await interaction.followup.send(f"Failed to download. Status code: {response.status_code}")

    async def wait_for_file(self, path):
        timeout = 60
        while not (os.path.exists(path) and os.path.getsize(path) > 0) and timeout > 0:
            await asyncio.sleep(1)
            timeout -= 1

    def read_lockfile(self):
        lockfile_path = "C:/Riot Games/League of Legends/lockfile"
        try:
            with open(lockfile_path, "r") as file:
                data = file.read().strip().split(':')
                api_port = data[2]
                api_pwd = data[3]
                return api_port, api_pwd
        except FileNotFoundError:
            print("Lockfile not found")
        except IndexError:
            print("Error reading lockfile")
        return None, None

async def setup(bot):
    await bot.add_cog(ReplayDownloader(bot))
