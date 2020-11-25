from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from AnimeAnnoucement import checkNewEpisode

load_dotenv()

#Need to fix
TOKEN = os.getenv('DISCORD_TOKEN')[1:-1]
GUILD = os.getenv('DISCORD_GUILD')[1:-1]

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print(checkNewEpisode())

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to UWA leaguers Discord server!'
    )

client.run(TOKEN)
keep_alive()