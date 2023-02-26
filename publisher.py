import os
import telegram
from dotenv import load_dotenv
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='file name')
    return parser


def publisher(token, chat_id, path, image):
    bot = telegram.Bot(token=token)
    if '.' in image:
        with open(f'{path}\\{image}', 'rb') as foto:
            bot.send_photo(chat_id=chat_id, photo=foto)
    else:
        pass


def main():
    load_dotenv()
    parser = create_parser()
    namespace = parser.parse_args()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    publisher(token, chat_id, path, namespace.name)


if __name__ == '__main__':
    main()
