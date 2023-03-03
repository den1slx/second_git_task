import os
import requests
import argparse
import datetime
from contextlib import suppress
from pathlib import PurePath
from dotenv import load_dotenv
from downloader import fetch_file, get_name_and_extension_file


def get_current_date():
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    return today


def get_images_from_apod(path, headers, url, boolean_hd=False):
    mod = get_hd_mod(boolean_hd)
    path = PurePath(path).joinpath('apod_images').joinpath(mod)
    response = requests.get(url, headers)
    response.raise_for_status()
    links = response.json()
    for link in links:
        url = link[f'{mod}url']
        name, extension = get_name_and_extension_file(url)
        fetch_file(
            path,
            url,
            name=name,
            extension=extension,
        )


def get_image_at_date_from_apod(path, headers, url, boolean_hd=False):
    mod = get_hd_mod(boolean_hd)
    path = PurePath(path).joinpath('apod_images').joinpath(mod)
    response = requests.get(url, headers)
    response.raise_for_status()
    today_photo = response.json()[f'{mod}url']
    name, extension = get_name_and_extension_file(today_photo)
    fetch_file(
        path,
        today_photo,
        name=name,
        extension=extension,
    )


def get_hd_mod(boolean):
    mod = ''
    if boolean:
        mod = 'hd'
    return mod


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--count',
        help='int count. Cannot be used with date or start_date and end_date.',
        type=int,
        default=None,
    )
    parser.add_argument(
        '-d',
        '--date',
        default=None,
        help='date format YYYY-MM-DD'
    )
    parser.add_argument(
        '-sd',
        '--start_date',
        help='''start_date used with end_date. default end_date=today.
         The start of a date range, when requesting date for a range of dates.
         Cannot be used with date.''',
        default=None,
    )
    parser.add_argument(
        '-ed',
        '--end_date',
        help='end_date used with start_date. default today',
        default=None,
    )
    parser.add_argument(
        '--hd',
        help='if indicated download hd version',
        action='store_true',
    )
    return parser


def main():
    load_dotenv()
    token = os.environ['NASA_TOKEN']
    path = os.environ['PATH_TO_FILES']
    url = 'https://api.nasa.gov/planetary/apod'
    parser = create_parser()
    namespace = parser.parse_args()
    count, hd = namespace.count, namespace.hd
    date, start_date, end_date = namespace.date, namespace.start_date, namespace.end_date
    if start_date and not end_date:
        end_date = get_current_date()
    headers = {
        'api_key': token,
        'count': count,
        'date': date,
        'start_date': start_date,
        'end_date': end_date,
    }
    with suppress(requests.exceptions.HTTPError):
        if date:
            get_image_at_date_from_apod(path, headers, url, hd)
        else:
            get_images_from_apod(path, headers, url, hd)


if __name__ == '__main__':
    main()
