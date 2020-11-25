from urllib.request import Request, urlopen
import os.path

'''Get the episode from the website using a Get request'''
def getEpisodes():
    Jujutsu_Kaisen = 'https://animeheaven.ru/detail/Jujutsu-Kaisen-TV.53463'
    uClient = Request(Jujutsu_Kaisen, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(uClient).read()
    webpage = webpage.decode('utf-8')
    webpage = webpage.split('\n')

    episodes = []
    # Get the episodes
    for line in webpage:
        if 'title="Episode ' in line:
            try:
                episode = int(line.partition("Episode")[2][1])
                episodes.append(episode)
            except:
                continue
    return episodes

def checkNewEpisode():
    #Check if logger file exists
    file_exists = os.path.exists('Jujutsu-Kaisen.txt')
    if file_exists:
        with open('Jujutsu-Kaisen.txt', 'r+') as logger:
            newEpisodes = getEpisodes()
            newEpisodes.reverse()
            oldEpisodes = logger.readline()
            oldEpisodes = oldEpisodes.split(',')[:-1]
            for i in range(len(oldEpisodes)):
                oldEpisodes[i] = int(oldEpisodes[i])
            if oldEpisodes != newEpisodes:
                logger.write(str(newEpisodes[-1]) + ',')
                return newEpisodes[-1]

    else:
        with open('Jujutsu-Kaisen.txt', 'w') as logger:
            newEpisodes = getEpisodes()
            newEpisodes.reverse()
            for episodes in newEpisodes:
                logger.write(str(episodes)+',')
    return False

    logger.close()

