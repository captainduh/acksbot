import bot_utils as util
import discord

from discord.ext import commands

async def check_if_not_gm(ctx):
    return not commands.has_role("GM")

class GMTools:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='newgame')
    @guild_only()
    @commands.check(check_if_not_gm)
    async def new_game(self, ctx, gameName=""):
        '''Creates a voice and text channel for your game.'''
        ctx.author
        ctx.guild.
    
    @commands.command(name='removegame')
    @guild_only()
    async def remove_game(self, ctx):
        '''Removes the voice and text channels you previously created for your game.'''
        
