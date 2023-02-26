import requests
import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote


def downloader(path, url, name, extend, token=None):
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    try:
        if token is None:
            response = requests.get(url)
        else:
            headers = {
                'api_key': token,
            }
            response = requests.get(url, headers)
        response.raise_for_status()
        with open(f'{path}/{name}{extend}', 'wb') as picture:
            picture.write(response.content)
    except requests.exceptions.HTTPError:
        try:
            with open(f'{path}/bad_links.txt', 'x') as txt:
                txt.write(f'{url}\n')
        except FileExistsError:
            with open(f'{path}/bad_links.txt', 'a') as txt:
                txt.write(f'{url}\n')


def get_file_extend(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    tail = os.path.split(path)[1]
    extend = os.path.splitext(tail)[1]
    return extend


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
        'path',
        help='your path where to save',
    )
    parser.add_argument(
        'url',
        help='date formate YYYY-MM-DD',
        default='0000-00-00'
    )
    parser.add_argument(
        '-n',
        '--name',
        help='Name downloading file',
        default=get_file_name(parser.parse_args().url),
    )
    parser.add_argument(
        'extend',
        help='extend downloading file',
        default=get_file_extend(parser.parse_args().url)
    )
    parser.add_argument(
        '-t',
        '--token',
        help='Your token. If not indicate ignored.',
        default=None,
    )
    return parser


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    downloader(
        namespace.path,
        namespace.url,
        namespace.name,
        namespace.extend,
        namespace.token,
    )
    pass


if __name__ == '__main__':
    main()
