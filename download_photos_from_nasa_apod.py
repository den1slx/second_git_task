import os
import requests
import argparse
import datetime
from contextlib import suppress
from dotenv import load_dotenv
from downloader import fetch_file, get_name_and_extension_file


def get_current_date():
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    return today


def get_images_at_quantity_from_apod(path, token, count, hd=False):
    url = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': token,
        'count': count,
    }
    mod = ''
    if hd:
        mod = 'hd'
        path = f'{path}/apod_images/{mod}'
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


def get_image_from_apod_by_date(path, token, date, hd=False):
    url = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': token,
        'date': date,
    }
    mod = ''
    if hd:
        mod = 'hd'
        path = f'{path}/apod_images/{mod}'
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


def get_images_from_apod_from_date_to_date(path, token, start_date=None, end_date=get_current_date(), hd=False):
    url = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': token,
        'start_date': start_date,
        'end_date': end_date,
    }
    mod = ''
    if hd:
        mod = 'hd'
        path = f'{path}/apod_images/{mod}'
    response = requests.get(url, headers)
    response.raise_for_status()
    photos = response.json()
    for photo in photos:
        name, extension = get_name_and_extension_file(photo[f'{mod}url'])
        fetch_file(
            path,
            photo[f'{mod}url'],
            name=f'{mod}{name}',
            extension=extension,
        )


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
        help='end_date used with start_date. default end_date=today',
        default=get_current_date(),
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
    parser = create_parser()
    namespace = parser.parse_args()
    count, hd = namespace.count, namespace.hd
    date, start_date, end_date = namespace.date, namespace.start_date, namespace.end_date
    with suppress(requests.exceptions.HTTPError):
        if count:
            get_images_at_quantity_from_apod(path, token, count, hd=hd)
        elif date:
            get_image_from_apod_by_date(path, token, date, hd=hd)
        elif start_date:
            get_images_from_apod_from_date_to_date(path, token, start_date=start_date, end_date=end_date, hd=hd)


if __name__ == '__main__':
    main()
