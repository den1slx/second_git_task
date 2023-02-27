# Загрузка и публикация изображений



## Установка
Должен быть .env файл содержащий переменные:  
  * TG_TOKEN='ваш токен бота Telegram'  
  * NASA_TOKEN='ваш токен'  
  * PATH_TO_FILES='абсолютный путь к создаваемой директории'  
  * PUBLISH_TIME='количество секунд между публикациями'  
  * CHAT_ID='id чата в Telegram'   


Токен должен быть получен из окружения. (.env файл должен содержать переменную NASA_TOKEN='ваштокен')  
Получите токен NASA [здесь](https://api.nasa.gov/) и запишите его в переменную NASA_TOKEN.


Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## main.py

Публикует в телеграм картинки по одной через каждые PUBLISH_TIME секунд, из списка файлов в директории PATH_TO_FILES и вложенных директорий.

Использует TG_TOKEN, CHAT_ID, PATH_TO_FILES, PUBLISH_TIME.
Не принимает аргументы.

### Использование

Укажите значения TG_TOKEN, CHAT_ID, PATH_TO_FILES, PUBLISH_TIME
нужные вам и запустите скрипт.

```
python main.py
```


### Использование

## Скачиваем картинки с помощью [NASA](https://api.nasa.gov/).
#### download_photos_from_nasa_epic
Здесь задействуются NASA_TOKEN и PATH_TO_FILES.


* Получаем подсказку
```
python download_photos_from_nasa_epic.py -h
```

* Получаем текстовый файл с датами.  

```
python download_photos_from_nasa_epic.py -a
```
* Скачиваем картинки.
Используем любую дату из файла с датами
и скачиваем все картинки за эту дату
```
python download_photos_from_nasa_epic.py -d 2023-02-24
```

#### download_photos_from_nasa_epic

Здесь задействуются NASA_TOKEN и PATH_TO_FILES

* Получаем подсказку
```
python download_photos_from_nasa_apod.py -h
```
* Скачиваем картинку за указанную дату:
```
python download_photos_from_nasa_apod.py -d 2023-02-24
```
* Скачиваем картинки за указанный промежуток дат:
```
python download_photos_from_nasa_apod.py -sd 2023-02-20 -ed 2023-02-24
```
* Скачиваем заданное количество случайных картинок
```
python download_photos_from_nasa_apod.py -c 5
```

Могут быть скачаны файлы без расширения, если их открыть в блокноте в конце файла будет ссылка на видео.
Возможно позже это будет исправлено.



## Downloads photo from SpaceX

Скачиваем фото по id запуска


### Использование
Здесь используется PATH_TO_FILES

Указываем id
```
python fetch_spacex_images.py --id 5eb87d0effd86e000604b35c
```
Чтобы скачать фото последнего запуска указываем только путь:
```
python fetch_spacex_images.py
```
* Не в каждом запуске делаются фото
* Фото берутся из 
```
response.json()['links']['flickr']['original']
```
Фото из других мест игнорируются

## downloader

содержит функции:
* *get_file_extend*
* *get_file_name*
* *downloader*

Используется как колбэк в 
* download_photos_from_nasa_epic.py 
* download_photos_from_nasa_apod.py
* fetch_spacex_images.py

## publisher

Использует TG_TOKEN, CHAT_ID, PATH_TO_FILES.
Здесь PATH_TO_FILES - абсолютный путь к вашакартинка.jpg.

### Использование

Ваш бот публикует картинку в телеграм.
```
python publisher.py вашакартинка.jpg
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).