import bot_utils as util
import discord
import db_utils

from discord.ext import commands

async def check_if_not_gm(ctx):
    return not commands.has_role("GM")

class GMTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["gm"])
    async def judge(self, ctx):
        '''Adds you as a GM'''
        util.logger.info(ctx.author.id)
        await db_utils.add_gm(ctx.author.id, ctx.author.name)
        await ctx.author.send("You are now a GM.")
    
    @commands.command(aliases=["newgame"])
    async def new_game(self, ctx, gameName=""):
        '''Adds your game to the database.'''
        if not gameName:
            gameName = f"{ctx.author.name}'s game"
        util.logger.info(f'{ctx.author.id} creating {gameName}')
        await db_utils.add_game(ctx.author.id, gameName)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        await ctx.channel.send(f'{gameName} created')
        
    @new_game.error
    async def new_game_error(self, ctx, error):
        util.logger.info(error)
        await ctx.author.send("Something went wrong creating that game. Have you flagged yourself as a GM? Use the !gm command to do so.")
    
    @commands.command(aliases=["listgame", "listgames"])
    async def list_games(self, ctx):
        '''Lists the games you are GMing'''
        game_names = await db_utils.get_games(ctx.author.id)
        await ctx.author.send(f'You are currently GMing the following games: {game_names}')
    
    @list_games.error
    async def list_games_error(self, ctx, error):
        util.logger.info(error)
        await ctx.author.send("I was unable to list your games.")
        
    @commands.command(aliases=["removegame"])
    async def remove_game(self, ctx, name:str):
        '''Removes one of your games from the database.'''
        await db_utils.remove_game(ctx.author.id, name)
        await ctx.author.send(f'{name} deleted.')
        
    @remove_game.error
    async def remove_game_error(self, ctx, error):
        util.logger.info(error)
        await ctx.author.send("Something went wrong removing that game. Did you enter the correct name? Are there still active players?")
    
    @commands.command(aliases=["addplayer"])
    @commands.guild_only()
    async def add_player(self, ctx, playerName:str, gameName:str=""):
        '''Add the mentioned (@ user) player to your game.'''
        #ctx.guild.members
        playerID = ctx.message.mentions[0].id
        playerName = ctx.message.mentions[0].name
        if not gameName:
            gameNameRecord = await db_utils.get_games(ctx.author.id)
            gameID = await db_utils.get_game_id(ctx.author.id, gameNameRecord['name'])
        else:
            gameID = await db_utils.get_game_id(ctx.author.id, gameName)
        await db_utils.add_player(gameID, playerID, playerName)
        
def setup(bot):
    bot.add_cog(GMTools(bot))
