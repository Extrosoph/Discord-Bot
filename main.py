from keep_alive import keep_alive
from dotenv import load_dotenv
from AnimeAnnoucement import checkNewEpisode
from Functions import getTemp
from Functions import getStatus
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

    channel = client.get_channel('channel name')
    temp = getTemp()
    image, status = getStatus()
    embed = discord.Embed(
        title='Weather forecast',
        description='Temperature: ' + str(temp) + 'C\n\n' + status,
        colour = discord.Colour.blue()
    )
    embed.set_image(url=image)
    await channel.send(embed=embed)

@client.event
async def annoucement():
    await client.wait_until_ready()
    channel = client.get_channel('channel name')
    while not client.is_closed():
        Jujutsu = checkNewEpisode('jujutsu kaisen')
        if Jujutsu != False:
            embed = discord.Embed(
                title='Jujutsu Kaisen',
                description='Episode ' + str(Jujutsu) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(url='https://upload.wikimedia.org/wikipedia/en/4/46/Jujutsu_kaisen.jpg')
            await channel.send(embed=embed)

        Tonikaku = checkNewEpisode('tonikaku kawaii')
        if Tonikaku != False:
            embed = discord.Embed(
                title='Tonikaku Kawaii',
                description='Episode ' + str(Tonikaku) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(url='https://cdn.myanimelist.net/images/anime/1613/108722l.jpg')
            await channel.send(embed=embed)

        BlackC = checkNewEpisode('black clover')
        if BlackC != False:
            embed = discord.Embed(
                title='Black Clover',
                description='Episode ' + str(BlackC) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://static.wikia.nocookie.net/blackclover/images/8/80/Anime_Visual_for_Arc_9.png/revision/latest?cb=20190718141839')
            await channel.send(embed=embed)

        TDIBAG = checkNewEpisode('the day i became a god')
        if TDIBAG != False:
            embed = discord.Embed(
                title='The Day I Became God',
                description='Episode ' + str(TDIBAG) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://cdn.myanimelist.net/images/anime/1396/109465l.jpg')
            await channel.send(embed=embed)

        Talentless_Nana = checkNewEpisode('talentless nana')
        if Talentless_Nana != False:
            embed = discord.Embed(
                title='Talentless Nana',
                description='Episode ' + str(Talentless_Nana) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://images-na.ssl-images-amazon.com/images/I/91yKBuefjpL._RI_.jpg')
            await channel.send(embed=embed)

        Million_lives = checkNewEpisode('I m standing on 1 000 000 lives')
        if Million_lives != False:
            embed = discord.Embed(
                title='I am Standing on a Million Lives',
                description='Episode ' + str(Million_lives) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://cdn.myanimelist.net/images/anime/1825/108800l.jpg')
            await channel.send(embed=embed)

        Last_crusade = checkNewEpisode('our last crusade or the rise of a new world')
        if Last_crusade != False:
            embed = discord.Embed(
                title='Our Last Crusade or the Rise of a New World',
                description='Episode ' + str(Last_crusade) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://images-na.ssl-images-amazon.com/images/I/91XDXrP-q2L.jpg')
            await channel.send(embed=embed)

        BTGOTG = checkNewEpisode('by the grace of the gods')
        if BTGOTG != False:
            embed = discord.Embed(
                title='By the Grace of the Gods',
                description='Episode ' + str(BTGOTG) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/0/0f/By_the_Grace_of_the_Gods_light_novel_volume_1_cover.jpg')
            await channel.send(embed=embed)

        Noblesse = checkNewEpisode('Noblesse')
        if Noblesse != False:
            embed = discord.Embed(
                title='Noblesse',
                description='Episode ' + str(Noblesse) + ' just released',
                colour=discord.Colour.blue()
            )
            embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/en/0/0f/By_the_Grace_of_the_Gods_light_novel_volume_1_cover.jpg')
            await channel.send(embed=embed)
        await asyncio.sleep(3600)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to SkyVision Discord server!'
    )

#Need to work on
@client.event
async def on_reaction_add(reaction, user):
    print('yay')
    Channel = 783315915982241842
    if reaction.message.channel.id != Channel:
        return
    print(reaction.emoji)
    if reaction.emoji == ":emoji_5:":
      Role = discord.utils.get(user.server.roles, name="Genshin Players")
      await client.add_roles(user, Role)
    if reaction.emoji == ":race_car:":
        Role = discord.utils.get(user.server.roles, name="RL players")
        await client.add_roles(user, Role)

client.loop.create_task(annoucement())
client.run(TOKEN)
keep_alive()
