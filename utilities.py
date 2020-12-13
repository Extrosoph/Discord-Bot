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

def getSunsetAndSunrise():
    url = 'https://www.timeanddate.com/sun/australia/perth'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(uClient).read()
    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    part = soup.find('div',class_='bk-focus__info')
    set = part.find_all('td')[6].getText().split(' ')[:2]
    rise = part.find_all('td')[5].getText().split(' ')[:2]
    sunrise = rise[0] + ' ' + rise[1][:-1]
    sunset = set[0] + ' ' + set[1][:-1]
    return sunrise, sunset

def createEmbed(title, description, link):
    embed = discord.Embed(
        title=title,
        description= description,
        colour=discord.Colour.blue()
    )
    embed.set_image(url=link)
    return embed
