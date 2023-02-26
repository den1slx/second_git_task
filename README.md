# Download photos
be added later



## Установка

Токен должен быть получен из окружения. (.env файл должен содержать переменную NASA_TOKEN='ваштокен')  
Получите токен [здесь](https://api.nasa.gov/) и запишите его в переменную NASA_TOKEN.


Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


## Использование

* Получаем подсказку
```
python download_photos_from_nasa.py -h
```
#### Download photos from NASA
Скачиваем картинки с помощью [NASA](https://api.nasa.gov/)

* Получаем текстовый файл с датами.  
**Всегда** указываем путь куда сохраняем файл
```
python download_photos_from_nasa.py new_folder -a
```
* Скачиваем картинки.
Используем любую дату из файла с датами
и скачиваем все картинки за эту дату
```
python download_photos_from_nasa.py new_folder -d 2023-02-24
```

#### Downloads photo from SpaceX
Скачиваем фото по id запуска

## Использование

Указываем путь и id
```
python fetch_spacex_images.py new_folder --id 5eb87d0effd86e000604b35c
```
Чтобы скачать фото последнего запуска указываем только путь:
```
python fetch_spacex_images.py new_folder
```
* Не в каждом запуске делаются фото

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).