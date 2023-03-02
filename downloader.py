import requests
import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote


def fetch_file(path, url, name=None, extension=None, token=None):
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    headers = {
        'api_key': token,
    }
    response = requests.get(url, headers)
    response.raise_for_status()
    with open(f'{path}/{name}{extension}', 'wb') as picture:
        picture.write(response.content)


def create_bad_links_log(path, url):
    with open(f'{path}/bad_links.txt', 'a') as txt:
        txt.write(f'{url}\n')


def get_name_and_extension_file(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    head, tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    return name, extension


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
    name, extension = namespace.name, namespace.extension
    default_name, default_extension = get_name_and_extension_file(namespace.url)
    if not name:
        name = default_name
    if not extension:
        extension = default_extension
    try:
        fetch_file(
            namespace.path,
            namespace.url,
            name,
            extension,
            namespace.token,
        )
    except requests.exceptions.HTTPError:
        create_bad_links_log(namespace.path, namespace.url)


if __name__ == '__main__':
    main()
