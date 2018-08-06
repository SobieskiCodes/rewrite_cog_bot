from discord.ext import commands
import os
from cogs.util import pyson
config = pyson.Pyson('data/config/startup.json')


def is_owner():
    def predictate(ctx):
        if ctx.author is ctx.guild.owner:
            return True
        return False
    return commands.check(predictate)


class GuildOwnerCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def enable(self, ctx, cog: str=None):
        '''Cogs are case senstive'''
        if not cog:
            cog_list = []
            for cog in self.bot.cogs:
                cog_list.append(cog)

            await ctx.send(f'Available cogs are: {cog_list[2:]}')
            return

        if cog in (cog for cog in self.bot.cogs):
            self.bot.config.data['servers'][str(ctx.guild.id)][cog] = True
            self.bot.config.save()
            await ctx.send(f'{cog} Enabled.')
            return

        else:
            await ctx.send(f'I couldnt find a cog named {cog}')

    @commands.command()
    @is_owner()
    async def disable(self, ctx, cog: str = None):
        '''Cogs are case senstive'''
        if not cog:
            cog_list = []
            for cog in self.bot.cogs:
                cog_list.append(cog)

            await ctx.send(f'Available cogs are: {cog_list[2:]}')
            return


        if cog in config.data.get('servers').get(str(ctx.guild.id)):
            self.bot.config.data['servers'][str(ctx.guild.id)].pop(cog, None)
            self.bot.config.save()
            await ctx.send(f'{cog} Disabled.')
            return

        else:
            await ctx.send(f'I couldnt find a cog named {cog}')


def setup(bot):
    bot.add_cog(GuildOwnerCog(bot))
