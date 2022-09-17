from typing import List
from tkinter import Tk, Frame
from tkinter import Entry, Label, Button
from tkinter import CENTER

from datetime import timedelta
import subprocess
import os


class Ff:
    """The class responsible for work with library ffmpeg and ffprobe"""
    @classmethod
    def __run(self, cmd: List[str]):
        subprocess.call(cmd, stderr=subprocess.STDOUT)

    @classmethod
    def get_video_duration(self, fp: str) -> float:
        """Func to get info about video duration

        Args:
            fp (str): path to file. Example: "path/to/file/example.mp4"

        Returns:
            float: video duration in seconds
        """
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", fp],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)

    @classmethod
    def download(self, url: str, fp: str, start: float = None, stop: float = None, codec_copy: bool = True):
        """Func to get video or audio from URL link by using ffmpeg library

        Args:
            url (str): URL link to content.
            fp (str): Path to file where it will be saved. Example: "path/to/file/example.mp4".
            start (float, optional): Gets in secconds. Starting position from where will be start saving content. Defaults to None.
            stop (float, optional): Gets in secconds. Ending position from where will be stop saving content. Defaults to None.
            codec_copy (bool, optional): Keep current encoding. If codec_copy false then it will encode to the most common encoding. Defaults to True.
        """
        cmd = ['ffmpeg', '-y']
        if start:
            cmd += ['-ss', str(start)]
        if stop:
            cmd += ['-to', str(stop)]
        cmd += ['-i', url]
        if codec_copy:
            cmd += ['-codec', 'copy']
        cmd.append(fp)
        self.__run(cmd)

    @classmethod
    def merge(self, fp: str, *args):
        """Simplest merging of video and audio

        Args:
            fp (str): Path to file where it will be saved new file.
            *args (str): Path to files to merge.
        """
        cmd = ['ffmpeg', '-y']
        for file in args:
            cmd += ['-i', file]
        cmd += ['-codec', 'copy', fp]

        self.__run(cmd)


class Core(Ff):
    """Child class Ff. Responsible for downloading files from YouTube"""
    OUTPUT = 'output'

    def __init__(self) -> None:
        if not os.path.isdir(self.OUTPUT):
            os.makedirs(self.OUTPUT)

    def get_youtube_links(self, url: str) -> List[str]:
        """Func to get source URL link to video and audio

        Args:
            url (str): link to video on YouTube

        Returns:
            List[str]: List[0] is video, List[1] is audio
        """
        proc = subprocess.Popen(['yt-dlp', '-f',
                                 "(bestvideo+bestaudio/best)[protocol!*=dash]",
                                 '-g', url],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, err = proc.communicate()
        links = out.decode().split('\n')
        return links

    def download_video(self, link: str, name: str, start: float = None, stop: float = None) -> str:
        name = f'{self.OUTPUT}/{name}_video.webm'
        self.download(link, name, start, stop)
        return name

    def download_audio(self, link: str, name: str, start: float = None, stop: float = None) -> str:
        name = f'{self.OUTPUT}/{name}_audio.webm'
        self.download(link, name, start, stop, codec_copy=False)
        return name


def fix_start(video: str, stop: float) -> float:
    """Video downloaded from Core.download_video haven't strict border.
    This func fix length to audio track

    Args:
        video (str): Path to file
        stop (float): Gets in secconds. Ending position from where will be stop saving content.

    Returns:
        float: New start position from where will be start saving content.
    """
    duration = Ff.get_video_duration(video)
    return stop - duration


def time_to_sec(times: str = None) -> float:
    '''
    set times as '00:00:00.000' format 'HH:MM:SS.ms'
    examples:
    01:12 -> MM:SS
    01:23:31 -> HH:MM:SS
    12 -> SS
    '''
    if not times:
        return

    times = times.split(':')
    h = m = s = 0
    if len(times) == 3:
        h, m, s = times
    elif len(times) == 2:
        m, s = times
    elif len(times) == 1:
        s = times[0]
    t = timedelta(hours=int(h), minutes=int(m), seconds=float(s))

    return t.total_seconds()


def delete_files(*args):
    for file in args:
        os.remove(file)


class Window(Tk):
    OUTPUT = 'output'

    def __init__(self):
        self.core = Core()

        Tk.__init__(self)
        self.title("Scissors")
        self.geometry('236x200')
        self.resizable()
        self.setUI()

        self.content = {}

    def setUI(self):
        self.frame_select = Frame(self)
        self.frame_select.grid(column=0, row=0, pady=5)

        Label(self.frame_select, text='Ссылка на видео:').grid(column=0, row=0)
        self.entry = Entry(self.frame_select, width=35, justify=CENTER)
        self.entry.grid(column=0, row=1, ipadx=5, padx=5, pady=5)
        # self.set_text('Ссылка на видео')

        self.frame_timing = Frame(self)
        self.frame_timing.grid(column=0, row=2, pady=5)

        Label(self.frame_timing, text=' Старт:').grid(column=0, row=0)
        self.start_pos = Entry(self.frame_timing, width=10, justify=CENTER)
        self.start_pos.grid(column=1, row=0, padx=5)

        Label(self.frame_timing, text="Стоп:").grid(column=2, row=0, padx=5)
        self.end_pos = Entry(self.frame_timing, width=10, justify=CENTER)
        self.end_pos.grid(column=3, row=0)

        self.frame_name = Frame(self)
        self.frame_name.grid(column=0, row=3)
        Label(self.frame_name, text="Название видео:").grid(column=0, row=0)
        self.video_name = Entry(self.frame_name, width=21, justify=CENTER)
        self.video_name.grid(column=1, row=0, pady=5)

        self.confirm_button = Button(self, text='Вырезать', command=self.make)
        self.confirm_button.grid(column=0, row=5, pady=5)

    def make(self):
        links = self.core.get_youtube_links(self.entry.get())

        start = time_to_sec(self.start_pos.get())
        stop = time_to_sec(self.end_pos.get())

        name = self.video_name.get()
        video = self.core.download_video(links[0], name, start, stop)

        start = fix_start(video, stop)
        audio = self.core.download_audio(links[1], name, start, stop)

        output_name = f'{self.core.OUTPUT}/{name}.webm'
        self.core.merge(f'{output_name}', video, audio)
        delete_files(video, audio)


if __name__ == '__main__':
    root = Window()
    root.mainloop()
