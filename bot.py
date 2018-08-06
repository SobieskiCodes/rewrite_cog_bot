import discord
import os
import traceback
from discord.ext import commands
from pathlib import Path
if not os.path.isdir('cogs/data'):
    os.makedirs('cogs/data')
from cogs.util import pyson


def get_prefix(bot, message):
    prefix = bot.config.data.get('servers').get(str(message.guild.id)).get('prefix')
    if not prefix:
        prefix = '!'
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefix)(bot, message)


bot = commands.AutoShardedBot(command_prefix=get_prefix, formatter=None, description='A Rewrite Cog Example',
                              pm_help=False)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    game = discord.Game("with building the cogs")
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.errors.CheckFailure):
        try:
            raise error
        except Exception as error:
            tb = traceback.format_exc()
            print(error, tb)
    else:
        pass


@bot.check
async def __before_invoke(ctx):
    cog_name = ctx.command.cog_name
    if not cog_name:
        cog_name = "None"
    if cog_name in bot.config.data.get('servers').get(str(ctx.guild.id)):
        return True


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


bot.config = pyson.Pyson('data/config/startup.json')
token = bot.config.data.get('config').get('token')
load_extensions()
bot.run(token, bot=True, reconnect=True)
