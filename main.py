from random import shuffle
from publisher import publisher
import os
from time import sleep
from dotenv import load_dotenv


def adress_names(path, period=True):
    names = os.walk(path)
    paths = []
    for adress, dirs, files in names:
        for names in files:
            if period is True:
                if '.' in names:
                    paths.append((adress, names))
                else:
                    pass
            else:
                paths.append((adress, names))
    return paths


def main():
    load_dotenv()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    sleeptime = int(os.environ['PUBLISH_TIME'])
    fullpaths = adress_names(path)
    while True:
        shuffle(fullpaths)
        for path, name in fullpaths:
            publisher(token, chat_id, path, name)
            sleep(sleeptime)


if __name__ == '__main__':
    main()
