from random import shuffle
from publisher import publisher, adress_names
import os
from time import sleep
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    try:
        path = os.environ['PATH_TO_FILES']
        sleeptime = int(os.environ['PUBLISH_TIME'])
    except KeyError:
        sleeptime = 14400
    fullpaths = adress_names(path)
    while True:
        shuffle(fullpaths)
        for path, name in fullpaths:
            publisher(token, chat_id, path, name)
            sleep(sleeptime)


if __name__ == '__main__':
    main()
