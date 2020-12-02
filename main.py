from dotenv import load_dotenv
from AnimeAnnoucement import checkNewEpisode
from Functions import getTemp
from Functions import getStatus
from Functions import createEmbed
import asyncio
import os
import discord


load_dotenv()

#Retrieve tokens and guild
TOKEN = os.getenv('DISCORD_TOKEN')[1:-1]
GUILD = os.getenv('DISCORD_GUILD')[1:-1]

client = discord.Client()

@client.event
async def on_ready():
    #print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Genshin Impact'))

@client.event
async def weather():
    await client.wait_until_ready()
    channel = client.get_channel(782857465107578892)
    while not client.is_closed():
        temp = getTemp()
        image, status = getStatus()
        embed = discord.Embed(
            title='Weather forecast',
            description='Temperature: ' + str(temp) + 'C\n\n' + status,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=image)
        await channel.send(embed=embed)
        await asyncio.sleep(21600)

@client.event
async def annoucement():
    await client.wait_until_ready()
    channel = client.get_channel(781035666553307136)
    while not client.is_closed():
        names = ['Jujutsu Kaisen', 'Tonikaku Kawaii', 'Black Clover', 'The day I became a God', 'Talentless Nana',
                 'I m Standing On 1 000 000 Lives', 'Our Last Crusade Or The Rise Of A New World',
                 'By The Grace Of The Gods', 'Noblesse']
        for anime in names:
            episode, link = checkNewEpisode(anime)
            if episode != False:
                embed = createEmbed(anime, episode, link)
                await channel.send(embed=embed)
        await asyncio.sleep(900)

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

client.loop.create_task(weather())
client.loop.create_task(annoucement())
client.run(TOKEN)
