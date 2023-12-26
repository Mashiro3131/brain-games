"""
SQL de la base de données pour les références
"""

"""
4. Affichage des résultats 
On souhaite maintenant un nouvel écran, accessible depuis le menu principal, qui affiche les résultats sous une forme proche de celle-ci. 
Si possible on aimerait pouvoir filtrer au moins par élève et exercise. En bonus, on aimerait aussi : 

    - filtrer en donnant une date de début et une date de fin pour les exercices affichés. 
    - avoir un résumé des lignes affichées (partie « Total ») 
    - avoir une pagination pour l’affichage de la liste (pages de 20 lignes par exemple, seule une partie des lignes s’affiche et un bouton permet d’afficher les lignes suivantes…)
Implémenter un de ces 3 bonus au moins, selon votre choix. 

Ca devra êrte un nouvel écran, accessible depuis le menu principal, qui affiche les résultats sous une forme proche de celle-ci.

Important ! Ca ne doit pas être affiché dans la console mais dans une interface graphique customtkinter.

"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import database
from database import remove_match_record, fetch_game_statistics, retrieve_exercise_catalog


tree = None # Global
pseudo_entry = None
exercise_entry = None
start_date_entry = None
end_date_entry = None

nbrows_label = None
duration_label = None
nbok_label = None
nbtotal_label = None
percentage_label = None

last_filters = {"pseudo": "", "exercise": ""}
loaded_data = False # Pour suivre si les données ont été chargées

def display_results():
    global tree, pseudo_entry, exercise_entry, start_date_entry, end_date_entry, duration_label, nbok_label, nbtotal_label, percentage_label, nbrows_label


    """ Initialization """
    
    # Main window
    window = ctk.CTk()
    window.title("BRAINGAMES : STATISTICS")
    window.geometry("1300x700+300+150")

    # Title
    title_label = ctk.CTkLabel(window, text="Statistics", font=ctk.CTkFont(size=15, weight="bold"))
    title_label.pack(pady=20)



    """ Filters """
    
    # Filter frame
    filter_frame = ctk.CTkFrame(window)
    filter_frame.pack(pady=10)


    # Pseudo filter
    pseudo_label = ctk.CTkLabel(filter_frame, text="Pseudo:")
    pseudo_label.grid(row=0, column=0, padx=15, pady=8)
    pseudo_entry = ctk.CTkEntry(filter_frame)
    pseudo_entry.grid(row=0, column=1, padx=5, pady=8)

    
    # Exercise filter
    exercise_label = ctk.CTkLabel(filter_frame, text="Exercise:")
    exercise_label.grid(row=0, column=2, padx=5, pady=8)
    exercise_entry = ctk.CTkEntry(filter_frame)
    exercise_entry.grid(row=0, column=3, padx=5, pady=8)


    # Start date filter
    start_date_label = ctk.CTkLabel(filter_frame, text="Start Date:")
    start_date_label.grid(row=0, column=4, padx=5, pady=8)
    start_date_entry = ctk.CTkEntry(filter_frame)
    start_date_entry.grid(row=0, column=5, padx=5, pady=8)


    # End date filter
    end_date_label = ctk.CTkLabel(filter_frame, text="End Date:")
    end_date_label.grid(row=0, column=6, padx=5, pady=8)
    end_date_entry = ctk.CTkEntry(filter_frame)
    end_date_entry.grid(row=0, column=7, padx=5, pady=8)

    
    # Display Data Button
    display_statistics_button = ctk.CTkButton(filter_frame, text="Search !", command=view_results)
    display_statistics_button.grid(row=0, column=8, padx=15, pady=8)
    
    
    """ Treeview """
    
    # Treeview under-frame
    treeview_frame = ctk.CTkFrame(window, corner_radius=15)
    treeview_frame.pack(expand=True, fill='both', padx=15, pady=15)

    # Treeview main frame
    tree = ttk.Treeview(treeview_frame, columns=("Pseudo", "Date Time", "Time", "Exercise", "NB OK", "NB Trials", "% Success"), show="headings", height=10)  # Adjust the height here
    tree.column("#0", width=0, stretch=ctk.NO)

    for col in tree["columns"]:
        tree.column(col, width=150, anchor="center")
        tree.heading(col, text=col, anchor="center")

    tree.pack(expand=True, fill='both', pady=20, padx=20)  # Adjust padding here



    # Custom Treeview Styling
    style = ttk.Style(window)
    style.theme_use("default")
    
    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#343638",
                    bordercolor="#343638",
                    borderwidth=0)
    
    style.map('Treeview',
              background=[('selected', '#22559b')])
    
    style.configure("Treeview.Heading",
                    background="#565b5e",
                    foreground="white",
                    relief="flat")
    
    style.map("Treeview.Heading",
              background=[('active', '#3484F0')])
    
    
    
    # Total statistics frame (under the treeview) but in the same frame as the treeview
    nbtotal_label
    
    
    

    window.mainloop()



    """ Total Statistics """
    
    # Total statistics frame (under the treeview) like we did for the filters like this: 


def display_total_statistics():
    pass





# CREATE
def insert_data_into_treeview(tree, values, percentage):
    bgcolor, fgcolor = colorize_percentage(percentage)
    formatted_values = (*values, f"{percentage} %")
    row_id = tree.insert('', 'end', values=formatted_values)
    tree.tag_configure(row_id, background=bgcolor, foreground=fgcolor)
    tree.item(row_id, tags=(row_id,))

# READ
def view_results():
    global loaded_data, last_filters

    # Retrieve values from input fields
    pseudo = pseudo_entry.get().strip()
    exercise = exercise_entry.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    # Check if filters have changed
    if (pseudo == last_filters["pseudo"] and
        exercise == last_filters["exercise"] and
        start_date == last_filters.get("start_date", "") and
        end_date == last_filters.get("end_date", "") and
        loaded_data):
        messagebox.showinfo("Information", "Les données sont déjà à jour.")
        return

    # Reload data if any filter has changed
    if (pseudo != last_filters["pseudo"] or
        exercise != last_filters["exercise"] or
        start_date != last_filters.get("start_date", "") or
        end_date != last_filters.get("end_date", "")):
        loaded_data = False

    # Save the current filters
    last_filters.update({"pseudo": pseudo, "exercise": exercise, "start_date": start_date, "end_date": end_date})

    # Fetch results from the database
    results, _ = database.fetch_game_statistics(pseudo=pseudo, exercise=exercise, start_date=start_date, end_date=end_date)

    # Check if results are available
    if not results:
        messagebox.showwarning("Erreur", "Aucun enregistrement trouvé pour les critères donnés.")
        loaded_data = False
        return

    # Clear existing data and display new results in Treeview
    tree.delete(*tree.get_children())
    for result in results:
        nbok = result[4]
        nbtrials = result[5]
        percentage = calculate_percentage(nbok, nbtrials)
        insert_data_into_treeview(tree, result, percentage)

    # Mark that data has been loaded
    loaded_data = True

# UPADTE

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
    duration_label = ctk.CTkLabel(update_window, text="Time:")
    duration_label.pack()
    duration_entry = ctk.CTkEntry(update_window)
    duration_entry.pack()
    duration_entry.insert(0, current_values[2])  # Default to original value

    # Input for nbok
    nbok_label = ctk.CTkLabel(update_window, text="Correct attempts:")
    nbok_label.pack()
    nbok_entry = ctk.CTkEntry(update_window)
    nbok_entry.pack()
    nbok_entry.insert(0, current_values[4])  # Default to original value

    # Input for NbTrials
    nbtrails_label = ctk.CTkLabel(update_window, text="NB Total")
    nbtrails_label.pack()
    nbtrials_entry = ctk.CTkEntry(update_window)
    nbtrials_entry.pack()
    nbtrials_entry.insert(0, current_values[5])  # Default to original value

    # Update button
    update_button = ctk.CTkButton(update_window, text="Update", command=lambda: update_result(selected_item, duration_entry.get(), nbok_entry.get(), nbtrials_entry.get()))
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
    database.revise_game_outcome(pseudo, exercise, date_hour, duration, nbok,nbtrials, new_duration, new_nbok, new_nbtrials)

    # mise a jour de tkinter
    updated_values = (pseudo, exercise, date_hour, new_duration, new_nbok, new_nbtrials, calculate_percentage(int(new_nbok), int(new_nbtrials)))
    tree.item(selected_item, values=updated_values)

    refresh_treeview()

    update_window.destroy()

# DELETE
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

    remove_match_record(pseudo, exercise, date_hour, duration, nbok, nbtrials)
    tree.delete(selected_item)



def refresh_treeview():
    # Clear all existing data in the treeview
    tree.delete(*tree.get_children())

    # Fetch updated data from the database
    results, _ = database.fetch_game_statistics()  # Assuming the second value (total) is not used here
    for result in results:
        if isinstance(result, (list, tuple)):
            nbok = result[4]
            nbtrials = result[5]
            percentage = calculate_percentage(nbok, nbtrials)
            insert_data_into_treeview(tree, result, percentage)

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
        return ('#800000', 'white') # At the bottom... please do better
    elif percentage < 50:
        return ('#cc5500', 'white') # Below average
    elif percentage < 75:
        return ('#add8e6', 'black') # Average results
    else:
        return ('#228b22', 'white') # Excellent


def view_total():
    rows_total = 0
    duration_total = 0
    nbok_total = 0
    nbtrials_total = 0
    percentage_total = 0

    for child in tree.get_children():
        values = tree.item(child, 'values')
        rows_total += 1
        duration_total += convert_time_to_seconds(values[2])  # Convert duration to seconds
        nbok_total += int(values[4])  # Add NbOk
        nbtrials_total += int(values[5])  # Add NbTrials

    # Calculate the average success rate
    if nbtrials_total > 0:
        percentage_total = (nbok_total / nbtrials_total) * 100
    else:
        percentage_total = 0

    # Update the labels with the total statistics
    nbrows_label.config(text=f"{rows_total}")
    duration_label.config(text=f"{duration_total} sec")
    nbok_label.config(text=f"{nbok_total}")
    nbtotal_label.config(text=f"{nbtrials_total}")
    percentage_label.config(text=f"{percentage_total:.2f}%")

def add_results():
    global add_window

    # Create a new window for adding a result
    add_window = ctk.CTkToplevel()
    add_window.title("Ajouter un résultat")
    add_window.geometry("400x250+700+350")
    add_window.grab_set()  # Focus on this window

    # Input for "pseudo"
    pseudo_label = ctk.CTkLabel(add_window, text="Pseudo:")
    pseudo_label.pack()
    pseudo_entry = ctk.CTkEntry(add_window)
    pseudo_entry.pack()

    # Input for 'Exercice'
    exercise_label = ctk.CTkLabel(add_window, text="Exercice:")
    exercise_label.pack()
    exercise_entry = ctk.CTkEntry(add_window)
    exercise_entry.pack()

    # Input for 'Temps'
    time_label = ctk.CTkLabel(add_window, text="Temps:")
    time_label.pack()
    time_entry = ctk.CTkEntry(add_window)
    time_entry.pack()

    # Input for 'NB OK'
    nbok_label = ctk.CTkLabel(add_window, text="NB OK:")
    nbok_label.pack()
    nbok_entry = ctk.CTkEntry(add_window)
    nbok_entry.pack()

    # Input for 'NB Trial'
    nbtrials_label = ctk.CTkLabel(add_window, text="NB Trials:")
    nbtrials_label.pack()
    nbtrial_entry = ctk.CTkEntry(add_window)
    nbtrial_entry.pack()

    # Button to add the new result
    add_result = ctk.CTkButton(add_window, text="Ajouter résultat", command=lambda: save_results(
        pseudo_entry.get(),
        exercise_entry.get(),
        time_entry.get(),
        nbok_entry.get(),
        nbtrial_entry.get()
    ))
    add_result.pack()

def save_results(pseudo, exercise, temps, nbok, nbtrials):
    global add_window

    # Verify if the exercise exists
    if not check_exercise_exists(exercise):
        existing_exercises = retrieve_exercise_catalog()
        messagebox.showwarning("Erreur", f"Cet exercise n'existe pas. Les exercices disponibles dans la BD sont: {', '.join(existing_exercises)}")
        return

    # Verify the time format
    if not time_format(temps):
        messagebox.showwarning("Erreur", "Format de temps invalide. Veuillez entrer le format HH:MM:SS.")
        return

    # Send data to the database
    database.save_game_result(pseudo, exercise, temps, nbok, nbtrials)
    refresh_treeview()

    # Display a success message
    messagebox.showinfo("Succès", "Données ajoutées avec succès !")

    # Close the add result window
    add_window.destroy()

def check_exercise_exists(exercise):
    """
    Checks if a given exercise exists in the database.
    """
    # Use the fetch_game_statistics function to check for the existence of the exercise
    results = fetch_game_statistics(exercise=exercise)

    # If no results are returned, the exercise does not exist
    return len(results) > 0

def time_format(temps_str):
    """
    Verifies if the given time string is in the correct format (HH:MM:SS).
    """
    try:
        heures, minutes, secondes = map(int, temps_str.split(':'))
        assert 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59
        return True
    except (ValueError, AssertionError):
        return False
