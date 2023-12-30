# Training (INFO02)
# JCY oct 23
# PRO DB PY

import tkinter as tk
from customtkinter import *
import random
from math import pow
import time
import database
import datetime
from tkinter.messagebox import showerror

class Info02Game(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Important data (to save)
        self.pseudo = "Gaston"  # Provisional pseudo for the user
        self.exercise = "INFO02"
        self.nbtrials = 0  # Number of total trials
        self.nbsuccess = 0  # Number of successful trials

        # Liaison entre le canvas et le code
        self.unite = ["B", "kB", "MB", "GB", "TB"]
        self.n1 = 0  # Valeur à convertir
        self.u1 = self.unite[0]
        self.n2 = 0  # Valeur à convertir
        self.u2 = self.unite[0]
        self.rapport = 0
        self.start_date = datetime.datetime.now()

        self.configure(fg_color='white')  # Set the foreground color
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.create_widgets()
        self.next()


    def create_widgets(self):
        # Title label
        self.title_label = CTkLabel(self, text=f"{self.exercise}", font=("Arial", 15))
        self.title_label.grid(row=0, column=0, columnspan=3, ipady=5, padx=20, pady=20)

        # Timer label
        self.duration_label = CTkLabel(self, text="0:00", font=("Arial", 15))
        self.duration_label.grid(row=0, column=2, ipady=5, padx=10, pady=10)

        # Pseudo label and entry
        CTkLabel(self, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
        self.pseudo_entry = CTkEntry(self, font=("Arial", 15))
        self.pseudo_entry.grid(row=1, column=1)

        # Result label
        self.lbl_result = CTkLabel(self, text=f"{self.pseudo} Essais réussis : 0/0", font=("Arial", 15))
        self.lbl_result.grid(row=1, column=2, columnspan=3, ipady=5, padx=20, pady=20)

        # Conversion question labels and entry
        self.label_n1 = CTkLabel(self, text="n1:", font=("Arial", 15))
        self.label_n1.grid(row=2, column=0, ipady=5, padx=20, pady=20, sticky='E')

        self.entry_n2 = CTkEntry(self, font=("Arial", 15))
        self.entry_n2.grid(row=2, column=1, ipady=5, padx=5, pady=20, sticky='E')

        self.label_u2 = CTkLabel(self, text="u2:", font=("Arial", 15))
        self.label_u2.grid(row=2, column=2, ipady=5, padx=5, pady=20, sticky='W')

        # 'Next' button
        self.btn_next = CTkButton(self, text="Suivant", font=("Arial", 15), command=self.next)
        self.btn_next.grid(row=3, column=0, columnspan=3, ipady=5, padx=5, pady=5)

        # 'Finish' button
        self.btn_finish = CTkButton(self, text="Terminer", font=("Arial", 15), command=self.save_game)
        self.btn_finish.grid(row=4, column=0, columnspan=3, ipady=5, padx=5, pady=5)

        # Bind the Return key to the test method (when the user presses Enter after typing their answer)
        self.entry_n2.bind("<Return>", self.test)
        self.display_timer()


    def next(self):
        # Logic to set up the next question
        self.n1 = round(random.uniform(0.001, 1000), 3)
        u1_index = random.randint(1, 4)
        self.u1 = self.unite[u1_index]
        u2_index = random.randint(0, 4)
        while u1_index == u2_index:
            u2_index = random.randint(0, 4)
        self.u2 = self.unite[u2_index]
        self.rapport = pow(10, 3 * (u2_index - u1_index))
        self.label_n1.configure(text=f"{self.n1} {self.u1} = ")
        self.label_u2.configure(text=f"{self.u2}")
        self.entry_n2.delete(0, tk.END)
        self.configure(fg_color='white')  # Reset background color


    def save_game(self):
        # Calculate the duration of the game
        end_time = datetime.datetime.now()
        duration_seconds = (end_time - self.start_date).total_seconds()

        # Get the pseudo from the entry widget
        pseudo = self.pseudo_entry.get()

        # Save the game result to the database
        database.save_game_result(pseudo, self.exercise, duration_seconds, self.nbtrials, self.nbsuccess)

        # Destroy the game frame or hide it, depending on your application's needs
        self.destroy()

    def test(self, event=None):
        try:
            self.n2 = float(self.entry_n2.get().replace(",", "."))
            self.nbtrials += 1
            success = abs(self.n1 / self.n2 / self.rapport - 1) < 0.01  # 1% tolerance
            if success:
                self.nbsuccess += 1
                self.configure(fg_color='green')  # Success color
            else:
                self.configure(fg_color='red')  # Error color
            self.lbl_result.configure(text=f"{self.pseudo} Essais réussis : {self.nbsuccess} / {self.nbtrials}")
            self.after(1000, self.next)  # Wait 1 second then go to next question
        except ValueError:
            showerror("Erreur", "Entrée non valide. Veuillez entrer un nombre.")
            self.entry_n2.delete(0, tk.END)


    def display_timer(self):
        # Calculate elapsed time
        duration = datetime.datetime.now() - self.start_date
        duration_s = int(duration.total_seconds())
        
        # Update the duration label text to display the time in min:sec format
        self.duration_label.configure(text="{:02d}:{:02d}".format(duration_s // 60, duration_s % 60))
        
        # Schedule the timer to update after one second again
        self.after(1000, self.display_timer)


    def open_window_info_02(self, window):
            global window_info02, duration_label, lbl_result, entry_n2, label_u2, label_n1, hex_color, start_date, pseudo_entry
            window_info02 = tk.Toplevel(window)

            # window_info02 = tk.Tk()
            window_info02.title("Conversion d'unités")
            window_info02.geometry("1100x900")
            window_info02.grid_columnconfigure((0, 1, 2), minsize=150, weight=1)

            # color definition
            rgb_color = (139, 201, 194)
            hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
            window_info02.configure(bg=hex_color)

            title_label = CTkLabel(window_info02, text=f"{exercise}", font=("Arial", 15))
            title_label.grid(row=0, column=0, columnspan=3, ipady=5, padx=20, pady=20)
            duration_label = CTkLabel(window_info02, text="0:00", font=("Arial", 15))
            duration_label.grid(row=0, column=2, ipady=5, padx=10, pady=10)

            CTkLabel(window_info02, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
            pseudo_entry = CTkEntry(window_info02, font=("Arial", 15))
            # pseudo_entry.pack(ipadx=2, ipady=10, padx=5,pady=5)
            pseudo_entry.grid(row=1, column=1)

            lbl_result = CTkLabel(window_info02, text=f"{pseudo}  Essais réussis : 0/0", font=("Arial", 15))
            lbl_result.grid(row=1, column=2, columnspan=3, ipady=5, padx=20, pady=20)

            label_n1 = CTkLabel(window_info02, text="n1:", font=("Arial", 15))
            label_n1.grid(row=2, column=0, ipady=5, padx=20, pady=20, sticky='E')

            entry_n2 = CTkEntry(window_info02, font=("Arial", 15))
            entry_n2.grid(row=2, column=1, ipady=5, padx=5, pady=20, sticky='E')

            label_u2 = CTkLabel(window_info02, text="u2:", font=("Arial", 15))
            label_u2.grid(row=2, column=2, ipady=5, padx=5, pady=20, sticky='W')

            btn_next = CTkButton(window_info02, text="Suivant", font=("Arial", 15))
            btn_next.grid(row=3, column=0, columnspan=3, ipady=5, padx=5, pady=5)

            btn_finish = CTkButton(window_info02, text="Terminer", font=("Arial", 15))
            btn_finish.grid(row=6, column=0, columnspan=6)

            # button-1 clic a gauche souris
            # bind pour relier un function sur un bouton
            btn_finish.bind("<Button-1>", lambda event: (save_game(event)))

            start_date = datetime.datetime.now()
            display_timer()
            # first call of next_point
            next(event=None)


            # binding actions (entry & buttons)
            entry_n2.bind("<Return>", test)
            btn_next.bind("<Button-1>", next)
            btn_finish.bind("<Button-1>", save_game)

            # Main loop
            window_info02.mainloop()