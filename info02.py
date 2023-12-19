# Training (INFO02)
# JCY oct 23
# PRO DB PY

import tkinter as tk
import random
from math import pow
import time
import database
import datetime
from tkinter.messagebox import *

#important data (to save)
pseudo="Gaston" #provisory pseudo for user
exercise="INFO02"
nbtrials=0 #number of total trials
nbsuccess=0 #number of successfull trials

# Liaison entre le canvas et le code
unite = ["B", "kB", "MB", "GB", "TB"]
n1 = 0  # valeur à convertir
u1 = unite[0]
n2 = 0  # valeur à convertir
u2 = unite[0]
rapport = 0


def next(event):
    global n1, u1, u2, rapport
    window_info02.configure(bg=hex_color)

    n1 = round(random.random(), 3)
    dec = random.randint(0, 3)
    for i in range(dec):
        n1 *= 10
    n1 = round(n1, 3)
    p1 = random.randint(1, 4)
    u1 = unite[p1]
    p2 = p1
    while p1 == p2:
        p2 = random.randint(0, 4)
    u2 = unite[p2]
    rapport = pow(10, 3 * (p2 - p1))
    label_n1.configure(text=f" {n1} {u1} =")
    label_u2.configure(text=f" {u2} ")
    entry_n2.delete(0, 'end')


def save_game(event):
    global start_date, pseudo, exercise, nbtrials, nbsuccess

    # pour obtenir le temp dernier
    end_time = datetime.datetime.now()

    # pour calculer le temps de partie
    duration_seconds = (end_time - start_date).total_seconds()

    pseudo = pseudo_entry.get()

    # insert bd
    database.save_game_result(pseudo, exercise, duration_seconds, nbtrials, nbsuccess)

    window_info02.destroy()

def test(event):
    global n2, nbsuccess, nbtrials, pseudo_entry
    # Fonction pour tester si la valeur est juste
    n2 = float(entry_n2.get().replace(" ", ""))
    nbtrials+=1
    success = (abs(n1 / n2 / rapport - 1) < 0.01) #tolerance 1%
    if success:
        nbsuccess += 1
        window_info02.configure(bg="green")
    else:
        window_info02.configure(bg="red")

    pseudo = pseudo_entry.get()
    lbl_result.configure(text=f"{pseudo} Essais réussis : {nbsuccess} / {nbtrials}")
    window_info02.update()
    time.sleep(1) # delai 1s
    next(event=None)


def display_timer():
    duration = datetime.datetime.now() - start_date  # elapsed time since beginning, in time with decimals
    duration_s = int(duration.total_seconds())  # idem but in seconds (integer)
    # display min:sec (00:13)
    duration_label.configure(text="{:02d}".format(int(duration_s / 60)) + ":" + "{:02d}".format(duration_s % 60))
    window_info02.after(1000, display_timer)  # recommencer après 15 ms


def open_window_info_02(window):
    global window_info02, duration_label, lbl_result, entry_n2, label_u2, label_n1, hex_color, start_date,pseudo_entry
    window_info02 = tk.Toplevel(window)

    #window_info02 = tk.Tk()
    window_info02.title("Conversion d'unités")
    window_info02.geometry("1100x900")
    window_info02.grid_columnconfigure((0,1,2), minsize=150, weight=1)

    # color definition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
    window_info02.configure(bg=hex_color)

    title_label = tk.Label(window_info02, text=f"{exercise}", font=("Arial", 15))
    title_label.grid(row=0,column=0,columnspan=3, ipady=5, padx=20,pady=20)
    duration_label = tk.Label(window_info02, text="0:00", font=("Arial", 15))
    duration_label.grid(row=0,column=2, ipady=5, padx=10,pady=10)

    tk.Label(window_info02, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
    pseudo_entry = tk.Entry(window_info02, font=("Arial", 15))
    # pseudo_entry.pack(ipadx=2, ipady=10, padx=5,pady=5)
    pseudo_entry.grid(row=1, column=1)




    lbl_result = tk.Label(window_info02, text=f"{pseudo}  Essais réussis : 0/0", font=("Arial", 15))
    lbl_result.grid( row=1, column=2,columnspan=3, ipady=5, padx=20,pady=20)

    label_n1 = tk.Label(window_info02, text="n1:",font=("Arial", 15))
    label_n1.grid(row=2,column=0,ipady=5, padx=20,pady=20,sticky='E')

    entry_n2 = tk.Entry(window_info02,font=("Arial", 15))
    entry_n2.grid(row=2,column=1,ipady=5,padx=5, pady=20,sticky='E')

    label_u2 =tk.Label(window_info02, text="u2:",font=("Arial", 15))
    label_u2.grid(row=2,column=2,ipady=5,padx=5,pady=20,sticky='W')

    btn_next =tk.Button(window_info02, text="Suivant", font=("Arial", 15))
    btn_next.grid(row=3,column=0,columnspan=3,ipady=5, padx=5,pady=5)

    btn_finish = tk.Button(window_info02, text="Terminer", font=("Arial", 15))
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
