import os
import telegram
from dotenv import load_dotenv
import argparse
from pathlib import PurePath


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'name',
        help='file name',
    )
    parser.add_argument(
        '-p',
        '--period',
        help='If not indicated: ignore files without period in name, where name is file_name+file_extension.',
        action='store_true',
    )
    return parser


def get_full_ways(path, boolean=True):
    names = os.walk(path)
    paths = []
    for adress, dirs, files in names:
        for names in files:
            if boolean and '.' in names:
                paths.append((adress, names))
            else:
                paths.append((adress, names))
    return paths


def send_image(token, chat_id, path, image_name_extension, boolean=True):
    bot = telegram.Bot(token=token)
    fullpath = PurePath(path).joinpath(image_name_extension)
    if boolean and '.' in image_name_extension and '.txt' not in image_name_extension:
        with open(fullpath, 'rb') as foto:
            bot.send_photo(chat_id=chat_id, photo=foto)
    else:
        with open(fullpath, 'rb') as foto:
            bot.send_photo(chat_id=chat_id, photo=foto)


def main():
    load_dotenv()
    parser = create_parser()
    namespace = parser.parse_args()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    send_image(token, chat_id, path, namespace.name, namespace.period)


if __name__ == '__main__':
    main()
