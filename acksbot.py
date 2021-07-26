import discord
import asyncio
import datetime

import bot_utils as util

from discord.ext import commands

bot = commands.Bot(command_prefix=['!','/'], case_insensitive=True)
PUSHPIN = '\U0001F4CC'
ARCHIVE_CHANNEL = 503204909173440519
ACKS_ID = 427567650449915904

@bot.event
async def on_ready():
    global archive_channel
    global acks_server
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    acks = discord.Game("Say !help for command list")
    await bot.change_presence(activity=acks)
    archive_channel = bot.get_channel(ARCHIVE_CHANNEL)
    acks_server = bot.get_guild(ACKS_ID)
    bot.load_extension('cogs.player_tools')
    bot.load_extension('cogs.world_tools')
    #bot.load_extension('cogs.gm_tools')
    bot.load_extension('cogs.misc')

@bot.event
async def on_raw_reaction_add(payload):
    global archive_channel
    
    if payload.emoji.name == PUSHPIN:
        channel = bot.get_channel(payload.channel_id)
        if payload.guild_id != 427567650449915904:
            return
        guild = bot.get_guild(payload.guild_id)
        channel_everyone_overwrites = channel.overwrites_for(guild.default_role)
        if channel_everyone_overwrites is not None and channel_everyone_overwrites.read_messages == False:
            print("Permission is insufficient to pin")
            return
        message = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)
        reactions = message.reactions
        for reaction in reactions:
            if(payload.emoji.name == reaction.emoji):
                if not reaction.me:
                    content = "%s: %s" % (message.channel.mention, message.jump_url)
                    embed = discord.Embed(description=message.content)
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url_as(format='png'))
                    embed.timestamp = message.created_at
                    if message.embeds:
                        data = message.embeds[0]
                        if data.type == 'image':
                            embed.set_image(url=data.url)

                    if message.attachments:
                        file = message.attachments[0]
                        if file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                            embed.set_image(url=file.url)
                        else:
                            embed.add_field(name='Attachment', value="[%s](%s)" % (file.filename, file.url), inline=False)
                            
                    await archive_channel.send(content, embed=embed)
                    await message.add_reaction(PUSHPIN)
                return
     
def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

def message_is_not_pinned(m):
    return not m.pinned

with open('server_key') as f:
    server_key = f.read()

bot.run(server_key)
