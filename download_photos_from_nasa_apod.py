import os
import requests
import argparse
import datetime
from dotenv import load_dotenv
from downloader import load_file, get_file_name, get_file_extension


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
        extension = get_file_extension(url)
        name = get_file_name(url)
        load_file(
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
    extension = get_file_extension(today_photo)
    name = get_file_name(today_photo)
    load_file(
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
        extension = get_file_extension(photo[f'{mod}url'])
        name = get_file_name(photo[f'{mod}url'])
        load_file(
            path,
            photo[f'{mod}url'],
            name=f'{mod}{name}',
            extension=extension,
        )


def pick_by_args(
        path,
        token,
        count=None,
        date=None,
        start_date=None,
        end_date=get_current_date(),
        hd=False,
):
    if count:
        get_images_at_quantity_from_apod(path, token, count, hd=hd)
    elif date:
        get_image_from_apod_by_date(path, token, date, hd=hd)
    elif start_date:
        get_images_from_apod_from_date_to_date(path, token, start_date=start_date, end_date=end_date, hd=hd)


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
    try:
        pick_by_args(
            path,
            token,
            namespace.count,
            namespace.date,
            namespace.start_date,
            namespace.end_date,
            namespace.hd,
        )
    except requests.exceptions.HTTPError:
        pass


if __name__ == '__main__':
    main()
