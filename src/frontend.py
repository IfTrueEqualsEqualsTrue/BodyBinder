""" Interface of bodyBinder"""
import tkinter.filedialog

import customtkinter as ctk
from backend import *
from toolz import partial
import os
from PIL import Image

colors = {"hred": "#780000", "red": "#c1121f", "white": "#fdf0d5", "hblue": "#003049",
          "blue": "#669bbc", "black": "#090d1f"}

root = None

font = 'Lucida Bright'

padx = 10
pady = 10

hits = ['A', 'Z', 'E', 'R', 'U', 'I', 'O', 'P']

names = get_catergories()

tagger = get_tagger()


class MainApp(ctk.CTk):
    """ Application principale de SquidReport"""

    def __init__(self, **kwargs):
        global root
        super().__init__(**kwargs)
        self.title('BodyBinder')
        self.geometry('720x480')
        self.iconbitmap('data/ressources/nobg_icon.ico')
        self.configure(fg_color=colors['white'])
        root = self  # Instance principale de l'application
        self.mainFrame = MainFrame(self, fg_color='transparent')
        center(self)
        fastgrid(self.mainFrame, 0, 0, 0, 0, "nsew")
        self.mainloop()


class MainFrame(ctk.CTkFrame):
    """ Frame principale de binding"""

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.indexLabel = ctk.CTkLabel(self, text=f'{tagger.index} / {tagger.total_tag}', font=(font, 30),
                                       text_color=colors['black'])
        self.nameLabel = ctk.CTkLabel(self, text=tagger.get_current_name(), font=(font, 30), text_color=colors['black'])
        self.chooseFrame = ChooseFrame(self, fg_color='transparent', border_width=3, border_color=colors['hblue'],
                                       corner_radius=10)
        self.openButton = ctk.CTkButton(self, text='', fg_color=colors['white'], border_color=colors['black'],
                                        width=55, height=50, border_width=3, hover_color=colors['blue'],
                                        command=self.open, image=ctk.CTkImage(Image.open('data/ressources/dir.png'),
                                                                              size=(40, 40)))
        self.selectButton = ctk.CTkButton(self, text='', fg_color=colors['white'], border_color=colors['black'],
                                          width=55, height=50, border_width=3, hover_color=colors['blue'],
                                          command=self.select,
                                          image=ctk.CTkImage(Image.open('data/ressources/select.png'), size=(40, 40)))

        self.display()

    def display(self):
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        fastgrid(self.indexLabel, 0, 0, padx, pady, 'ew')
        fastgrid(self.nameLabel, 1, 0, padx, pady, 'ew')
        fastgrid(self.selectButton, 0, 1, padx * 2, pady, '')
        fastgrid(self.openButton, 1, 1, padx * 2, pady, '')
        fastgrid(self.chooseFrame, 2, 0, padx * 2, pady * 2, 'nsew', columnspan=2)

    def update_index(self, progress_index, next_name, end=False):
        self.indexLabel.configure(text=f"{progress_index + 1} / {tagger.total_tag}")
        self.nameLabel.configure(text=next_name)
        if end:
            self.nameLabel.configure(text_color=colors['blue'])

    def update_selection(self):
        self.indexLabel.configure(text=f'{tagger.index} / {tagger.total_tag}')
        self.nameLabel.configure(text=tagger.get_current_name())

    def select(self):
        global tagger
        filename = tkinter.filedialog.askopenfilename(defaultextension='.json')
        change_parsed_file(filename)
        tagger = get_tagger()
        self.update_selection()
        self.chooseFrame.reset_colors()

    @staticmethod
    def open():
        os.startfile(os.path.join(os.getcwd(), "data/output"))


class ChooseFrame(ctk.CTkFrame):
    """ Frame de saisie des boutons et des binds"""

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.buttons = {}
        self.tagger = TagManager()
        self.display()

    def display(self):
        self.grid_rowconfigure((0, 1), weight=1)
        for index, (hit, name) in enumerate(zip(hits, names)):
            self.buttons[index] = [
                ctk.CTkButton(self, text=hit, font=(font, 40), fg_color=colors['white'], border_color=colors['black'],
                              text_color=colors['black'], width=55, height=50, border_width=3,
                              hover_color=colors['blue'],
                              command=partial(self.callback, index)),
                ctk.CTkLabel(self, text=name, font=(font, 25), text_color=colors['black'])
            ]
            self.grid_columnconfigure(index, weight=1)
            root.bind(f'<{hit.lower()}>', partial(self.callback, index))
            fastgrid(self.buttons[index][0], 0, index, padx, pady, '')
            fastgrid(self.buttons[index][1], 1, index, padx, (0, pady), '')

    def callback(self, index, event=None):
        global tagger
        if not tagger.complete:
            self.on_hit(index)
            progress_index, next_name = tagger.next(names[index])
            if next_name != 'end':
                self.master.update_index(progress_index, next_name)
                self.after(300, partial(self.reset_button, index))
            else:
                self.on_end()
                self.master.update_index(progress_index - 1, 'Terminé !', end=True)

    def on_hit(self, index):
        self.buttons[index][0].configure(border_color=colors['red'], text_color=colors['red'])
        self.buttons[index][1].configure(text_color=colors['red'])

    def reset_button(self, index):
        self.buttons[index][0].configure(border_color=colors['black'], text_color=colors['black'])
        self.buttons[index][1].configure(text_color=colors['black'])

    def on_end(self):
        for (button, label) in self.buttons.values():
            button.configure(border_color=colors['blue'], text_color=colors['blue'])
            label.configure(text_color=colors['blue'])

    def reset_colors(self):
        for index in self.buttons:
            self.reset_button(index)


def fastgrid(widget, x, y, xpad, ypad, sticky='', columnspan=1, rowspan=1):
    widget.grid(row=x, column=y, padx=xpad, pady=ypad, sticky=sticky, columnspan=columnspan, rowspan=rowspan)


def center(widget):
    widget.grid_rowconfigure(0, weight=1)
    widget.grid_columnconfigure(0, weight=1)
