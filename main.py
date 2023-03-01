from random import shuffle
from publisher import publisher, get_full_way
import os
from time import sleep
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    try:
        sleeptime = int(os.environ['PUBLISH_TIME'])
    except KeyError:
        sleeptime = 14400
    fullpaths = get_full_way(path)
    while True:
        shuffle(fullpaths)
        for path, name in fullpaths:
            publisher(token, chat_id, path, name)
            sleep(sleeptime)


if __name__ == '__main__':
    main()
