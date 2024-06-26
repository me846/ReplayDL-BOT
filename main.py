import discord
from discord.ext import commands
import configparser
import os
import src.Check_Client as check_client
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(application_path)

config = configparser.ConfigParser()
config_file = os.path.join(application_path, 'config.ini')
config.read(config_file)

if 'Settings' not in config or 'BOT_TOKEN' not in config['Settings'] or 'REGION' not in config['Settings']:
    raise ValueError("Config file is missing required settings.")

bot_token = config['Settings']['BOT_TOKEN']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!#", intents=intents)

@bot.event
async def on_ready():
    cogs_path = resource_path('cogs')
    for filename in os.listdir(cogs_path):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    slash = await bot.tree.sync()
    print(f'{bot.user} is online \n {len(slash)} slash commands')

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')

def main():
    try:
        if check_client.check_lol_client_running():
            bot.run(bot_token)
        else:
            print("The bot will not start. Please start the League of Legends client.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press any key to exit...")

if __name__ == '__main__':
    main()