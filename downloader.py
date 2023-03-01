import requests
import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote


def load_file(path, url, name=None, extension=None, token=None):
    if not name:
        name = get_file_name(url)
    if not extension:
        extension = get_file_extension(url)
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    try:
        if not token:
            response = requests.get(url)
        else:
            headers = {
                'api_key': token,
            }
            response = requests.get(url, headers)
        response.raise_for_status()
        with open(f'{path}/{name}{extension}', 'wb') as picture:
            picture.write(response.content)
    except requests.exceptions.HTTPError:
        try:
            with open(f'{path}/bad_links.txt', 'x') as txt:
                txt.write(f'{url}\n')
        except FileExistsError:
            with open(f'{path}/bad_links.txt', 'a') as txt:
                txt.write(f'{url}\n')


def get_file_extension(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    tail = os.path.split(path)[1]
    extension = os.path.splitext(tail)[1]
    return extension


def get_file_name(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    tail = os.path.split(path)[1]
    name = os.path.splitext(tail)[0]
    return name


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        help='your url',
    )
    parser.add_argument(
        'path',
        help='path to save',
    )
    parser.add_argument(
        'name',
        help='Name downloading file',
    )
    parser.add_argument(
        'extension',
        help='extension downloading file',
    )
    parser.add_argument(
        '-t',
        '--token',
        help='Your token. If not indicate ignored.',
    )
    return parser


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    load_file(
        namespace.path,
        namespace.url,
        namespace.name,
        namespace.extension,
        namespace.token,
    )


if __name__ == '__main__':
    main()
