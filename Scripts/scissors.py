from tkinter import Tk, Frame
from tkinter import Entry, Label, Button
from tkinter import CENTER, END
from tkinter.font import NORMAL

from datetime import timedelta
import subprocess
import os


def time_to_sec(times: str) -> float:
    '''
    set times as '00:00:00.000' format 'HH:MM:SS.ms'
    examples:
    01:12 -> MM:SS
    01:23:31 -> HH:MM:SS
    12 -> SS
    '''
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


class Core:
    OUTPUT = 'output'

    def __init__(self) -> None:
        self.low = False
        if not os.path.isdir(self.OUTPUT):
            os.makedirs(self.OUTPUT)

    def get_link(self, url) -> list:
        cmd = [
            'yt-dlp',
            '-f', "(bestvideo+bestaudio/best)[protocol!*=dash]",
            '-g', url
        ]
        
        links = []
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        links = out.decode().split('\n')
        return links

    def time_parsing(self, start: float, end: float):
        self.audio_timing = [start, end]

        time = []
        low_encoding = start % 5
        plus = 5 - low_encoding
        if low_encoding > 0:
            time += [start, plus + start]
            self.low = True
            time += [plus + start, end]
        else:
            time += [start, end]
        self.time = time

    def download_video(self, link: str, name: str) -> str:
        files = []
        if self.low:
            name_low = f'{self.OUTPUT}/{name}_low.webm'
            files.append(name_low)
            cmd = [
                'Program/ffmpeg', '-y',
                '-ss', str(self.time.pop(0)),
                '-to', str(self.time.pop(0)),
                '-i', link,
                name_low
            ]
            subprocess.call(cmd)
        
        name_std = f'{self.OUTPUT}/{name}_v.webm'
        files.append(name_std)
        cmd = [
            'Program/ffmpeg', '-y',
            '-ss', str(self.time.pop(0)),
            '-to', str(self.time.pop(0)),
            '-i', link,
            '-codec', 'copy',
            name_std
        ]
        subprocess.call(cmd)

        if len(files) > 1:
            text = ''
            for file in files:
                text += f"file '{file}'\n"
            with open('concat.txt', 'w') as f:
                f.write(text)
            
            name = f'{self.OUTPUT}/{name}_r.webm'
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', 'concat.txt',
                '-codec', 'copy',
                name
                ]
            subprocess.call(cmd)
            os.remove('concat.txt')
            os.remove(files[0])
            os.remove(files[1])
        if self.low:
            return name
        return name_std

    def download_audio(self, link, name) -> str:
        name = f'{self.OUTPUT}/{name}_a.webm'
        cmd = [
            'Program/ffmpeg', '-y',
            '-ss', str(self.audio_timing.pop(0)), 
            '-to', str(self.audio_timing.pop(0)),
            '-i', link,
            name
            ]
        subprocess.call(cmd)
        return name

    def merge(self, video: str, audio: str, name):
        cmd = [
            'ffmpeg',
            '-i', video,
            '-i', audio,
            '-codec', 'copy',
            f"{self.OUTPUT}/{name}.webm"
        ]
        subprocess.call(cmd)
        os.remove(video)
        os.remove(audio)


class Window(Tk):
    OUTPUT = 'output'
    def __init__(self):
        self.core = Core()

        Tk.__init__(self)
        self.title("Scissors")
        self.geometry('236x200')
        self.resizable(False, False)
        self.setUI()

        self.content = {}

    def setUI(self):
        self.frame_select = Frame(self)
        self.frame_select.grid(column=0, row=0, pady=5)

        self.entry = Entry(self.frame_select, width=35, justify=CENTER)
        self.entry.grid(column=0, row=0, ipadx=5, padx=5, pady=5)
        self.set_text('Ссылка на видео')

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
    
    def set_text(self, filename: str):
        self.entry.configure(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.insert(0, filename)
    

    def make(self):
        links = self.core.get_link(self.entry.get())
        
        float_start = time_to_sec(self.start_pos.get())
        float_end = time_to_sec(self.end_pos.get())
        self.core.time_parsing(start=float_start, end=float_end)
        
        name = self.video_name.get()
        video = self.core.download_video(links[0], name)
        audio = self.core.download_audio(links[1], name)
        self.core.merge(video, audio, name)


if __name__ == '__main__':
    root = Window()
    root.mainloop()