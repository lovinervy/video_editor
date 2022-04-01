from tkinter import Tk, Frame
from tkinter import Entry, Label, Button, Checkbutton, IntVar
from tkinter import CENTER, DISABLED, END
from tkinter import filedialog
from tkinter.font import NORMAL

import subprocess
import os


class Window(Tk):
    OUTPUT = 'output'
    def __init__(self):
        if not os.path.isdir(self.OUTPUT):
            os.makedirs(self.OUTPUT)

        Tk.__init__(self)
        self.title("Scissors")
        self.geometry('236x200')
        self.resizable(False, False)
        self.videopath = ''
        self.setUI()

    def setUI(self):
        self.frame_select = Frame(self)
        self.frame_select.grid(column=0, row=0, pady=5)

        self.entry = Entry(self.frame_select, width=35, justify=CENTER)
        self.entry.grid(column=0, row=0, ipadx=5, padx=5, pady=5)
        self.set_text('Выберите файл')
        
        self.select_button = Button(self.frame_select, text='Выбрать', command=self.onOpen)
        self.select_button.grid(column=0, row=1, ipadx=45)

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

        self.low_decoding = IntVar(self, False)
        self.check = Checkbutton(self, text='low decoding', variable=self.low_decoding)
        self.check.grid(column=0, row=4)

        self.confirm_button = Button(self, text='Вырезать', command=self.make)
        self.confirm_button.grid(column=0, row=5, pady=5)


    def onOpen(self):
        ftypes = [
            ('webm файлы', '*.webm'),
            ('mp4 файлы', '*.mp4'),
            ('Все файлы', '*'),
            ]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
 
        if fl != '':
            self.videopath = fl
            fl = fl.split('/')[-1]
            self.set_text(fl)
    
    def set_text(self, filename: str):
        self.entry.configure(state=NORMAL)
        self.entry.delete(0, END)
        self.entry.insert(0, filename)
        self.entry.configure(state=DISABLED)
    

    def make(self):
        cmd = [
            'Program/ffmpeg', '-y',
            '-i', self.videopath,
            '-ss', self.start_pos.get(), 
            '-to', self.end_pos.get(),
        ]
        if self.low_decoding.get():
            cmd += [
                '-c:v', 'libvpx-vp9',
                '-b:v', '0',
            ]
        else:
            cmd += ['-codec', 'copy']

        cmd += [f"{self.OUTPUT}/{self.video_name.get()}"]

        subprocess.call(cmd)
        
        


if __name__ == '__main__':
    root = Window()
    root.mainloop()