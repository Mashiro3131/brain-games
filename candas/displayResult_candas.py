import tkinter as tk
from tkinter import ttk
import database
from tkinter import messagebox  # Pour la fenêtre pop-up
from database import delete_game_result
from database import fetch_game_statistics
from database import retrieve_exercise_catalog


tree = None  # Global

pseudo_entry = None
exercise_entry = None
global last_filters,loaded_data
last_filters = {"pseudo": "", "exercise": ""}
loaded_data = False  # Pour suivre si les données ont été chargées



def display_results():
    global tree,pseudo_entry,exercise_entry,nblines_label, duration_label, nbok_label, nbtotal_label, percentage_label , start_date_entry, end_date_entry#pour definir global
    #cree nouvelle fenetre avec titre
    window = tk.Tk()
    window.title("TRAINING : AFFICHAGE")
    window.configure(bg='#8aded5')

    #pour gere la taille de fenetre
    window.geometry("1300x700+300+150")


    #titre
    lbl_title = tk.Label(window, text="TRAINING : AFFICHAGE", font=("Arial",16))
    lbl_title.grid(row=0,column=0, columnspan=8, pady=(0,20))

    #pour les inputs
    #Pseudo
    pseudo_label = tk.Label(window, text="Pseudo:")
    pseudo_label.grid(row=1,column=0 , sticky="e", padx=(0,60))
    pseudo_entry = tk.Entry(window)
    pseudo_entry.grid(row=1,column=1,sticky="w", padx=(0,60))

    # exercise
    exercise_label = tk.Label(window, text="Exercice:")
    exercise_label.grid(row=1,column=2, sticky="e", padx=(0,60))
    exercise_entry = tk.Entry(window)
    exercise_entry.grid(row=1,column=3,sticky="w", padx=(0,60))

    # date debut
    lbl_date_debut = tk.Label(window, text="Date debut:")
    lbl_date_debut.grid(row=1,column=4,sticky="e", padx=(0,60))
    start_date_entry = tk.Entry(window)
    start_date_entry.grid(row=1,column=5,sticky="w", padx=(0,60))

    # date fin
    lbl_date_fin = tk.Label(window, text="Date fin:")
    lbl_date_fin.grid(row=1,column=6,sticky="e", padx=(0,60))
    end_date_entry = tk.Entry(window)
    end_date_entry.grid(row=1,column=7,sticky="w", padx=(0,60))

    # button "voir result"

    btn_voir_resultat = tk.Button(window, text="Voir Resultat", command=lambda:view_results())
    btn_voir_resultat.grid(row=2, padx=(0,5))

    btn_total = tk.Button(window, text="Total", command=lambda: view_total())
    btn_total.grid(row=21, padx=(0,0))

    # bouton "nouvelle result"
    add_result = tk.Button(window, text="Ajouter", command=add_results)
    add_result.grid(row=2, column=3, padx=(0, 5))

    #les titre de tableau



    # pour cree Treeview
    tree = ttk.Treeview(window, height=20)
    tree["columns"] = ("Éléve", "Date Heure", "Temps", "Exercice", "NB OK", "Nb Trial", ""% Success")
    tree.column("#0", width=0, stretch=tk.NO)
    # tree.column

    # definir les tittre et leur taille et styles
    for col in tree["columns"]:
        tree.column(col, width=150,anchor="center")
        tree.heading(col, text=col, anchor="center")

    tree.grid(row=3, column=0, columnspan=8)


    # partie total

    # total
    tk.Label(window, text="NbLignes").grid(row=4, column=0, sticky='w')
    tk.Label(window, text="Temps total").grid(row=4, column=1, sticky='w')
    tk.Label(window, text="Nb OK").grid(row=4, column=2, sticky='w')
    tk.Label(window, text="Nb Total").grid(row=4, column=3, sticky='w')
    tk.Label(window, text="% Total").grid(row=4, column = 4, sticky="w")

    # total
    nblines_label = tk.Label(window, text="")
    nblines_label.grid(row=5, column=0, sticky='w')

    duration_label = tk.Label(window, text="")
    duration_label.grid(row=5, column=1, sticky='w')

    nbok_label = tk.Label(window, text="")
    nbok_label.grid(row=5, column=2, sticky='w')

    nbtotal_label = tk.Label(window, text="")
    nbtotal_label.grid(row=5, column=3, sticky='w')

    percentage_label = tk.Label(window, text="")
    percentage_label.grid(row=5, column=4,sticky="w")

    # Bouton Supprimer
    btn_supprimer = tk.Button(window, text="Supprimer", command=supprimer_resultat)
    btn_supprimer.grid(row=2, column=1, padx=(0, 5))

    # Bouton Modifier
    btn_modifier = tk.Button(window, text="Modifier", command=modifier_resultat)
    btn_modifier.grid(row=2, column=2, padx=(0, 5))



    window.mainloop()



def insert_data_into_treeview(tree, values, percentage):
    color = colorize_percentage(percentage)
    row_id = tree.insert('', 'end', values=(*values, ''))
    tree.set(row_id, column=""% Success", value=f"{percentage} %")
    tree.tag_configure(row_id, background=color)
    tree.item(row_id, tags=(row_id,))



def supprimer_resultat():
    try:
        selected_item = tree.selection()[0]  # Sélectionner l'élément
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à supprimer.")
        return

    pseudo = tree.item(selected_item, 'values')[0]
    date_hour = tree.item(selected_item, 'values')[1]
    duration = tree.item(selected_item, 'values')[2]
    exercise = tree.item(selected_item, 'values')[3]
    nbok = tree.item(selected_item, 'values')[4]
    nbtrials = tree.item(selected_item, 'values')[5]

    delete_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials)
    tree.delete(selected_item)



def modifier_resultat():
    global update_window

    try:
        selected_item = tree.selection()[0]
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à modifier.")
        return

    current_values = tree.item(selected_item, 'values')

    # pour ouvrir nouvelle fenetre
    update_window = tk.Toplevel()
    update_window.title("Modifier un résultat")

    update_window.geometry("400x200+700+350")
    # Force le focus sur cette fenêtre
    update_window.grab_set()

    # input pour Duration
    duration_label = tk.Label(update_window, text="Temps:")
    duration_label.pack()
    duration_entry = tk.Entry(update_window)
    duration_entry.pack()
    duration_entry.insert(0, current_values[2])  # par default value original

    # Ninput pour nbok
    nbok_label = tk.Label(update_window, text="NB d’essais réussi:")
    nbok_label.pack()
    nbok_entry = tk.Entry(update_window)
    nbok_entry.pack()
    nbok_entry.insert(0, current_values[4])  # par default value original

    # input pour NbTrials
    nbtrials_label = tk.Label(update_window, text="Nb total:")
    nbtrials_label.pack()
    nbtrials_entry = tk.Entry(update_window)
    nbtrials_entry.pack()
    nbtrials_entry.insert(0, current_values[5])  # par default value original

    # boutton mise a jour
    update_button = tk.Button(update_window, text="Update", command=lambda: update_result(selected_item, duration_entry.get(), nbok_entry.get(), nbtrials_entry.get()))
    update_button.pack()


def update_result(selected_item, new_duration, new_nbok, new_nbtrials):

    global update_window
    current_values = tree.item(selected_item, 'values')
    pseudo = tree.item(selected_item, 'values')[0]  # pour pseudo
    date_hour = tree.item(selected_item, 'values')[1]  # pour date
    duration = tree.item(selected_item, 'values')[2]  # pour temps
    exercise = tree.item(selected_item, 'values')[3]  # pour exercise
    nbok = tree.item(selected_item, 'values')[4]  # pour nbok
    nbtrials = tree.item(selected_item, 'values')[5]  # pour nbtrials


    # mise a jour de bd
    database.update_game_result(pseudo, exercise, date_hour, duration, nbok,nbtrials, new_duration, new_nbok, new_nbtrials)

    # mise a jour de tkinter
    updated_values = (pseudo, exercise, date_hour, new_duration, new_nbok, new_nbtrials, calculate_percentage(int(new_nbok), int(new_nbtrials)))
    tree.item(selected_item, values=updated_values)

    refresh_treeview()

    update_window.destroy()

def refresh_treeview():
    # supprimer tous les donnees
    tree.delete(*tree.get_children())

    # mise a jour tous les donnees depuis bd
    results = database.fetch_game_statistics()
    for result in results:
        nbok = result[4]
        nbtrials = result[5]
        percentage = calculate_percentage(nbok, nbtrials)
        insert_data_into_treeview(tree, result, percentage)


def calculate_percentage(nbok, nb_trial):
    if nb_trial > 0:
        return round((nbok / nb_trial) * 100, 2)
    else:
        return 0

def convert_time_to_seconds(time_str):
    """ Convertir la chaine de temps donnée (HH:MM:SS) en secondes."""
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds



def colorize_percentage(percentage):
    #pour definir les coleurs avec %
    if percentage < 25:
        return 'red'
    elif percentage < 50:
        return 'orange'
    elif percentage < 75:
        return 'yellow'
    else:
        return 'green'


# def view_results():
#     global loaded_data, last_filters
#     pseudo = pseudo_entry.get().strip()
#     exercise = exercise_entry.get().strip()
#
#     # Vérifier si les filtres sont identiques aux derniers utilisés et si les données ont déjà été chargées
#     if pseudo == last_filters["pseudo"] and exercise == last_filters["exercise"] and loaded_data:
#         messagebox.showinfo("Information", "Les données sont déjà à jour.")
#         return
#
#     # Réinitialiser les données si les filtres ont changé
#     if pseudo != last_filters["pseudo"] or exercise != last_filters["exercise"]:
#         loaded_data = False
#
#     # Mémoriser les filtres actuels
#     last_filters["pseudo"] = pseudo
#     last_filters["exercise"] = exercise
#
#     # Récupérer les résultats de la base de données
#     results = database.fetch_game_statistics(pseudo=pseudo, exercise=exercise)
#
#     # Afficher un message si aucun résultat n'est trouvé
#     if not results:
#         messagebox.showinfo("Information", "Aucun enregistrement trouvé pour les critères donnés.")
#         loaded_data = False
#         return
#
#     # Nettoyer les données existantes dans le Treeview et afficher les nouveaux résultats
#     tree.delete(*tree.get_children())
#     for result in results:
#         # Traiter chaque résultat et l'ajouter au Treeview
#         nbok = result[4]
#         nbtrials = result[5]
#         percentage = calculate_percentage(nbok, nbtrials)
#         insert_data_into_treeview(tree, result, percentage)
#
#     # Marquer que les données sont chargées
#     loaded_data = True

def view_results():
    global loaded_data, last_filters

    # Récupérer les valeur d'inputs de champ de saisie
    pseudo = pseudo_entry.get().strip()
    exercise = exercise_entry.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()


    # Vérifier si les filtres ont changé, y compris les dates
    if (pseudo == last_filters["pseudo"] and
        exercise == last_filters["exercise"] and
        start_date == last_filters.get("start_date", "") and
        end_date == last_filters.get("end_date", "") and
        loaded_data):
        messagebox.showinfo("Information", "Les données sont déjà à jour.")
        return

    # Recharger les données si un des filtres a changé
    if (pseudo != last_filters["pseudo"] or
        exercise != last_filters["exercise"] or
        start_date != last_filters.get("start_date", "") or
        end_date != last_filters.get("end_date", "")):
        loaded_data = False

    # Enregistrer les nouveaux filtres
    last_filters.update({"pseudo": pseudo, "exercise": exercise, "start_date": start_date, "end_date": end_date})

    # Obtenir les résultats de la bd
    results = database.fetch_game_statistics(pseudo=pseudo, exercise=exercise, start_date=start_date, end_date=end_date)

    # Vérifier s'il y a des résultats
    if not results:
        messagebox.showwarning("Erreur", "Aucun enregistrement trouvé pour les critères donnés.")
        loaded_data = False
        return

    # Nettoyer les données existantes dans Treeview et afficher les nouveaux résultats
    tree.delete(*tree.get_children())
    for result in results:
        nbok = result[4]
        nbtrials = result[5]
        percentage = calculate_percentage(nbok, nbtrials)
        insert_data_into_treeview(tree, result, percentage)

    # Marquer que les données sont deja été chargees
    loaded_data = True



def view_total():
    lines_total = 0
    duration_total = 0
    nbok_total = 0
    nbtrials_total = 0
    percentage_total = 0

    for child in tree.get_children():
        values = tree.item(child, 'values')
        lines_total += 1
        duration_total += convert_time_to_seconds(values[2])  # converdir la valauer de duration minute en second
        nbok_total += int(values[4])  # ajouter NbOk
        nbtrials_total += int(values[5])  # ajouter NbTrials

    # calculer la moyenne de reussit
    if nbtrials_total > 0:
        percentage_total = (nbok_total / nbtrials_total) * 100
    else:
        percentage_total = 0

    nblines_label.config(text=f"{lines_total}")
    duration_label.config(text=f"{duration_total}")
    nbok_label.config(text=f"{nbok_total}")
    nbtotal_label.config(text=f" {nbtrials_total}")
    percentage_label.config(text=f"{percentage_total:.2f}")


def add_results():
    global add_window

    add_window = tk.Toplevel()
    add_window.title("Ajouter un résultat")
    add_window.geometry("400x250+700+350")
    add_window.grab_set()

    # input pour "pseudo"
    pseudo_label = tk.Label(add_window, text="Pseudo:")
    pseudo_label.pack()
    pseudo_entry = tk.Entry(add_window)
    pseudo_entry.pack()

    # input pour 'Exercice'
    exercise_label = tk.Label(add_window, text="Exercice:")
    exercise_label.pack()
    exercise_entry = tk.Entry(add_window)
    exercise_entry.pack()

    # input pour 'Temps'
    time_label = tk.Label(add_window, text="Temps:")
    time_label.pack()
    time_entry = tk.Entry(add_window)
    time_entry.pack()

    # input pour 'NB OK'
    nbok_label = tk.Label(add_window, text="NB OK:")
    nbok_label.pack()
    nbok_entry = tk.Entry(add_window)
    nbok_entry.pack()

    # input pour 'Nb Trial'
    nbtrials_label = tk.Label(add_window, text="NB Trials:")
    nbtrials_label.pack()
    nbtrial_entry = tk.Entry(add_window)
    nbtrial_entry.pack()

    # pour engregistrer nouvelle result
    add_result = tk.Button(add_window, text="Ajouter résultat", command=lambda: save_results(
        pseudo_entry.get(),
        exercise_entry.get(),
        time_entry.get(),
        nbok_entry.get(),
        nbtrial_entry.get()
    ))
    add_result.pack()




def save_results(pseudo, exercise, temps, nbok, nb_trial):
    global add_window

    # Vérifier si l'exercise existe
    if not check_exercise_exists(exercise):
        existing_exercises = retrieve_exercise_catalog()
        messagebox.showwarning("Erreur", f"Cet exercise n'existe pas. Les exercices qui sont disponibles dans le bd: {', '.join(existing_exercises)}")
        return

    # Vérifier le format de temps
    if not time_format(temps):
        messagebox.showwarning("Erreur", "Format de temps invalide. Veuillez entrer le format HH:MM:SS.")
        return

    # envoyer à le bd
    database.save_game_result(pseudo, exercise, temps, nbok, nb_trial)
    refresh_treeview()

    messagebox.showinfo("Succès", "Données ajoutées avec succès !")

    add_window.destroy()


def check_exercise_exists(exercise):
    """
    Vérifie si un exercise donné existe dans la base de données.
    """
    # Utiliser la fonction fetch_game_statistics pour vérifier l'existence de l'exercise
    results = fetch_game_statistics(exercise=exercise)

    # Si aucun résultat n'est retourné, l'exercise n'existe pas
    return len(results) > 0



def time_format(temps_str):
    """
    Vérifie si une chaîne de temps donnée est dans le format correct (HH:MM:SS).

    """
    try:
        heures, minutes, secondes = map(int, temps_str.split(':'))
        assert 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59
        return True
    except (ValueError, AssertionError):
        return False

