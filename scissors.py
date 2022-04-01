from tkinter import CENTER, DISABLED, Entry, Label, Tk, Button, END
from tkinter import filedialog
from tkinter.font import NORMAL

import subprocess


class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("ffmpeg scissors")
        self.geometry('320x240')
        self.resizable(False, False)
        self.videopath = ''
        self.setUI()

    def setUI(self):
        self.entry = Entry(self, width=30, justify=CENTER)
        self.entry.pack()
        self.set_text('Выберите файл')
        
        self.select_button = Button(self, text='Выбрать', command=self.onOpen)
        self.select_button.pack()


        Label(self, text='Началальная позиция').pack()
        self.start_pos = Entry(self, width=10, justify=CENTER)
        self.start_pos.pack()

        Label(self, text="Конечная позиция").pack()
        self.end_pos = Entry(self, width=10, justify=CENTER)
        self.end_pos.pack()

        Label(self, text="Название видео").pack()
        self.video_name = Entry(self, width=20, justify=CENTER)
        self.video_name.pack()

        self.confirm_button = Button(self, text='Вырезать', command=self.make)
        self.confirm_button.pack()


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
            'ffmpeg',
            '-i', self.videopath,
            '-ss', self.start_pos.get(), 
            '-codec', 'copy',
            '-to', self.end_pos.get(),
            self.video_name.get()
            ]

        subprocess.call(cmd)
        
        


if __name__ == '__main__':
    root = Window()
    root.mainloop()