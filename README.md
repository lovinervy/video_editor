# Video Editor
## Пример работы: [YouTube]()
&nbsp;

## Усатновка
&nbsp;
### Windows

1. Установить [Python](https://python.org), во время установки обязательно поставить галочку на "Add To PATH..."

2. Скачать скрипты 
    * Нажать на этой странице сверху на зеленую кнопку ```Code```
    * Скачать zip архив
    * Расспаковать архив в удобном для вас месте

3. Скачать архив [ffmpeg-git-full.7z](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) и извлечь от туда ffmpeg.exe из директории ```bin``` и положить в папку ```Program``` в директории ```video_editor```

4. Запустить командную строку внутри ```video_editor``` 
5. Пишем следующие команды в командную строку
```cmd
pip install -U pip
pip install virtualenv
python -m venv venv
```
6. Активируем виртуальное окружение
```cmd
.\venv\Scripts\activate
```
7. Далее пишем команды
```
pip install -U pip
pip install yt-dlp
```
8. На этом все

Для того чтобы пользоваться, перед запуском всегда надо будет активировать виртуальное окружение (Пункт 6) затем уже запускать скрипт

Запуск скриптов
* Ножницы
```
python .\Scripts\scissors.py
``` 
* Склейка роликов (У всех видео должен быть одна и та же кодировка)
```
python .\Scripts\concat.py
```