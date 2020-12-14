from dotenv import load_dotenv
from AnimeAnnoucement import checkNewEpisode, adds, listAllBulletin, listEpisodes, removes
from utilities import getDailyTemps, createEmbed, getSunsetAndSunrise
from datetime import datetime, timedelta
from pytz import timezone
from discord.ext import commands
import asyncio
import os
import discord


load_dotenv()

#Retrieve tokens and guild
TOKEN = os.getenv('DISCORD_TOKEN')[1:-1]
GUILD = os.getenv('DISCORD_GUILD')[1:-1]

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    #print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Genshin Impact'))

@client.event
async def weather():
    await client.wait_until_ready()
    channel = client.get_channel('your channel name')
    while not client.is_closed():
        now_utc = datetime.now()
        perthHour = now_utc.astimezone(timezone('Australia/Perth')).hour
        perthMinutes = now_utc.astimezone(timezone('Australia/Perth')).minute
        perthSeconds = now_utc.astimezone(timezone('Australia/Perth')).second
        #Set morning status
        if perthHour == 7 and perthMinutes == 30 and perthSeconds == 1:
            temperature, status, image = getDailyTemps()
            sunrise, sunset = getSunsetAndSunrise()
            title = 'Morning Status'
            description = 'Temperature: ' + temperature + '\n' +'Status: ' + status + '\n' + 'Sunrise: ' + sunrise + '\n' + 'Sunset: ' + sunset
            embed = createEmbed(title, description, image)
            await channel.send(embed=embed)
        #Set noon status
        if perthHour == 12 and perthMinutes == 30 and perthSeconds == 1:
            temperature, status, image = getDailyTemps()
            title = 'Noon Status'
            description = 'Temperature: ' + temperature + '\n\n' + status
            embed = createEmbed(title, description, image)
            await channel.send(embed=embed)
        #Set afternoon status
        if perthHour == 18 and perthMinutes == 30 and perthSeconds == 1:
            temperature, status, image = getDailyTemps()
            title = 'Noon Status'
            description = 'Temperature: ' + temperature + '\n\n' + status
            embed = createEmbed(title, description, image)
            await channel.send(embed=embed)
        await asyncio.sleep(1)

@client.event
async def annoucement():
    await client.wait_until_ready()
    channel = client.get_channel('your channel name')
    while not client.is_closed():
        animes = checkNewEpisode()
        if(animes == -1):
            await channel.send('Failed to update bulletin')
        elif animes != False:
            for anime in animes:
                title = anime.split(',')[0]
                description = 'Episode: ' + anime[1] + ' just released.'
                link = anime.split(',')[2]
                embed = createEmbed(title,description,link)
                await channel.send(embed=embed)
        await asyncio.sleep(900)

@client.event
async def delete():
    await client.wait_until_ready()
    while not client.is_closed():
        channel = client.get_channel('your channel name')
        await channel.purge(before=datetime.now() - timedelta(days=14))
        channel = client.get_channel('your channel name')
        await channel.purge(before=datetime.now() - timedelta(days=3))
        await asyncio.sleep(86400)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to SkyVision Discord server!'
    )

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 'your channel name':
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Rocketleague':
            role = discord.utils.get(guild.roles, name='RL players')
        elif payload.emoji.name == '3842_PaimonAngry':
            role = discord.utils.get(guild.roles, name='Genshin players')
        elif payload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles, name='CSGO')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 'your channel name':
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Rocketleague':
            role = discord.utils.get(guild.roles, name='RL players')
        elif payload.emoji.name == '3842_PaimonAngry':
            role = discord.utils.get(guild.roles, name='Genshin players')
        elif payload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles, name='CSGO')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.remove_roles(role)

@client.command()
async def add(ctx, *args):
    anime = ''
    for arg in args:
        anime += arg + ' '
    anime = anime[:-1]
    test, test2, full = adds(anime)
    if test == -1:
        await ctx.send('Failed to get episodes')
    elif test == 2:
        await ctx.send('Already in the bulletin')
    else:
        title = test
        description = 'Added to bulletin' + '\n\n' + 'Latest episode is ' + str(test2) + '.'
        embed = createEmbed(title, description, full)
        await ctx.send(embed=embed)

@client.command()
async def listAll(ctx, *args):
    summary = listAllBulletin()
    await ctx.send(summary)

@client.command()
async def listEp(ctx, *args):
    anime = ''
    for arg in args:
        anime += arg + ' '
    anime = anime[:-1]
    test, full = listEpisodes(anime)
    if test == 2:
        await ctx.send('Not in the list')
    else:
        embed = createEmbed(anime, test, full)
        await ctx.send(embed=embed)

@client.command()
async def remove(ctx, *args):
    anime = ''
    for arg in args:
        anime += arg + ' '
    anime = anime[:-1]
    test = removes(anime)
    if test == 2:
        await ctx.send('Not in the list')
    else:
        await ctx.send(anime + ' successfully removed.')


client.loop.create_task(weather())
client.loop.create_task(annoucement())
client.loop.create_task(delete())
client.run(TOKEN)
