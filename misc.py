import bot_utils as util
import random
import discord
import datetime

from discord.ext import tasks, commands

random.seed()
PVP_CHANNEL = 467354528807649290

class Misc(commands.Cog):
    pvp_channel = None
    def __init__(self, bot):
        self.bot = bot
        pvp_channel = bot.get_channel(PVP_CHANNEL)
        #self.clean_pvp_channel.start()
        
    def cog_unload():
        self.clean_pvp_channel.cancel()
        
    def message_is_not_pinned(m):
        return not m.pinned
        
    @tasks.loop(seconds=600.0)
    async def clean_pvp_channel(self):
        two_weeks_ago = datetime.datetime.today() - datetime.timedelta(days=14)
        pvp_channel = self.bot.get_channel(PVP_CHANNEL)
        print(dir(pvp_channel))
        deleted = await pvp_channel.purge(limit=10000, oldest_first=True, before=two_weeks_ago, check=self.message_is_not_pinned)
        print(len(deleted))
    
    @clean_pvp_channel.before_loop
    async def before_clean_pvp(self):
        print('Waiting for server start')
        await self.bot.wait_until_ready()

    def get_roll_message(self, ctx, roll_cmd:str, sorted_output:bool):
        command_and_description = roll_cmd.split(' ', maxsplit=1)
        description = None
        if len(command_and_description) > 1:
            description = command_and_description[1]
        command_array = command_and_description[0].split('+')
        bonus = 0
        if len(command_array) > 1:
            bonus = int(command_array[1])
        else:
            command_array = command_and_description[0].split('-')
            if len(command_array) > 1:
                bonus = int(command_array[1]) * -1
        roll_cmd_array = command_array[0].split('d')
        
        dice = int(roll_cmd_array[0])
        sides = int(roll_cmd_array[1])
        drop = 0
        if(len(roll_cmd_array) > 2):
            drop = int(roll_cmd_array[2])
            
        rolled = []
        total = 0
        for x in range(dice):
            die_roll = random.randint(1, sides)
            rolled.append(die_roll)
        
        rolled_output = rolled if sorted_output else list(rolled)
        rolled.sort()
        rolled.reverse()
        total = sum(rolled[0:len(rolled)-drop])
        total = total + bonus
        message = ctx.author.display_name + " rolled " + str(rolled_output) + ((" + " + str(bonus)) if bonus > 0 else "")
        message += ((" and dropped the lowest " + str(drop)) if drop > 0 else " ")
        message += "\nTotal: " + str(total)
        return message, description
        
    @commands.command(name='unsortedroll', aliases=["rollunsorted"])
    async def unsorted_roll_cmd(self, ctx, *, roll_cmd:str):
        '''
        Type !roll xdy+z to roll x y sided dice and add z.
        You can also drop the lowest with xdydz.
        '''
        message, description = self.get_roll_message(ctx, roll_cmd, False)
        if description is not None:
            await ctx.send(f'{description}\n{message}')
        else:
            await ctx.send(message)
        util.logger.info(f'{ctx.author.name} : {ctx.message.content}')
                
    @commands.command(name='roll')
    async def roll(self, ctx, *, roll_cmd:str):
        '''
        Type !roll xdy+z to roll x y sided dice and add z.
        You can also drop the lowest with xdydz.
        '''
        message, description = self.get_roll_message(ctx, roll_cmd, True)
        if description is not None:
            await ctx.send(f'{description}\n{message}')
        else:
            await ctx.send(message)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.author.send("I can't understand that roll. Valid formats are xdy, xdy+z, xdydw, xdydw+z.")
        util.logger.error(error)
        
    @commands.command(name='statblock', aliases=["roll_stats","stats","rollstats"])
    async def statblock(self, ctx, roll_cmd:str=None):
        '''
        Type !roll xdy+z to roll x y sided dice and add z.
        You can also drop the lowest with xdydz.
        '''
        if not roll_cmd:
            roll_cmd = "3d6"
        message, description = self.get_roll_message(ctx, f'{roll_cmd} STR', False)
        total_message = f'{description}: {message}'
        message, description = self.get_roll_message(ctx, f'{roll_cmd} INT', False)
        total_message = f'{total_message}\n{description}: {message}'
        message, description = self.get_roll_message(ctx, f'{roll_cmd} WIS', False)
        total_message = f'{total_message}\n{description}: {message}'
        message, description = self.get_roll_message(ctx, f'{roll_cmd} DEX', False)
        total_message = f'{total_message}\n{description}: {message}'
        message, description = self.get_roll_message(ctx, f'{roll_cmd} CON', False)
        total_message = f'{total_message}\n{description}: {message}'
        message, description = self.get_roll_message(ctx, f'{roll_cmd} CHA', False)
        total_message = f'{total_message}\n{description}: {message}'
        await ctx.send(total_message)
        
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @statblock.error
    async def statblock_error(self, ctx, error):
        await ctx.author.send("I can't understand that roll. Valid formats are xdy, xdy+z, xdydw, xdydw+z.")
        util.logger.error(error)
        
    @commands.command()
    async def credits(self, ctx):
        '''Shows who to blame for all the bugs.'''
        await ctx.send("Bot made by CaptainDuh using discord.py rewrite. \
        \nTreasure generator, magic item availability, merc generator, \
        \ncalamity calculator, and npc generator by jedavis.  https://github.com/jedavis-rpg/ackstools \
        \nHenchman generator by golan2027. https://github.com/Golan2072/RPG")
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    #@commands.command()
    #async def friendcode(self, ctx, code:str):
    #    '''Add your friendcode to the server's database.'''
        
        
def setup(bot):
    bot.add_cog(Misc(bot))
