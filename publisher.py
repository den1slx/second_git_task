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
        '-u',
        '--unacceptable_name_parts',
        help='''It should not be in name. default=('.txt',)''',
        type=tuple,
        default=('.txt',),
    ),
    parser.add_argument(
        '-n',
        '--necessary_name_parts',
        help='''It should be in name. default=('.',)''',
        type=tuple,
        default=('.',),
    )
    return parser


def get_full_ways(path, necessary_name_parts=('.',), unacceptable_name_parts=''):
    names = os.walk(path)
    paths = []
    for adress, dirs, files in names:
        for names in files:
            if is_available_name(
                    names,
                    necessary_name_parts,
                    unacceptable_name_parts,
            ):
                paths.append((adress, names))
    return paths


def is_available_name(name, unacceptable_name_parts='', necessary_name_parts=''):
    """
Check if the name matches the conditions:
1) All elements 'unacceptable_name_parts' should not in name.
2) All elements 'necessary_name_parts' should in name.
    :param name: type=str. Verifiable name
    :param unacceptable_name_parts: type=tuple. If any of this in name: return False
    :param necessary_name_parts: type=tuple. If any of this not in name: return False
    :return: boolean
    """
    is_available = True
    for unacceptable_name_part in unacceptable_name_parts:
        if str(unacceptable_name_part) in name:
            is_available = False
            break
    for necessary_name_part in necessary_name_parts:
        if str(necessary_name_part) not in name:
            is_available = False
            break
    return is_available


def send_image(
        token,
        chat_id,
        path,
        image_name_extension,
        unacceptable_name_parts=('.txt',),
        necessary_name_parts=('.',),
):
    bot = telegram.Bot(token=token)
    fullpath = PurePath(path).joinpath(image_name_extension)
    if is_available_name(
            image_name_extension,
            unacceptable_name_parts=unacceptable_name_parts,
            necessary_name_parts=necessary_name_parts,
    ):
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
        unacceptable_name_parts=namespace.unacceptable_name_parts,
        necessary_name_parts=namespace.necessary_name_parts,
    )


if __name__ == '__main__':
    main()
