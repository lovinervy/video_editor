from tkinter import BOTTOM, CENTER, DISABLED, Entry, Frame, Label, Tk, Button, END
from tkinter import filedialog
from tkinter.font import NORMAL

import subprocess
from os import remove


class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.all_entry = {}
        self.cur_entry = 0
        self.title("ffmpeg concat")
        self.geometry('320x540')
        self.resizable(width=False, height=True)
        self.setUI()

    def setUI(self):
        self.add_button = None
        self.add_video()


        self.confirm_button = Button(self, text='Склеить', command=self.make)
        self.confirm_button.pack(side=BOTTOM, pady=5)

        self.video_name = Entry(self, width=20, justify=CENTER)
        self.video_name.pack(side=BOTTOM)

        Label(self, text="Название видео").pack(side=BOTTOM)

    def onOpen(self, entry):
        ftypes = [
            ('webm файлы', '*.webm'),
            ('mp4 файлы', '*.mp4'),
            ('Все файлы', '*'),
            ]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
 
        if fl != '':
            self.set_text(entry, fl)
    
    def add_video(self):
        if self.add_button: self.add_button.pack_forget()
        
        cur = self.cur_entry
        self.all_entry[cur] = {}
        
        entry = Entry(self, width=30, justify=CENTER)
        self.all_entry[cur]['entry'] = entry
        entry.pack()
        self.set_text(entry, "Выберите файл")

        frame = Frame(self)
        self.all_entry[cur]['frame'] = frame
        frame.pack(pady=5)

        select_button = Button(frame, text='Выбрать', command=lambda:self.onOpen(entry))
        self.all_entry[cur]['select'] = select_button
        select_button.grid(column=0, row=0, padx=5)

        btn = Button(frame, text='Удалить', command= lambda: self.delete_video(cur, btn))
        btn.grid(column=1, row=0)
        self.add_button = Button(self, text='Добавить', command=self.add_video)
        self.add_button.pack()
        self.cur_entry += 1

    def delete_video(self, cur, btn):
        self.all_entry[cur]['entry'].pack_forget()
        self.all_entry[cur]['select'].pack_forget()
        self.all_entry[cur]['frame'].pack_forget()
        self.all_entry.pop(cur)
        btn.pack_forget()

    def set_text(self, entry, filename: str):
        entry.configure(state=NORMAL)
        entry.delete(0, END)
        entry.insert(0, filename)
        entry.configure(state=DISABLED)
    
    def result(self):
        text = ''
        for i in self.all_entry.keys():
            res = self.all_entry[i]['entry']
            text += f"file '{res.get()}'\n"
        with open('files.txt', 'w') as f:
            f.write(text)

    def make(self):
        self.result()
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'files.txt',
            '-codec', 'copy',
            self.video_name.get()
            ]

        subprocess.call(cmd)
        remove('files.txt')
        
        


if __name__ == '__main__':
    root = Window()
    root.mainloop()
