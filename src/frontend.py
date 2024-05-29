""" Interface of bodyBinder"""

import customtkinter as ctk
from backend import *
from toolz import partial

colors = {"hred": "#780000", "red": "#c1121f", "white": "#fdf0d5", "hblue": "#003049",
          "blue": "#669bbc", "black": "#090d1f"}

root = None

font = 'Lucida Bright'

padx = 10
pady = 10

hits = ['A', 'Z', 'E', 'R', 'U', 'I', 'O', 'P']

names = get_catergories()


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
        self.maste = master
        self.indexLabel = ctk.CTkLabel(self, text='143 / 296', font=(font, 30), text_color=colors['black'])
        self.nameLabel = ctk.CTkLabel(self, text='orl21Gy', font=(font, 30), text_color=colors['black'])
        self.chooseFrame = ChooseFrame(self, fg_color='transparent', border_width=3, border_color=colors['hblue'],
                                       corner_radius=10)
        self.display()

    def display(self):
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        fastgrid(self.indexLabel, 0, 0, padx, pady, 'ew')
        fastgrid(self.nameLabel, 1, 0, padx, pady, 'ew')
        fastgrid(self.chooseFrame, 2, 0, padx*2, pady*2, 'nsew')


class ChooseFrame(ctk.CTkFrame):
    """ Frame de saisie des boutons et des binds"""

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.maste = master
        self.buttons = {}
        self.display()

    def display(self):
        self.grid_rowconfigure((0, 1), weight=1)
        for index, (hit, name) in enumerate(zip(hits, names)):
            self.buttons[index] = [
                ctk.CTkButton(self, text=hit, font=(font, 40), fg_color=colors['white'], border_color=colors['black'],
                              text_color=colors['black'], width=55, height=50, border_width=3, hover_color=colors['white'],
                              command=partial(self.callback, index)),
                ctk.CTkLabel(self, text=name, font=(font, 25), text_color=colors['black'])
            ]
            self.grid_columnconfigure(index, weight=1)
            root.bind(f'<{hit.lower()}>', partial(self.callback, index))
            fastgrid(self.buttons[index][0], 0, index, padx, pady, '')
            fastgrid(self.buttons[index][1], 1, index, padx, (0, pady), '')

    def callback(self, index, event=None):
        self.on_hit(index)
        self.after(300, partial(self.reset_button, index))

    def on_hit(self, index):
        self.buttons[index][0].configure(border_color=colors['red'], text_color=colors['red'])
        self.buttons[index][1].configure(text_color=colors['red'])

    def reset_button(self, index):
        self.buttons[index][0].configure(border_color=colors['black'], text_color=colors['black'])
        self.buttons[index][1].configure(text_color=colors['black'])







def fastgrid(widget, x, y, xpad, ypad, sticky, columnspan=1, rowspan=1):
    widget.grid(row=x, column=y, padx=xpad, pady=ypad, sticky=sticky, columnspan=columnspan, rowspan=rowspan)


def center(widget):
    widget.grid_rowconfigure(0, weight=1)
    widget.grid_columnconfigure(0, weight=1)
