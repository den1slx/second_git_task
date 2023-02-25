import requests
import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote
from dotenv import load_dotenv


def downloader(path, url, name='0', format='.txt', token=None):
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
        with open(f'{path}/{name}{format}', 'wb') as picture:
            picture.write(response.content)
    except requests.exceptions.HTTPError:
        try:
            with open(f'{path}/bad_links.txt', 'x') as txt:
                txt.write(f'{url}\n')
        except FileExistsError:
            with open(f'{path}/bad_links.txt', 'a') as txt:
                txt.write(f'{url}\n')


def create_dates_archive(path, token):
    response = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/all?api_key={token}'
    )
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    with open(f'{path}/archive_dates.txt', 'w') as dates:
        text = response.text
        dates.write(text)


def fetch_spacex_last_launch(
    path='latest_launch',
    id='latest',
    name='SpaceX_',
):
    url = f'https://api.spacexdata.com/v5/launches/{id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        links = response.json()['links']['flickr']['original']
        for index, link in enumerate(links):
            format = get_file_format_and_name(link)[0]
            downloader(path, link, name=f'{name}{index}', format=format)
    except requests.exceptions.HTTPError:
        pass


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
        format, name = get_file_format_and_name(url)
        print(url)
        downloader(
            path,
            url,
            name=name,
            format=format,
            token=token,
        )


def get_file_format_and_name(url):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    tail = os.path.split(path)[1]
    name, format = os.path.splitext(tail)
    return format, name


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='your path where to save',
    )
    parser.add_argument(
        '-d',
        '--date',
        help='date formate YYYY-MM-DD'
    )
    parser.add_argument(
        '-a',
        '--archive',
        help='create archive_dates.txt with available dates',
        action='store_true'
    )
    parser.add_argument(
        '--id',
        help='launch id',
        default='latest'
    )

    return parser


def main():
    load_dotenv()
    token = os.environ['NASA_TOKEN']
    parser = create_parser()
    namespace = parser.parse_args()
    fetch_spacex_last_launch(path=f'{namespace.path}/launch_{namespace.id}', id=namespace.id)
    epic_images(
        f'{namespace.path}/epic/{namespace.date}',
        namespace.date,
        token,
    )
    if namespace.archive is True:
        create_dates_archive(namespace.path, token)


if __name__ == '__main__':
    main()
