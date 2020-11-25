from keep_alive import keep_alive
from dotenv import load_dotenv
from AnimeAnnoucement import checkNewEpisode
import os
import discord


load_dotenv()

#Retrieve tokens and guild
TOKEN = os.getenv('DISCORD_TOKEN')[1:-1]
GUILD = os.getenv('DISCORD_GUILD')[1:-1]

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Rocket League'))
    channel = client.get_channel(781035666553307136)
    new = checkNewEpisode()
    if new != False:
        embed = discord.Embed(
            title='Jujutsu Kaisen',
            description = 'Episode ' + str(new) + ' just released',
            colour = discord.Colour.blue()
        )
        embed.set_image(url='https://upload.wikimedia.org/wikipedia/en/4/46/Jujutsu_kaisen.jpg')

        await channel.send(embed=embed)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to UWA leaguers Discord server!'
    )

client.run(TOKEN)
keep_alive()