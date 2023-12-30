# Training (GEO01)
# JCY oct 23
# PRO DB PY

import tkinter as tk
import random
from math import sqrt
import time
import database
import datetime
import tkinter as tk
import random
from math import sqrt
import time
import database
import datetime
from customtkinter import *


class GeoGame(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Game configuration and initial state
        self.l = 1000  # canvas length
        self.h = 500  # canvas height
        self.scale = 47.5  # scale for the canvas
        self.target_x = 10  # initial target x-coordinate
        self.target_y = 10  # initial target y-coordinate
        self.pseudo = "Gaston"  # default player name
        self.exercise = "GEO01"
        self.nbtrials = 0  # number of total trials
        self.nbok = 0  # number of successful trials
        self.start_date = datetime.datetime.now()  # start time
        self.hex_color = '#8bc9c2'  # background color

        self.configure(fg_color=self.hex_color)  # Set the frame color

        # Setup widgets
        self.setup_widgets()


    def setup_widgets(self):
        # Create and place canvas
        self.canvas = tk.Canvas(self, width=self.l, height=self.h, bg="#f9d893")
        self.canvas.pack(padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.canvas_click)

        # Create and place pseudo entry
        self.pseudo_entry = CTkEntry(self, placeholder_text="Pseudo")
        self.pseudo_entry.pack(pady=10)

        # Create and place result label
        self.lbl_result = CTkLabel(self, text="Essais réussis : 0/0")
        self.lbl_result.pack(pady=10)

        # Create and place target label
        self.lbl_target = CTkLabel(self, text="")
        self.lbl_target.pack(pady=10)

        # Create and place 'Next' button
        self.btn_next = CTkButton(self, text="Suivant", command=self.next_point)
        self.btn_next.pack(pady=10)

        # Create and place 'Finish' button
        self.btn_finish = CTkButton(self, text="Terminer", command=self.save_game)
        self.btn_finish.pack(pady=10)

        # Create and place duration label
        self.duration_label = CTkLabel(self, text="0:00")
        self.duration_label.pack(pady=10)

        # Start the first point
        self.next_point()

    def canvas_click(self, event):
        click_x = (event.x - self.l / 2) / self.scale
        click_y = -(event.y - self.h / 2) / self.scale

        dx = abs(click_x - self.target_x)
        dy = abs(click_y - self.target_y)
        d = sqrt(dx**2 + dy**2)

        self.mycircle = self.circle(self.target_x, self.target_y, 0.5, "red")

        self.nbtrials += 1
        if d > 0.5:
            self.configure(fg_color="red")
        else:
            self.configure(fg_color="green")
            self.nbok += 1

        # Update labels and other widgets as needed
        self.lbl_result.configure(text=f"{self.pseudo} Essais réussis : {self.nbok} / {self.nbtrials}")

    def circle(self, x, y, r, color):
        return self.canvas.create_oval(
            (x - r) * self.scale + self.l / 2, 
            -(y - r) * self.scale + self.h / 2, 
            (x + r) * self.scale + self.l / 2, 
            -(y + r) * self.scale + self.h / 2, 
            fill=color
        )

    def next_point(self, event=None):
        self.configure(fg_color=self.hex_color)
        self.canvas.delete('all')

        self.canvas.create_line(0, self.h/2, self.l, self.h/2, fill="black")
        self.canvas.create_line(self.l/2, 0, self.l/2, self.h, fill="black")
        for i in range(-10, 11, 5):
            self.canvas.create_line(self.l/2+i*self.scale, self.h/2-10, self.l/2+i*self.scale, self.h/2+10, fill="black")
            self.canvas.create_text(self.l/2+i*self.scale, self.h/2+20, text=i, fill="black", font=("Helvetica 15"))
        for i in range(-5, 6, 5):
            self.canvas.create_line(self.l/2-10, self.h/2-i*self.scale, self.l/2+10, self.h/2-i*self.scale, fill="black")
            self.canvas.create_text(self.l/2-20, self.h/2-i*self.scale, text=i, fill="black", font=("Helvetica 15"))

        self.target_x = round(random.uniform(-10, 10), 0)
        self.target_y = round(random.uniform(-5, 5), 0)

        self.lbl_target.configure(text=f"Cliquez sur le point ({round(self.target_x, 1)}, {round(self.target_y, 1)}). Echelle x -10 à +10, y-5 à +5")

    def save_game(self, event):
        end_time = datetime.datetime.now()
        duration = (end_time - self.start_date).total_seconds()
        pseudo = self.pseudo_entry.get()

        database.record_match_outcome(pseudo, self.exercise, duration, self.nbtrials, self.nbok)
        self.destroy()

    def display_timer(self):
        duration = datetime.datetime.now() - self.start_date
        duration_s = int(duration.total_seconds())
        self.duration_label.configure(text="{:02d}".format(int(duration_s / 60)) + ":" + "{:02d}".format(duration_s % 60))
        self.after(1000, self.display_timer)

    def open_window_geo_01(self, window):
        self.window_geo01 = tk.Toplevel(window)

        self.window_geo01.title("Exercice de géométrie")
        self.window_geo01.geometry("1100x900")

        rgb_color = (139, 201, 194)
        self.hex_color = '#%02x%02x%02x' % rgb_color
        self.window_geo01.configure(bg=self.hex_color)

        self.title_label = tk.Label(self.window_geo01, text=self.exercise, font=("Arial", 15))
        self.title_label.grid(row=0, column=1, padx=5, pady=5)

        self.duration_label = tk.Label(self.window_geo01, text="0:00", font=("Arial", 15))
        self.duration_label.grid(row=0, column=2, ipady=5, padx=10, pady=10)

        tk.Label(self.window_geo01, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
        self.pseudo_entry = tk.Entry(self.window_geo01, font=("Arial", 15))
        self.pseudo_entry.grid(row=1, column=1)

        self.lbl_result = tk.Label(self.window_geo01, text=f"Essais réussis : 0/0", font=("Arial", 15))
        self.lbl_result.grid(row=1, column=3, padx=5, pady=5, columnspan=4)

        self.lbl_target = tk.Label(self.window_geo01, text="", font=("Arial", 15))
        self.lbl_target.grid(row=2, column=0, padx=5, pady=5, columnspan=6)

        self.canvas = tk.Canvas(self.window_geo01, width=self.l, height=self.h, bg="#f9d893")
        self.canvas.grid(row=4, column=0, padx=5, pady=5, columnspan=6)
        self.btn_next = tk.Button(self.window_geo01, text="Suivant", font=("Arial", 15))
        self.btn_next.grid(row=5, column=0, padx=5, pady=5, columnspan=6)

        self.btn_finish = tk.Button(self.window_geo01, text="Terminer", font=("Arial", 15))
        self.btn_finish.grid(row=6, column=0, columnspan=6)

        self.btn_finish.bind("<Button-1>", lambda event: (self.save_game(event)))

        self.next_point(event=None)
        self.start_date = datetime.datetime.now()
        self.display_timer()

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.btn_next.bind("<Button-1>", self.next_point)
        self.btn_finish.bind("<Button-1>", self.save_game)

        self.window_geo01.mainloop()