import discord
import os
from discord.ext import commands
from pathlib import Path
if not os.path.isdir('cogs/data'):
    os.makedirs('cogs/data')
from cogs.util import pyson

config = pyson.Pyson('data/config/startup.json')
token = config.data.get('config').get('token')


def get_prefix(bot, message):
    prefixes = ['?', '!']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.util.owner']
bot = commands.Bot(command_prefix=get_prefix, description='A Rewrite Cog Example')


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    game = discord.Game("with building the cogs")
    await bot.change_presence(status=discord.Status.idle, activity=game)


def load_extensions():
    bot.startup_extensions = []
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                extension = 'cogs.'+cog[:-3]
                bot.startup_extensions.append(extension)

    if __name__ == "__main__":
        for extension in bot.startup_extensions:
            try:
                bot.load_extension(extension)
                print('Loaded {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


load_extensions()
bot.run(token, bot=True, reconnect=True)
