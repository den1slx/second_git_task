import requests
import argparse
import os
from contextlib import suppress
from pathlib import Path
from dotenv import load_dotenv
from downloader import fetch_file, get_name_and_extension_file


def create_dates_archive(path, token):
    params = {'api_key': token}
    response = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/all',
        params=params,
    )
    images = Path(path)
    images.mkdir(parents=True, exist_ok=True)
    with open(f'{path}/archive_dates.txt', 'w') as dates:
        text = response.text
        dates.write(text)


def get_images_from_epic(path, date, token):
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    headers = {
        'api_key': token,
    }
    response = requests.get(url, headers)
    links = response.json()
    for link in links:
        image = link['image']
        date, *unused = link['date'].split()
        date = date.replace('-', '/')
        url = f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png'
        name, extension = get_name_and_extension_file(url)
        fetch_file(
            path,
            url,
            name=name,
            extension=extension,
            token=token,
        )


def create_parser():
    parser = argparse.ArgumentParser()
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
    path = os.environ['PATH_TO_FILES']
    token = os.environ['NASA_TOKEN']
    parser = create_parser()
    namespace = parser.parse_args()
    with suppress(requests.exceptions.HTTPError):
        get_images_from_epic(
            f'{path}/epic/{namespace.date}',
            namespace.date,
            token,
        )
        if namespace.archive:
            create_dates_archive(path, token)


if __name__ == '__main__':
    main()
