import os
import telegram


def main():
    token = os.environ['TG_TOKEN']
    bot = telegram.Bot(token=token)
    chat_id = '@channerfortest'
    path = r'C:\Users\Денис\Projects\devman tasks\second_git_task\new_folder\apod_images'
    image = '2016-12-11T173502JunoPerijove3Peach1024.jpg'
    with open(f'{path}\\{image}', 'rb') as foto_1:
        bot.send_photo(chat_id=chat_id, photo=foto_1)


if __name__ == '__main__':
    main()
