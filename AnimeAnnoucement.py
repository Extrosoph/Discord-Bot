from urllib.request import Request, urlopen
from urllib.error import HTTPError
import os.path

'''Get the episode from the website using a Get request'''
def getEpisodes(anime):
    #Webscraping
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
    webpage = webpage.split('\n')

    episodes = []
    # Get the episodes
    for line in webpage:
        if 'title="Episode ' in line:
            try:
                episode = int(line.partition("Episode")[2].partition('"')[0])
                episodes.append(episode)
            except:
                continue
    return episodes

'''Check for new anime episode'''
def checkNewEpisode(anime):
    # Check if logger file exists
    name = anime.replace(' ', '-')
    file_name = name+'.txt'
    file_exists = os.path.exists(file_name)
    if file_exists:
        with open(file_name, 'r+') as logger:
            newEpisodes = getEpisodes(name)
            newEpisodes.reverse()
            oldEpisodes = logger.readline()
            oldEpisodes = oldEpisodes.split(',')[:-1]
            for i in range(len(oldEpisodes)):
                oldEpisodes[i] = int(oldEpisodes[i])
            if oldEpisodes[-1] != newEpisodes[-1]:
                logger.write(str(newEpisodes[-1]) + ',')
                return newEpisodes[-1]

    else:
        with open(file_name, 'w') as logger:
            newEpisodes = getEpisodes(name)
            newEpisodes.reverse()
            for episodes in newEpisodes:
                logger.write(str(episodes) + ',')
    return False
    logger.close()

