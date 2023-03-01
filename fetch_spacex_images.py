import os
from dotenv import load_dotenv
import requests
import argparse
from downloader import load_file, get_file_extension


def fetch_spacex_last_launch(
    path,
    launch_id,
    name='SpaceX_',
):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    path = f'{path}//launch//{launch_id}'
    response = requests.get(url)
    response.raise_for_status()
    links = response.json()['links']['flickr']['original']
    for index, link in enumerate(links):
        extension = get_file_extension(link)
        load_file(path, link, name=f'{name}{index}', extension=extension)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-id',
        '--id',
        help='launch id',
        default='latest'
    )
    return parser


def main():
    load_dotenv()
    parser = create_parser()
    spacename = parser.parse_args()
    path = os.environ['PATH_TO_FILES']
    try:
        fetch_spacex_last_launch(
            path,
            spacename.id,
        )
    except requests.exceptions.HTTPError:
        pass


if __name__ == '__main__':
    main()
