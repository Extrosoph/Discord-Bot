from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
def getTemp():
    url = 'https://www.weather.com.au/wa/perth/current'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(uClient).read()
    webpage = webpage.decode('utf-8')
    webpage = webpage.split('\n')
    temp = 0
    for i in range(len(webpage)):
        if '>Temperature<' in webpage[i]:
            temp = float(webpage[i+1].split('&')[0].split('>')[1])
    return temp

def getStatus():
    url = 'https://www.weather.com.au/wa/perth/current'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(uClient).read()
    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    part = soup.find('div', {'id':'currentIcon'})
    status = part.find('p').getText()
    link = part.find('img')['src']
    return link, status
