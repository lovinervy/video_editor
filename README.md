# Video Editor
## Пример работы: [YouTube](https://youtu.be/6GmllC1heTE)
&nbsp;

## Установка
&nbsp;
### Windows

1. Установить [Python](https://python.org), во время установки обязательно поставить галочку на "Add To PATH..."

2. Скачать скрипты 
    * Нажать на этой странице сверху на зеленую кнопку ```Code```
    * Скачать zip архив
    * Расспаковать архив в удобном для вас месте

3. Скачать архив [ffmpeg-git-full.7z](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) и извлечь от туда ffmpeg.exe и ffprobe.exe из директории ```bin``` и положить в корень директории ```video_editor```

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
python scissors.py
``` 
* Склейка роликов (У всех видео должен быть одна и та же кодировка)
```
python concat.py
```

### Linux / Ubuntu
1. Установить Python
```bash
sudo apt install python3 
```
2. Установить Git
```bash
sudo apt install git 
```
3. Скачать репозиторию
```bash
git clone https://github.com/lovinervy/video_editor.git
```
4. Настройка скрипта
```bash
cd video_editor/
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install yt-dlp
```
5. Запуск скрипта
```bash
source .venv/bin/activate
python scissors.py
```
