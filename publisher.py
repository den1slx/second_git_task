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
        '-e',
        '--exceptions',
        help='''It should not be in name. default=('.txt',)''',
        type=tuple,
        default=('.txt',),
    ),
    parser.add_argument(
        '-r',
        '--requirements',
        help='''It should be in name. default=('.',)''',
        type=tuple,
        default=('.',),
    )
    return parser


def get_full_ways(path, requirements=('.',), exceptions=''):
    names = os.walk(path)
    paths = []
    for adress, dirs, files in names:
        for names in files:
            if is_available_name(names, requirements=requirements, exceptions=exceptions):
                paths.append((adress, names))
    return paths


def is_available_name(name, exceptions='', requirements=''):
    boolean = True
    for exception in exceptions:
        if str(exception) in name:
            boolean = False
            break
    for requirement in requirements:
        if str(requirement) not in name:
            boolean = False
            break
    return boolean


def send_image(token, chat_id, path, image_name_extension, exceptions=('.txt',), requirements='.'):
    bot = telegram.Bot(token=token)
    fullpath = PurePath(path).joinpath(image_name_extension)
    if is_available_name(image_name_extension, exceptions=exceptions, requirements=requirements):
        with open(fullpath, 'rb') as foto:
            bot.send_photo(chat_id=chat_id, photo=foto)


def main():
    load_dotenv()
    parser = create_parser()
    namespace = parser.parse_args()
    token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    path = os.environ['PATH_TO_FILES']
    send_image(
        token,
        chat_id,
        path,
        namespace.name,
        exceptions=namespace.exceptions,
        requirements=namespace.requirements,
    )


if __name__ == '__main__':
    main()
