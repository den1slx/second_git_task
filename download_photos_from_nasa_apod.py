import os
import requests
import argparse
import datetime
from dotenv import load_dotenv
from downloader import downloader, get_file_name, get_file_extend


def is_today():
    today = datetime.date.today()
    today.strftime('%Y-%m-%d')
    return today


def apod_images(path, token, count=None, date=False, start_date=None, end_date=is_today(), hd=False):
    url = 'https://api.nasa.gov/planetary/apod'
    headers = {
        'api_key': token,
    }
    mod = ''
    if hd is True:
        mod = 'hd'
        path = f'{path}/apod_images/{mod}'
    else:
        path = f'{path}/apod_images'
    if count is True:
        headers['count'] = count
        response = requests.get(url, headers)
        response.raise_for_status()
        links_list = response.json()
        for link in links_list:
            extend = get_file_extend(link[f'{mod}url'])
            name = get_file_name(link[f'{mod}url'])
            downloader(
                path,
                link['{mod}url'],
                name=name,
                extend=extend,
            )
    elif date is True:
        headers['date'] = date
        response = requests.get(url, headers)
        today_photo = response.json()[f'{mod}url']
        extend = get_file_extend(today_photo)
        name = get_file_name(today_photo)
        downloader(
            path,
            today_photo,
            name=name,
            extend=extend,
        )
    elif start_date is not None:
        headers['start_date'] = start_date
        headers['end_date'] = end_date
        response = requests.get(url, headers)
        photos = response.json()
        for photo in photos:
            extend = get_file_extend(photo[f'{mod}url'])
            name = get_file_name(photo[f'{mod}url'])
            downloader(
                path,
                photo[f'{mod}url'],
                name=f'{mod}{name}',
                extend=extend,
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
        'path',
        help='path to save',
    )
    parser.add_argument(
        '-d',
        '--date',
        default=None,
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
        default=is_today(),
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
    parser = create_parser()
    namespace = parser.parse_args()
    apod_images(
        namespace.path,
        token,
        namespace.count,
        namespace.date,
        namespace.start_date,
        namespace.end_date,
        namespace.hd,
    )


if __name__ == '__main__':
    main()
