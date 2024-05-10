import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
import base64
import asyncio
import psutil
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ReplayDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="replaydl", description="Download and post the replay file for the specified game ID.")
    @app_commands.describe(game_id="Game ID of the replay to download")
    async def replay_download(self, interaction: discord.Interaction, game_id: str):
        await interaction.response.defer()

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
            filename = f"JP1-{game_id}.rofl"
            save_directory = os.path.expanduser("~/Documents/League of Legends/Replays")
            path = os.path.join(save_directory, filename)
            await self.wait_for_file(path)

            if os.path.exists(path) and os.path.getsize(path) > 0:
                file = discord.File(path, filename=filename)
                await interaction.followup.send("Replay file downloaded.", file=file)
            else:
                await interaction.followup.send("The file was not downloaded correctly.")
        else:
            await interaction.followup.send(f"Download failed. Status code: {response.status_code}")

    async def wait_for_file(self, path):
        timeout = 60
        while not (os.path.exists(path) and os.path.getsize(path) > 0) and timeout > 0:
            await asyncio.sleep(1)
            timeout -= 1

    def read_lockfile(self):
        client_process = self.find_lol_client()
        if client_process:
            base_folder = os.path.dirname(client_process.exe())
            lockfile_path = os.path.join(base_folder, "lockfile")
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
        else:
            print("LOL client is not running")
        return None, None

    def find_lol_client(self):
        for process in psutil.process_iter(['pid', 'name']):
            if "leagueclient.exe" in process.info['name']:
                return process
        return None

async def setup(bot):
    await bot.add_cog(ReplayDownloader(bot))