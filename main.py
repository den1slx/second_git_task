import requests
import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote
from dotenv import load_dotenv
from downloader import downloader


def create_dates_archive(path, token):
    response = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/all?api_key={token}'
    )
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    with open(f'{path}/archive_dates.txt', 'w') as dates:
        text = response.text
        dates.write(text)


def epic_images(path, date, token):
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    headers = {
        'api_key': token,
    }
    response = requests.get(url, headers)
    links = response.json()
    for link in links:
        image = link['image']
        date = link['date'].split()[0]
        date = date.replace('-', '/')
        url = f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png'
        extend, name = get_file_format_and_name(url)
        downloader(
            path,
            url,
            name=name,
            extend=extend,
            token=token,
        )


def get_file_format_and_name(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    tail = os.path.split(path)[1]
    name, extend = os.path.splitext(tail)
    return extend, name


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='your path where to save',
    )
    parser.add_argument(
        '-d',
        '--date',
        help='date formate YYYY-MM-DD',
        default='0000-00-00'
    )
    parser.add_argument(
        '-a',
        '--archive',
        help='create archive_dates.txt with available dates',
        action='store_true'
    )
    return parser


def main():
    load_dotenv()
    token = os.environ['NASA_TOKEN']
    parser = create_parser()
    namespace = parser.parse_args()
    epic_images(
        f'{namespace.path}/epic/{namespace.date}',
        namespace.date,
        token,
    )
    if namespace.archive is True:
        create_dates_archive(namespace.path, token)


if __name__ == '__main__':
    main()
