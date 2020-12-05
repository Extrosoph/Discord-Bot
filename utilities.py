from urllib.request import Request, urlopen
import discord
from bs4 import BeautifulSoup


def getDailyTemps():
    url = 'https://www.weather.com.au/wa/perth/current'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(uClient).read()
    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    temp = soup.find_all('tr')[1].find('td', class_='val').getText()
    part = soup.find('div', {'id': 'currentIcon'})
    status = part.find('p').getText()
    link = part.find('img')['src']
    return temp, status, link

def createEmbed(title, episode, link):
    embed = discord.Embed(
        title=title,
        description='Episode ' + str(episode) + ' just released',
        colour=discord.Colour.blue()
    )
    embed.set_image(url=link)
    return embed