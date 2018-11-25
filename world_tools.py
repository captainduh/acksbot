import bot_utils as util
import henchstat_gen_for_bot as hg
import magicavail
import treasuregen
import hex2 as lairGen

from discord.ext import commands

class WorldTools:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='magicmarket')
    async def magicmarket(self, ctx, marketClass:int, months:int=1):
        '''DMs you a long list of available magic items.'''
        magicMarketOutput = magicavail.genMarketAvailability(marketClass, months)
        for magicMarketMessage in util.chunks(magicMarketOutput, 2000):
            await ctx.author.send(magicMarketMessage)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    @magicmarket.error
    async def magicmarket_error(self, ctx, error):
        await ctx.author.send("I didn't understand that command. Please provide a valid market class (1-6) and number of months.")
        util.logger.error(error)

    @commands.command(name='treasure')
    async def treasure(self, ctx, *, tableList:str):
        '''!treasure [amount] <comma separated list of table names>
        Valid treasure types: A-R 
        Ornamental, Orn[10,25,50]
        Gem, Gem[75,100,250,500,750,1000]
        Brilliant, Bril[1500,2000,4000,6000,8000,10000]
        Trinket, Jewelry, Regalia, Magic, Potion 
        Ring, ProtRing, Scroll, Wand, Sword 
        MiscMagic, MiscWeapon, Armor
        Example: !treasure 4 Bril4000
        '''
        maybeNumber = tableList.split(" ", 1)
        amount = 1
        if maybeNumber[0].isnumeric():
            tables = maybeNumber[1].replace(" ","").split(",")
            amount = int(maybeNumber[0])
        else:
            tables = tableList.replace(" ","").split(",")
        treasureOutput = treasuregen.generateTreasure(tables, amount)
        for treasureMessage in util.chunks(treasureOutput, 2000):
            await ctx.author.send(treasureMessage)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    @treasure.error
    async def treasure_error(self, ctx, error):
        await ctx.author.send("I didn't understand that treasure command. Make sure you capitalize properly (e.g. Gems, K, C) and separate treasure types by a comma. If you only want one treasure type you don't need a comma. You can optionally include how much treasure you want to generate.")
        util.logger.error(error)
    
    @commands.command(name='npc')
    async def npc(self, ctx, level:int):
        '''Generate an npc at the specified level'''
        if level < 0 or level > 14:
            await ctx.author.send("NPC level must be between 0 and 14.")
        else:
            await ctx.author.send(hg.genHenches(level))
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @npc.error
    async def npc_error(self, ctx, error):
        await ctx.author.send("I didn't understand that command. Please specify a level.")
        util.logger.error(error)

    @commands.command(name='party')
    async def party(self, ctx, num:int, minLevel:int, maxLevel:int=0):
        '''Generate stats for a party.'''
        if maxLevel == 0:
            maxLevel = minLevel
        if minLevel < 0 or maxLevel > 14:
            await ctx.author.send("The party got lost. Make sure you send a valid min and max level.")
        else:
            await ctx.author.send(hg.genParty(num, minLevel, maxLevel))
        util.logger.info(ctx.author.name + ": " + ctx.message.content)

    @party.error
    async def party_error(self, ctx, error):
        await ctx.author.send("The party got lost. Please specify a number of party members and their level range.")
    
    @commands.command(name='lairs', aliases=["lair"])
    async def lairs(self, ctx, terrain:str, *, optional='1 1'):
        '''Generates lairs for a given terrain and number of hexes. Optional arguments <row>, <col>.
        Valid terrain types are "City","Inhabited","Clear","Grass","Scrub",
        "Hill","Woods","Desert","Jungle","Mountain",and "Swamp"
        '''
        rows = 1
        cols = 1
        if optional is not None and len(optional) > 0:
            layout = optional.split()
            rows = int(layout[0])
            if len(layout) > 1:
                cols = int(layout[1])
        if (rows * cols) > 25:
            await ctx.author.send("You really don't want to generate that many hexes over Discord all at once. Do it a bit at a time, or download this tool directly from Jedavis's github page. You can find a link to it with the !credits command.")
            return
            
        lairString = lairGen.generate(rows, cols, terrain.capitalize(), False, True)
        for lairMessage in util.chunks(lairString, 2000):
            await ctx.author.send(lairMessage)
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
    
    @lairs.error
    async def lair_error(self, ctx, error):
        await ctx.author.send("You specified an invalid terrain type or number of columns/rows of hexes. Type !help lairs to see a list of valid terrains.")
        util.logger.error(error)
    
    @commands.command(name='encounter')
    async def encounter(self, ctx, terrain:str):
        '''Generates an encounter for a given terrain type.
        Valid terrain types are "City","Inhabited","Clear","Grass","Scrub",
        "Hill","Woods","Desert","Jungle","Mountain",and "Swamp"
        '''
        await ctx.author.send(lairGen.generate(1, 1, terrain.capitalize(), True, True))
        util.logger.info(ctx.author.name + ": " + ctx.message.content)
        
    @encounter.error
    async def encounter_error(self, ctx, error):
        await ctx.author.send("You specified an invalid terrain type. Type !help lairs to see a list of valid terrains.")
        util.logger.error(error)
        
def setup(bot):
    bot.add_cog(WorldTools(bot))
