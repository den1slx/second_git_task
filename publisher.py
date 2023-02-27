import os
import telegram
from dotenv import load_dotenv
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'name',
        help='file name',
    )
    parser.add_argument(
        '-p',
        '--period',
        help='If not indicated: ignore files without period in name, where name is file_name+file_extend.',
        action='store_true',
    )
    return parser


def publisher(token, chat_id, path, image, period=True):
    bot = telegram.Bot(token=token)
    if period is True:
        if '.' in image:
            with open(f'{path}\\{image}', 'rb') as foto:
                bot.send_photo(chat_id=chat_id, photo=foto)
        else:
            pass
    else:
        with open(f'{path}\\{image}', 'rb') as foto:
            bot.send_photo(chat_id=chat_id, photo=foto)


def main():
    load_dotenv()
    parser = create_parser()
    namespace = parser.parse_args()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    publisher(token, chat_id, path, namespace.name, namespace.period)


if __name__ == '__main__':
    main()
