import tkinter as tk
from tkinter import ttk
import database
from tkinter import messagebox  # Pour la fenêtre pop-up
from database import remove_match_record
from database import fetch_game_statistics
from database import fetch_game_statistics
from database import retrieve_exercise_catalog


tree = None  # Global

entry_pseudo = None
entry_exercise = None
global derniers_filtres,donnees_chargees
derniers_filtres = {"pseudo": "", "exercise": ""}
donnees_chargees = False  # Pour suivre si les données ont été chargées



def create_result_window():
    global tree,entry_pseudo,entry_exercise,lbl_nblignes, lbl_tempTotal, lbl_nbOK, lbl_nbTotal, lbl_pourcentageTotal , entry_date_debut, entry_date_fin#pour definir global
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
    lbl_pseudo = tk.Label(window, text="Pseudo:")
    lbl_pseudo.grid(row=1,column=0 , sticky="e", padx=(0,60))
    entry_pseudo = tk.Entry(window)
    entry_pseudo.grid(row=1,column=1,sticky="w", padx=(0,60))

    # exercice
    lbl_exercice = tk.Label(window, text="Exercice:")
    lbl_exercice.grid(row=1,column=2, sticky="e", padx=(0,60))
    entry_exercise = tk.Entry(window)
    entry_exercise.grid(row=1,column=3,sticky="w", padx=(0,60))

    # date debut
    lbl_date_debut = tk.Label(window, text="Date debut:")
    lbl_date_debut.grid(row=1,column=4,sticky="e", padx=(0,60))
    entry_date_debut = tk.Entry(window)
    entry_date_debut.grid(row=1,column=5,sticky="w", padx=(0,60))

    # date fin
    lbl_date_fin = tk.Label(window, text="Date fin:")
    lbl_date_fin.grid(row=1,column=6,sticky="e", padx=(0,60))
    entry_date_fin = tk.Entry(window)
    entry_date_fin.grid(row=1,column=7,sticky="w", padx=(0,60))

    # button "voir result"

    btn_voir_resultat = tk.Button(window, text="Voir Resultat", command=lambda:voir_resultat())
    btn_voir_resultat.grid(row=2, padx=(0,5), )

    btn_total = tk.Button(window, text="Total", command=lambda: voir_total())
    btn_total.grid(row=21, padx=(0,0), )

    # bouton "nouvelle resultat"
    btn_ajouter = tk.Button(window, text="Ajouter", command=ajouter_resultat)
    btn_ajouter.grid(row=2, column=3, padx=(0, 5), )

    #les titre de tableau



    # pour cree Treeview
    tree = ttk.Treeview(window, height=20)
    tree["columns"] = ("Éléve", "Date Heure", "Temps", "Exercice", "NB OK", "Nb Trial", "% réussi")
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
    lbl_nblignes = tk.Label(window, text="")
    lbl_nblignes.grid(row=5, column=0, sticky='w')

    lbl_tempTotal = tk.Label(window, text="")
    lbl_tempTotal.grid(row=5, column=1, sticky='w')

    lbl_nbOK = tk.Label(window, text="")
    lbl_nbOK.grid(row=5, column=2, sticky='w')

    lbl_nbTotal = tk.Label(window, text="")
    lbl_nbTotal.grid(row=5, column=3, sticky='w')

    lbl_pourcentageTotal = tk.Label(window, text="")
    lbl_pourcentageTotal.grid(row=5, column=4,sticky="w")
    
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
    tree.set(row_id, column="% réussi", value=f"{percentage} %")
    tree.tag_configure(row_id, background=color)
    tree.item(row_id, tags=(row_id,))



def supprimer_resultat():
    try:
        selected_item = tree.selection()[0]  # Sélectionner l'élément
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à supprimer.")
        return

    pseudo = tree.item(selected_item, 'values')[0]
    dateHour = tree.item(selected_item, 'values')[1]
    duration = tree.item(selected_item, 'values')[2]
    exercise = tree.item(selected_item, 'values')[3]
    nbok = tree.item(selected_item, 'values')[4]
    nbtrials = tree.item(selected_item, 'values')[5]

    remove_match_record(pseudo, exercise, dateHour, duration, nbok, nbtrials)
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
    lbl_duration = tk.Label(update_window, text="Temps:")
    lbl_duration.pack()
    entry_duration = tk.Entry(update_window)
    entry_duration.pack()
    entry_duration.insert(0, current_values[2])  # par default value original

    # Ninput pour nbok
    lbl_nbok = tk.Label(update_window, text="Nb d’essais réussi:")
    lbl_nbok.pack()
    entry_nbok = tk.Entry(update_window)
    entry_nbok.pack()
    entry_nbok.insert(0, current_values[4])  # par default value original

    # input pour NbTrials
    lbl_nbtrials = tk.Label(update_window, text="Nb total:")
    lbl_nbtrials.pack()
    entry_nbtrials = tk.Entry(update_window)
    entry_nbtrials.pack()
    entry_nbtrials.insert(0, current_values[5])  # par default value original

    # boutton mise a jour
    btn_update = tk.Button(update_window, text="Update", command=lambda: update_result(selected_item, entry_duration.get(), entry_nbok.get(), entry_nbtrials.get()))
    btn_update.pack()


def update_result(selected_item, new_duration, new_nbok, new_nbtrials):

    global update_window
    current_values = tree.item(selected_item, 'values')
    pseudo = tree.item(selected_item, 'values')[0]  # pour pseudo
    dateHour = tree.item(selected_item, 'values')[1]  # pour date
    duration = tree.item(selected_item, 'values')[2]  # pour temps
    exercise = tree.item(selected_item, 'values')[3]  # pour exercise
    nbok = tree.item(selected_item, 'values')[4]  # pour nbok
    nbtrials = tree.item(selected_item, 'values')[5]  # pour nbtrials


    # mise a jour de bd
    database.revise_game_outcome(pseudo, exercise, dateHour, duration, nbok,nbtrials, new_duration, new_nbok, new_nbtrials)

    # mise a jour de tkinter
    updated_values = (pseudo, exercise, dateHour, new_duration, new_nbok, new_nbtrials, calculate_percentage(int(new_nbok), int(new_nbtrials)))
    tree.item(selected_item, values=updated_values)

    refresh_treeview()

    update_window.destroy()

def refresh_treeview():
    # Clear all existing data in the treeview
    tree.delete(*tree.get_children())

    # Fetch updated data from the database
    resultats, _ = database.fetch_game_statistics()  # Assuming the second value (total) is not used here
    for resultat in resultats:
        if isinstance(resultat, (list, tuple)):
            nbok = resultat[4]
            nbtrials = resultat[5]
            percentage = calculate_percentage(nbok, nbtrials)
            insert_data_into_treeview(tree, resultat, percentage)


def calculate_percentage(nbok, nbtrials):
    if isinstance(nbtrials, int) and nbtrials > 0:
        return round((nbok / nbtrials) * 100, 2)
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



def voir_resultat():
    global donnees_chargees, derniers_filtres

    # Retrieve values from input fields
    pseudo = entry_pseudo.get().strip()
    exercise = entry_exercise.get().strip()
    date_debut = entry_date_debut.get().strip()
    date_fin = entry_date_fin.get().strip()

    # Check if filters have changed
    if (pseudo == derniers_filtres["pseudo"] and
        exercise == derniers_filtres["exercise"] and
        date_debut == derniers_filtres.get("date_debut", "") and
        date_fin == derniers_filtres.get("date_fin", "") and
        donnees_chargees):
        messagebox.showinfo("Information", "Les données sont déjà à jour.")
        return

    # Reload data if any filter has changed
    if (pseudo != derniers_filtres["pseudo"] or
        exercise != derniers_filtres["exercise"] or
        date_debut != derniers_filtres.get("date_debut", "") or
        date_fin != derniers_filtres.get("date_fin", "")):
        donnees_chargees = False

    # Save the current filters
    derniers_filtres.update({"pseudo": pseudo, "exercise": exercise, "date_debut": date_debut, "date_fin": date_fin})

    # Fetch results from the database
    resultats, _ = database.fetch_game_statistics(pseudo=pseudo, exercise=exercise, start_date=date_debut, end_date=date_fin)

    # Check if results are available
    if not resultats:
        messagebox.showwarning("Erreur", "Aucun enregistrement trouvé pour les critères donnés.")
        donnees_chargees = False
        return

    # Clear existing data and display new results in Treeview
    tree.delete(*tree.get_children())
    for resultat in resultats:
        nbok = resultat[4]
        nbtrials = resultat[5]
        percentage = calculate_percentage(nbok, nbtrials)
        insert_data_into_treeview(tree, resultat, percentage)

    # Mark that data has been loaded
    donnees_chargees = True




def voir_total():
    total_lignes = 0
    total_duration = 0
    total_nbok = 0
    total_nbtrials = 0
    total_pourcentage = 0

    for child in tree.get_children():
        values = tree.item(child, 'values')
        total_lignes += 1
        total_duration += convert_time_to_seconds(values[2])  # converdir la valauer de duration minute en second
        total_nbok += int(values[4])  # ajouter NbOk
        total_nbtrials += int(values[5])  # ajouter NbTrials

    # calculer la moyenne de reussit
    if total_nbtrials > 0:
        total_pourcentage = (total_nbok / total_nbtrials) * 100
    else:
        total_pourcentage = 0

    lbl_nblignes.config(text=f"{total_lignes}")
    lbl_tempTotal.config(text=f"{total_duration}")
    lbl_nbOK.config(text=f"{total_nbok}")
    lbl_nbTotal.config(text=f" {total_nbtrials}")
    lbl_pourcentageTotal.config(text=f"{total_pourcentage:.2f}")


def ajouter_resultat():
    global ajout_window
    # pour creer nouvelle fenetre
    ajout_window = tk.Toplevel()
    ajout_window.title("Ajouter un résultat")

    ajout_window.geometry("400x250+700+350")

    # Force le focus sur cette fenêtre
    ajout_window.grab_set()

    # input pour "pseudo"
    lbl_pseudo = tk.Label(ajout_window, text="Pseudo:")
    lbl_pseudo.pack()
    entry_pseudo = tk.Entry(ajout_window)
    entry_pseudo.pack()

    # input pour 'Exercice'
    lbl_exercice = tk.Label(ajout_window, text="Exercice:")
    lbl_exercice.pack()
    entry_exercice = tk.Entry(ajout_window)
    entry_exercice.pack()

    # input pour 'Temps'
    lbl_temps = tk.Label(ajout_window, text="Temps:")
    lbl_temps.pack()
    entry_temps = tk.Entry(ajout_window)
    entry_temps.pack()

    # input pour 'NB OK'
    lbl_nbok = tk.Label(ajout_window, text="NB OK:")
    lbl_nbok.pack()
    entry_nbok = tk.Entry(ajout_window)
    entry_nbok.pack()

    # input pour 'Nb Trial'
    lbl_nbtrial = tk.Label(ajout_window, text="Nb Trial:")
    lbl_nbtrial.pack()
    entry_nbtrial = tk.Entry(ajout_window)
    entry_nbtrial.pack()

    # pour engregistrer nouvelle resultat
    btn_ajouter = tk.Button(ajout_window, text="Ajouter résultat", command=lambda: enregistrer_resultat(
        entry_pseudo.get(),
        entry_exercice.get(),
        entry_temps.get(),
        entry_nbok.get(),
        entry_nbtrial.get()
    ))
    btn_ajouter.pack()




def enregistrer_resultat(pseudo, exercice, temps, nbok, nbtrials):
    global ajout_window

    # Vérifier si l'exercice existe
    if not exercice_existe(exercice):
        existing_exercises = retrieve_exercise_catalog()
        messagebox.showwarning("Erreur", f"Cet exercice n'existe pas. Les exercices qui sont disponibles dans le bd: {', '.join(existing_exercises)}")
        return

    # Vérifier le format de temps
    if not format_temps_valide(temps):
        messagebox.showwarning("Erreur", "Format de temps invalide. Veuillez entrer le format HH:MM:SS.")
        return

    # envoyer à le bd
    database.save_game_result(pseudo, exercice, temps, nbok, nbtrials)
    refresh_treeview()

    messagebox.showinfo("Succès", "Données ajoutées avec succès !")

    ajout_window.destroy()


def exercice_existe(exercice):
    """
    Vérifie si un exercice donné existe dans la base de données.
    """
    # Utiliser la fonction get_game_results pour vérifier l'existence de l'exercice
    resultats = fetch_game_statistics(exercise=exercice)

    # Si aucun résultat n'est retourné, l'exercice n'existe pas
    return len(resultats) > 0



def format_temps_valide(temps_str):
    """
    Vérifie si une chaîne de temps donnée est dans le format correct (HH:MM:SS).

    """
    try:
        heures, minutes, secondes = map(int, temps_str.split(':'))
        assert 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59
        return True
    except (ValueError, AssertionError):
        return False

