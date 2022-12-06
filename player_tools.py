import bot_utils as util
import hirelings as hirelingGenerator
import henchgenchar
import deserter
import muleteer

from discord.ext import commands

class PlayerTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mercs', aliases=["hirelings"])
    async def mercs(self, ctx, marketClass:int, months:int=1):
        '''DMs you a list of hirelings.'''
        hirelingMessage = hirelingGenerator.genHirelings("hireprices", marketClass, months)
        await ctx.author.send(content=hirelingMessage)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @mercs.error
    async def mercs_error(self, ctx, error):
        await ctx.author.send("I don't understand what you mean. Please provide the a valid market class (1-5) and number of months, separated by a space.")
        util.logger.error(error)
    
    @commands.command(name='henchmen')
    async def henchmen(self, ctx, marketClass:int):
        '''DMs you a long list of henchmen.'''
        henchmenOutput = henchgenchar.market_gen(marketClass, True)
        for henchMessage in util.chunks(henchmenOutput, 2000):
            await ctx.author.send(content=henchMessage)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @henchmen.error
    async def henchmen_error(self, ctx, error):
        await ctx.author.send("I didn't understand that command. Please provide a valid market class (1-6).")
        util.logger.error(error)

    @commands.command(name='calamity', aliases=['deserters'])
    async def calamity(self, ctx, groupSize:int, moraleMod:int):
        '''Calculate how a group reacts after a calamity
        Take a number of mercenaries or thieves who have 
        suffered a calamity or leadership change, and determine how many 
        desert, betray, or so forth
        '''
        await ctx.author.send(deserter.calculateDeserters(groupSize, moraleMod))
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    @calamity.error
    async def calamity_error(self, ctx, error):
        await ctx.author.send("I didn't understand that calamity command. Please send the group size and morale modifier.")
        util.logger.error(error)
    
    
    @commands.command(name='mules', aliases=["mule"])
    async def mules(self, ctx, people:int, days:int):
        '''
        Calculates the number of mules required to carry food for a group
        Per page 94, 8 lb of water and 2lb of food (1 st total) per person per day
        Rations are sold per week, -> 1.4st of food per price given
        '''
        await ctx.author.send(muleteer.muleteer(people, days))
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    @mules.error
    async def mule_error(self, ctx, error):
        await ctx.author.send("The mules got lost. Please remember to send the group size and number of days.")
        util.logger.error(error)

def setup(bot):
    bot.add_cog(PlayerTools(bot))
