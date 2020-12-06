from dotenv import load_dotenv
from AnimeAnnoucement import checkNewEpisode, adds
from utilities import getDailyTemps, createEmbed
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
    channel = client.get_channel(782857465107578892)
    while not client.is_closed():
        now_utc = datetime.now()
        perthHour = now_utc.astimezone(timezone('Australia/Perth')).hour
        perthMinutes = now_utc.astimezone(timezone('Australia/Perth')).minute
        perthSeconds = now_utc.astimezone(timezone('Australia/Perth')).second
        if (perthHour == 7 or perthHour == 12 or perthHour == 18) and perthMinutes == 30 and perthSeconds == 1:
            temperature, status, image = getDailyTemps()
            embed = discord.Embed(
                title='Daily Temperatures',
                description='Temperature: ' + temperature + '\n\n' + status,
                colour=discord.Colour.blue()
            )
            embed.set_image(url=image)
            await channel.send(embed=embed)
        await asyncio.sleep(1)

@client.event
async def annoucement():
    await client.wait_until_ready()
    channel = client.get_channel(781035666553307136)
    while not client.is_closed():
        animes = checkNewEpisode()
        if animes != False:
            for anime in animes:
                anime = anime.split(',')
                embed = createEmbed(anime[0],anime[1],anime[2])
                await channel.send(embed=embed)
        await asyncio.sleep(900)

@client.event
async def delete():
    await client.wait_until_ready()
    while not client.is_closed():
        channel = client.get_channel(781035666553307136)
        await channel.purge(before=datetime.now() - timedelta(days=14))
        channel = client.get_channel(782857465107578892)
        await channel.purge(before=datetime.now() - timedelta(days=3))
        await asyncio.sleep(1209600)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to SkyVision Discord server!'
    )

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 783523446142664715:
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
    if message_id == 783523446142664715:
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
    name, episode, link = adds(anime[:-1])
    embed = discord.Embed(
        title=name,
        description='Added to bulletin' + '\n\n' + 'Latest episode is ' + str(episode) + '.',
        colour=discord.Colour.blue()
    )
    embed.set_image(url=link)
    await ctx.send(embed=embed)


client.loop.create_task(weather())
client.loop.create_task(annoucement())
client.loop.create_task(delete())
client.run(TOKEN)
