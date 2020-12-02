from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os.path

"""Get the episode from the website using a Get request"""
def getEpisodes(anime):
    url = 'https://animeheaven.ru/detail/' + anime + '-TV'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        webpage = urlopen(uClient).read()
    except HTTPError as err:
        if err.code == 404:
            url = 'https://animeheaven.ru/detail/'+anime
            uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(uClient).read()

    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    part = soup.find('div', class_='infopicbox')
    link = part.find('img')['src']
    part2 = soup.find('div', class_='infoepbox')
    episodeList = part2.find_all('a')
    episodes = []
    for line in episodeList:
        try:
            episode = int(line['title'].split(' ')[-1])
            episodes.append(episode)
        except:
            pass
    return episodes, link

"""Check for new anime episode"""
def checkNewEpisode(anime):
    # Check if logger file exists
    name = anime.replace(' ', '-')
    file_name = name+'.txt'
    file_exists = os.path.exists(file_name)
    if file_exists:
        with open(file_name, 'r+') as logger:
            newEpisodes, link = getEpisodes(name)
            newEpisodes.reverse()
            oldEpisodes = logger.readline()
            oldEpisodes = oldEpisodes.split(',')[:-1]
            for i in range(len(oldEpisodes)):
                oldEpisodes[i] = int(oldEpisodes[i])
            if oldEpisodes[-1] != newEpisodes[-1]:
                logger.write(str(newEpisodes[-1]) + ',')
                logger.close()
                return newEpisodes[-1], link

    else:
        with open(file_name, 'w') as logger:
            newEpisodes, link = getEpisodes(name)
            newEpisodes.reverse()
            for episodes in newEpisodes:
                logger.write(str(episodes) + ',')
            logger.close()
    return False, link

