import bot_utils as util
import random

from discord.ext import commands

random.seed()
class Misc:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def roll(self, ctx, *, roll_cmd:str):
        '''
        Type !roll xdy+z to roll x y sided dice and add z.
        You can also drop the lowest with xdydz.
        '''
        command_array = roll_cmd.split('+')
        bonus = 0
        if len(command_array) > 1:
            bonus = int(command_array[1])
        else:
            command_array = roll_cmd.split('-')
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
        
        rolled.sort()
        rolled.reverse()
        total = sum(rolled[0:len(rolled)-drop])
        total = total + bonus
        message = ctx.author.display_name + " rolled " + str(rolled) + ((" + " + str(bonus)) if bonus > 0 else "")
        message += ((" and dropped the lowest " + str(drop)) if drop > 0 else " ")
        message += "\nTotal: " + str(total)
        
        await ctx.send(message)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.author.send("I can't understand that roll. Valid formats are xdy, xdy+z, xdydw, xdydw+z.")
        util.logger.error(error)
        
    @commands.command()
    async def credits(self, ctx):
        '''Shows who to blame for all the bugs.'''
        await ctx.send("Bot made by CaptainDuh using discord.py rewrite. \
        \nTreasure generator, magic item availability, merc generator, \
        \ncalamity calculator, npc generator, and mule calculator by jedavis.  https://github.com/jedavis-rpg/ackstools \
        \nHenchman generator by golan2027. https://github.com/Golan2072/RPG")
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
def setup(bot):
    bot.add_cog(Misc(bot))
