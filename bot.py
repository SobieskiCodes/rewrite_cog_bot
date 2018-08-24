import discord
import os
import traceback
from discord.ext import commands
from pathlib import Path
from cogs.util import pyson
version = '0.1.0'


def get_prefix(bot, message):
    prefix = bot.config.data.get('servers').get(str(message.guild.id)).get('prefix')
    if not prefix:
        prefix = '!'
    return commands.when_mentioned_or(*prefix)(bot, message)


bot = commands.AutoShardedBot(command_prefix=get_prefix, formatter=None, description=f'v{version} IAmGroot', pm_help=False)


@bot.event
async def on_guild_join(guild):
    new_guild = {"None": True, "OwnerCog": True, "GuildOwnerCog": True, "prefix": "!"}
    bot.config.data['servers'][str(guild.id)] = new_guild
    bot.config.save()


@bot.event
async def on_guild_remove(guild):
    bot.config.data['servers'].pop(str(guild.id), None)
    bot.config.save()


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    game = discord.Game(f"Mention me for prefix")
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure) or isinstance(error, commands.errors.CommandNotFound):
        return
    else:
        raise error


@bot.check
async def __before_invoke(ctx):
    cog_name = ctx.command.cog_name
    if not cog_name:
        cog_name = "None"
    if cog_name in bot.config.data.get('servers').get(str(ctx.guild.id)):
        return True


@bot.event
async def on_message(message):
    if any(mention.name == bot.user.name for mention in message.mentions):
        if len(message.mentions) == 1:
            if message.content == f'<@{message.raw_mentions[0]}>':
                prefix = bot.config.data.get('servers').get(str(message.guild.id)).get('prefix')
                await message.channel.send(f'my prefix is {prefix}')
    await bot.process_commands(message)


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
servers = bot.config.data.get('servers')
token = bot.config.data.get('config').get('token')
load_extensions()
bot.run(token, bot=True, reconnect=True)
