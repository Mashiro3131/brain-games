"""
SQL de la base de données pour les références
"""

"""
4. Affichage des résultats 
On souhaite maintenant un nouvel écran, accessible depuis le menu principal, qui affiche les résultats sous une forme proche de celle-ci. 
Si possible on aimerait pouvoir filtrer au moins par élève et exercice. En bonus, on aimerait aussi : 

    - filtrer en donnant une date de début et une date de fin pour les exercices affichés. 
    - avoir un résumé des lignes affichées (partie « Total ») 
    - avoir une pagination pour l’affichage de la liste (pages de 20 lignes par exemple, seule une partie des lignes s’affiche et un bouton permet d’afficher les lignes suivantes…)
Implémenter un de ces 3 bonus au moins, selon votre choix. 

Ca devra êrte un nouvel écran, accessible depuis le menu principal, qui affiche les résultats sous une forme proche de celle-ci.

Important ! Ca ne doit pas être affiché dans la console mais dans une interface graphique customtkinter.

"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import database
from tkinter import messagebox
from database import remove_match_record, fetch_game_statistics, retrieve_exercise_catalog


tree = None # Global
entry_pseudo = None
entry_exercise = None
lbl_nblignes = None
lbl_tempTotal = None
lbl_nbOK = None
lbl_nbTotal = None
lbl_pourcentageTotal = None
entry_date_debut = None
entry_date_fin = None
derniers_filtres = {"pseudo": "", "exercise": ""}
donnees_chargees = False # Pour suivre si les données ont été chargées

def create_result_window():
    global tree, entry_pseudo, entry_exercise, lbl_nblignes, lbl_tempTotal, lbl_nbOK, lbl_nbTotal, lbl_pourcentageTotal, entry_date_debut, entry_date_fin

    # Create a new window with CustomTkinter
    window = ctk.CTk()
    window.title("BRAINGAMES : Statistics")
    window.geometry("1300x700+300+150")

    # Title label
    lbl_title = ctk.CTkLabel(window, text="BRAINGAMES : Statistics", font=("Arial", 16))
    lbl_title.grid(row=0, column=0, columnspan=8, pady=(0, 20))

    # Pseudo input
    lbl_pseudo = ctk.CTkLabel(window, text="Pseudo:")
    lbl_pseudo.grid(row=1, column=0, sticky="e", padx=(0, 60))
    entry_pseudo = ctk.CTkEntry(window)
    entry_pseudo.grid(row=1, column=1, sticky="w", padx=(0, 60))

    # Exercise input
    lbl_exercice = ctk.CTkLabel(window, text="Exercice:")
    lbl_exercice.grid(row=1, column=2, sticky="e", padx=(0, 60))
    entry_exercise = ctk.CTkEntry(window)
    entry_exercise.grid(row=1, column=3, sticky="w", padx=(0, 60))

    # Date start input
    lbl_date_debut = ctk.CTkLabel(window, text="Date debut:")
    lbl_date_debut.grid(row=1, column=4, sticky="e", padx=(0, 60))
    entry_date_debut = ctk.CTkEntry(window)
    entry_date_debut.grid(row=1, column=5, sticky="w", padx=(0, 60))

    # Date end input
    lbl_date_fin = ctk.CTkLabel(window, text="Date fin:")
    lbl_date_fin.grid(row=1, column=6, sticky="e", padx=(0, 60))
    entry_date_fin = ctk.CTkEntry(window)
    entry_date_fin.grid(row=1, column=7, sticky="w", padx=(0, 60))

    # Buttons
    btn_voir_resultat = ctk.CTkButton(window, text="Voir Resultat", command=lambda: voir_resultat())
    btn_voir_resultat.grid(row=2, padx=(0, 5))
    btn_total = ctk.CTkButton(window, text="Total", command=lambda: voir_total())
    btn_total.grid(row=21, padx=(0, 0))
    btn_ajouter = ctk.CTkButton(window, text="Ajouter", command=ajouter_resultat)
    btn_ajouter.grid(row=2, column=3, padx=(0, 5))
    btn_supprimer = ctk.CTkButton(window, text="Supprimer", command=supprimer_resultat)
    btn_supprimer.grid(row=2, column=1, padx=(0, 5))
    btn_modifier = ctk.CTkButton(window, text="Modifier", command=modifier_resultat)
    btn_modifier.grid(row=2, column=2, padx=(0, 5))

    # Treeview (still using ttk as CTK does not provide a Treeview)
    tree = ttk.Treeview(window, height=20)
    tree["columns"] = ("Éléve", "Date Heure", "Temps", "Exercice", "NB OK", "Nb Trial", "% réussi")
    tree.column("#0", width=0, stretch=ctk.NO)
    for col in tree["columns"]:
        tree.column(col, width=150, anchor="center")
        tree.heading(col, text=col, anchor="center")
    tree.grid(row=3, column=0, columnspan=8)

    # Total section labels
    ctk.CTkLabel(window, text="NbLignes").grid(row=4, column=0, sticky='w')
    ctk.CTkLabel(window, text="Temps total").grid(row=4, column=1, sticky='w')
    ctk.CTkLabel(window, text="Nb OK").grid(row=4, column=2, sticky='w')
    ctk.CTkLabel(window, text="Nb Total").grid(row=4, column=3, sticky='w')
    ctk.CTkLabel(window, text="% Total").grid(row=4, column=4, sticky='w')

    # Total section dynamic labels
    lbl_nblignes = ctk.CTkLabel(window, text="")
    lbl_nblignes.grid(row=5, column=0, sticky='w')
    lbl_tempTotal = ctk.CTkLabel(window, text="")
    lbl_tempTotal.grid(row=5, column=1, sticky='w')
    lbl_nbOK = ctk.CTkLabel(window, text="")
    lbl_nbOK.grid(row=5, column=2, sticky='w')
    lbl_nbTotal = ctk.CTkLabel(window, text="")
    lbl_nbTotal.grid(row=5, column=3, sticky='w')
    lbl_pourcentageTotal = ctk.CTkLabel(window, text="")
    lbl_pourcentageTotal.grid(row=5, column=4, sticky='w')

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
        selected_item = tree.selection()[0]  # Select the item
    except IndexError:
        messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à modifier.")
        return

    current_values = tree.item(selected_item, 'values')

    # Open a new window for updating
    update_window = ctk.CTkToplevel()  # Using CustomTkinter
    update_window.title("Modifier un résultat")
    update_window.geometry("400x200+700+350")
    update_window.grab_set()  # Focus on this window

    # Input for Duration
    lbl_duration = ctk.CTkLabel(update_window, text="Temps:")
    lbl_duration.pack()
    entry_duration = ctk.CTkEntry(update_window)
    entry_duration.pack()
    entry_duration.insert(0, current_values[2])  # Default to original value

    # Input for nbok
    lbl_nbok = ctk.CTkLabel(update_window, text="Nb d’essais réussi:")
    lbl_nbok.pack()
    entry_nbok = ctk.CTkEntry(update_window)
    entry_nbok.pack()
    entry_nbok.insert(0, current_values[4])  # Default to original value

    # Input for NbTrials
    lbl_nbtrials = ctk.CTkLabel(update_window, text="Nb total:")
    lbl_nbtrials.pack()
    entry_nbtrials = ctk.CTkEntry(update_window)
    entry_nbtrials.pack()
    entry_nbtrials.insert(0, current_values[5])  # Default to original value

    # Update button
    btn_update = ctk.CTkButton(update_window, text="Update", command=lambda: update_result(selected_item, entry_duration.get(), entry_nbok.get(), entry_nbtrials.get()))
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
    """ Convert a given time string (HH:MM:SS) to seconds. """
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds

def colorize_percentage(percentage):
    """ Define colors based on the percentage. """
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
        total_duration += convert_time_to_seconds(values[2])  # Convert duration to seconds
        total_nbok += int(values[4])  # Add NbOk
        total_nbtrials += int(values[5])  # Add NbTrials

    # Calculate the average success rate
    if total_nbtrials > 0:
        total_pourcentage = (total_nbok / total_nbtrials) * 100
    else:
        total_pourcentage = 0

    # Update the labels with the total statistics
    lbl_nblignes.config(text=f"{total_lignes}")
    lbl_tempTotal.config(text=f"{total_duration} sec")
    lbl_nbOK.config(text=f"{total_nbok}")
    lbl_nbTotal.config(text=f"{total_nbtrials}")
    lbl_pourcentageTotal.config(text=f"{total_pourcentage:.2f}%")

def ajouter_resultat():
    global ajout_window

    # Create a new window for adding a result
    ajout_window = ctk.CTkToplevel()
    ajout_window.title("Ajouter un résultat")
    ajout_window.geometry("400x250+700+350")
    ajout_window.grab_set()  # Focus on this window

    # Input for "pseudo"
    lbl_pseudo = ctk.CTkLabel(ajout_window, text="Pseudo:")
    lbl_pseudo.pack()
    entry_pseudo = ctk.CTkEntry(ajout_window)
    entry_pseudo.pack()

    # Input for 'Exercice'
    lbl_exercice = ctk.CTkLabel(ajout_window, text="Exercice:")
    lbl_exercice.pack()
    entry_exercice = ctk.CTkEntry(ajout_window)
    entry_exercice.pack()

    # Input for 'Temps'
    lbl_temps = ctk.CTkLabel(ajout_window, text="Temps:")
    lbl_temps.pack()
    entry_temps = ctk.CTkEntry(ajout_window)
    entry_temps.pack()

    # Input for 'NB OK'
    lbl_nbok = ctk.CTkLabel(ajout_window, text="NB OK:")
    lbl_nbok.pack()
    entry_nbok = ctk.CTkEntry(ajout_window)
    entry_nbok.pack()

    # Input for 'Nb Trial'
    lbl_nbtrial = ctk.CTkLabel(ajout_window, text="Nb Trial:")
    lbl_nbtrial.pack()
    entry_nbtrial = ctk.CTkEntry(ajout_window)
    entry_nbtrial.pack()

    # Button to add the new result
    btn_ajouter = ctk.CTkButton(ajout_window, text="Ajouter résultat", command=lambda: enregistrer_resultat(
        entry_pseudo.get(),
        entry_exercice.get(),
        entry_temps.get(),
        entry_nbok.get(),
        entry_nbtrial.get()
    ))
    btn_ajouter.pack()

def enregistrer_resultat(pseudo, exercice, temps, nbok, nbtrials):
    global ajout_window

    # Verify if the exercise exists
    if not exercice_existe(exercice):
        existing_exercises = retrieve_exercise_catalog()
        messagebox.showwarning("Erreur", f"Cet exercice n'existe pas. Les exercices disponibles dans la BD sont: {', '.join(existing_exercises)}")
        return

    # Verify the time format
    if not format_temps_valide(temps):
        messagebox.showwarning("Erreur", "Format de temps invalide. Veuillez entrer le format HH:MM:SS.")
        return

    # Send data to the database
    database.save_game_result(pseudo, exercice, temps, nbok, nbtrials)
    refresh_treeview()

    # Display a success message
    messagebox.showinfo("Succès", "Données ajoutées avec succès !")

    # Close the add result window
    ajout_window.destroy()

def exercice_existe(exercice):
    """
    Checks if a given exercise exists in the database.
    """
    # Use the fetch_game_statistics function to check for the existence of the exercise
    resultats = fetch_game_statistics(exercise=exercice)

    # If no results are returned, the exercise does not exist
    return len(resultats) > 0

def format_temps_valide(temps_str):
    """
    Verifies if the given time string is in the correct format (HH:MM:SS).
    """
    try:
        heures, minutes, secondes = map(int, temps_str.split(':'))
        assert 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59
        return True
    except (ValueError, AssertionError):
        return False
