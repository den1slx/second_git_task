from random import shuffle
from publisher import send_image, get_full_ways
import os
from time import sleep
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    sleeptime = int(os.getenv('PUBLISH_TIME', default='14400'))
    fullpaths = get_full_ways(path)
    while True:
        shuffle(fullpaths)
        for path, name in fullpaths:
            send_image(token, chat_id, path, name)
            sleep(sleeptime)


if __name__ == '__main__':
    main()
