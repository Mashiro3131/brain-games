import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import CTkTable
from CTkMessagebox import CTkMessagebox
from customtkinter import *
import database
from database import fetch_game_statistics, retrieve_exercise_catalog, remove_match_record
import display_results
import new_menu

"""

- [ ] Ajouter le tableau des résultats dans la frame statistiques
- [ ] Changer le treeview à CTkTable, faire en sorte que les colonnes se redimensionnent automatiquement et qu'on puisse faire la meme chose que avec le treeview
- [ ] Ajouter la fonctionnaliter de filtrer en asc et desc en cliquant sur les entêtes des colonnes
- [ ] Ajouter un autre sideframe sur la droite pour les filtres
- [ ] Ajouter l'option faire un bouton crud


"""

class Statistics(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.display_statistics()
        self.filtered_data = []  # Data filtered according to applied filters
        self.current_page = 0
        self.rows_per_page = 20
        self.loaded_data = False  # To track if data has been loaded
        self.parent = parent
        self.last_filters = {"pseudo": "", "exercise": "", "start_date": "", "end_date": ""}

    
    def display_statistics(self):
        
        def treeview_sort_column(self,tv,col,reverse):
            l = [(tv.set(k,col),k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val,k) in enumerate(l):
                tv.move(k,'',index)

            # reverse sort next time
            tv.heading(col,command=lambda: treeview_sort_column(tv,col,not reverse))
        
        # Main frame
        display_results_frame = ctk.CTkFrame(self, corner_radius=15)
        display_results_frame.pack_propagate(0)
        display_results_frame.pack(expand=True, fill='both', padx=15, pady=15)        
            
            
            
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Statistics", font=ctk.CTkFont(size=15, weight="bold"))
        self.title_label.pack(pady=20)

        # Filter frame
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10)

        # Pseudo filter
        self.pseudo_label = ctk.CTkLabel(self.filter_frame, text="Pseudo:")
        self.pseudo_label.grid(row=0, column=0, padx=15, pady=8)
        self.pseudo_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="PSEUDO01")
        self.pseudo_entry.grid(row=0, column=1, padx=5, pady=8)

        # Exercise filter
        self.exercise_label = ctk.CTkLabel(self.filter_frame, text="Exercise:")
        self.exercise_label.grid(row=0, column=2, padx=5, pady=8)
        self.exercise_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="EXE03")
        self.exercise_entry.grid(row=0, column=3, padx=5, pady=8)

        # Treeview setup
        self.treeview_frame = ctk.CTkFrame(self, corner_radius=15)
        self.treeview_frame.pack(expand=True, fill='both', padx=15, pady=15)

        self.tree = ttk.Treeview(self.treeview_frame, columns=("Pseudo", "Date Time", "Time", "Exercise", "NB OK", "NB Trials", "% Success"), show="headings", height=10)
        self.tree.column("#0", width=0, stretch=ctk.NO)

        # Configuring the columns and headings
        for col in self.tree["columns"]:
            self.tree.column(col, width=150, anchor="center")
            self.tree.heading(col, text=col, anchor="center")

        self.tree.pack(expand=True, fill='both', pady=20, padx=20)

        # Pagination frame and buttons
        self.pagination_frame = ctk.CTkFrame(self)
        self.pagination_frame.pack(pady=10)

        self.prev_page_button = ctk.CTkButton(self.pagination_frame, text="Previous Page", command=self.previous_page)
        self.prev_page_button.pack(side="left", padx=5, pady=5)

        self.next_page_button = ctk.CTkButton(self.pagination_frame, text="Next Page", command=self.next_page)
        self.next_page_button.pack(side="left", padx=5, pady=5)

        # Initial call to display results
        self.view_results()
   
   
    def display_home_frame_statistics(self):
        pass
    
     
    # def right_sidebar(self):
    #     right_sidebar_frame = CTkFrame(self, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
    #     right_sidebar_frame.pack_propagate(0)
    #     right_sidebar_frame.pack(side="right", anchor="w", fill="y")

    def insert_data_into_treeview(self, values, percentage):
        bgcolor, fgcolor = self.colorize_percentage(percentage)
        formatted_values = (*values, f"{percentage} %")
        row_id = self.tree.insert('', 'end', values=formatted_values)
        self.tree.tag_configure(row_id, background=bgcolor, foreground=fgcolor)
        self.tree.item(row_id, tags=(row_id,))

    def view_total(self):
        rows_total = 0
        duration_total = 0
        nbok_total = 0
        nbtrials_total = 0
        percentage_total = 0

        for child in self.tree.get_children():
            values = self.tree.item(child, 'values')
            rows_total += 1
            duration_total += self.convert_time_to_seconds(values[2])  # Convert duration to seconds
            nbok_total += int(values[4])  # Add NbOk
            nbtrials_total += int(values[5])  # Add NbTrials

        # Calculate the average success rate
        if nbtrials_total > 0:
            percentage_total = (nbok_total / nbtrials_total) * 100
        else:
            percentage_total = 0

        # Update the labels with the total statistics
        self.nbrows_label.configure(text=f"{rows_total}")
        self.duration_label.configure(text=f"{duration_total} seconds")
        self.nbok_label.configure(text=f"{nbok_total}")
        self.nbtotal_label.configure(text=f"{nbtrials_total}")
        self.percentage_label.configure(text=f"{percentage_total:.2f}%")
 
    def view_results(self):
        # Retrieve values from input fields
        pseudo = self.pseudo_entry.get().strip()
        exercise = self.exercise_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        # Check if filters have changed
        if (pseudo == self.last_filters["pseudo"] and
                exercise == self.last_filters["exercise"] and
                start_date == self.last_filters.get("start_date", "") and
                end_date == self.last_filters.get("end_date", "") and
                self.loaded_data):
            CTkMessagebox(title="Information", message="Les données sont déjà à jour.")
            CTkLabel
            return

        # Reload data if any filter has changed
        if (pseudo != self.last_filters["pseudo"] or
                exercise != self.last_filters["exercise"] or
                start_date != self.last_filters.get("start_date", "") or
                end_date != self.last_filters.get("end_date", "")):
            self.loaded_data = False

        # Save the current filters
        self.last_filters.update({"pseudo": pseudo, "exercise": exercise, "start_date": start_date, "end_date": end_date})

        # Fetch results from the database
        results, _ = database.fetch_game_statistics(pseudo=pseudo, exercise=exercise, start_date=start_date,
                                                    end_date=end_date)

        # Store the filtered data and reset the current page
        self.filtered_data = results
        self.current_page = 0
        self.loaded_data = True

        # Display the current page of results
        self.display_current_page()

    def display_current_page(self):
        
        # Calculate the slice of the data to display
        start_index = self.current_page * self.rows_per_page
        end_index = start_index + self.rows_per_page
        page_data = self.filtered_data[start_index:end_index]

        # Clear existing data in the treeview
        self.tree.delete(*self.tree.get_children())

        # Insert new data for the current page
        for result in page_data:
            nbok = result[4]
            nbtrials = result[5]
            percentage = self.calculate_percentage(nbok, nbtrials)
            self.insert_data_into_treeview(result, percentage)

        # Update total statistics
        self.view_total()

    def next_page(self):
        # Increment the current page number
        self.current_page += 1
        self.display_current_page()
        # # Logic to fetch the next set of data based on the current page
        # # You'll need to adapt this to your application's data fetching and pagination logic
        # start_index = self.current_page * self.rows_per_page
        # end_index = start_index + self.rows_per_page
        # page_data = self.filtered_data[start_index:end_index]

        # # Clear existing data in the treeview
        # self.tree.delete(*self.tree.get_children())

        # # Insert new data for the current page
        # for result in page_data:
        #     self.tree.insert('', 'end', values=result)

        # # Update total statistics, if applicable
        # self.update_total_statistics()

    def previous_page(self):
        
        self.current_page = max(0, self.current_page - 1)
        self.display_current_page()
        
        # # Decrement the current page number, ensuring it doesn't go below zero
        # self.current_page = max(0, self.current_page - 1)

        # # Logic to fetch the set of data for the previous page
        # # This needs to be adapted to your application's data fetching and pagination logic
        # start_index = self.current_page * self.rows_per_page
        # end_index = start_index + self.rows_per_page
        # page_data = self.filtered_data[start_index:end_index]

        # # Clear existing data in the treeview
        # self.tree.delete(*self.tree.get_children())

        # # Insert data for the current page
        # for result in page_data:
        #     self.tree.insert('', 'end', values=result)

        # # Update total statistics, if applicable
        # self.update_total_statistics()   
        
    def modify_results(self):
        try:
            selected_item = self.tree.selection()[0]  # Select the item
        except IndexError:
            messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à modifier.")
            return

        current_values = self.tree.item(selected_item, 'values')

        # Open a new window for updating
        self.update_window = ctk.CTkToplevel()  # Using CustomTkinter
        self.update_window.title("Modifier un résultat")
        self.update_window.geometry("400x200+700+350")
        self.update_window.grab_set()  # Focus on this window

        # Input for Duration
        duration_label = ctk.CTkLabel(self.update_window, text="Time:")
        duration_label.pack()
        self.duration_entry = ctk.CTkEntry(self.update_window)
        self.duration_entry.pack()
        self.duration_entry.insert(0, current_values[2])  # Default to original value

        # Input for nbok
        nbok_label = ctk.CTkLabel(self.update_window, text="Correct attempts:")
        nbok_label.pack()
        self.nbok_entry = ctk.CTkEntry(self.update_window)
        self.nbok_entry.pack()
        self.nbok_entry.insert(0, current_values[4])  # Default to original value

        # Input for NbTrials
        nbtrials_label = ctk.CTkLabel(self.update_window, text="NB Total")
        nbtrials_label.pack()
        self.nbtrials_entry = ctk.CTkEntry(self.update_window)
        self.nbtrials_entry.pack()
        self.nbtrials_entry.insert(0, current_values[5])  # Default to original value

        # Update button
        update_button = ctk.CTkButton(self.update_window, text="Update",
                                      command=lambda: self.update_result(selected_item, self.duration_entry.get(), self.nbok_entry.get(),
                                                                         self.nbtrials_entry.get()))
        update_button.pack()
        
    def update_results(self, selected_item, new_duration, new_nbok, new_nbtrials):
        current_values = self.tree.item(selected_item, 'values')
        pseudo = current_values[0]  # pour pseudo
        date_hour = current_values[1]  # pour date
        duration = current_values[2]  # pour temps
        exercise = current_values[3]  # pour exercise
        nbok = current_values[4]  # pour nbok
        nbtrials = current_values[5]  # pour nbtrials

        # Update the database
        database.revise_game_outcome(pseudo, exercise, date_hour, duration, nbok, nbtrials, new_duration, new_nbok,
                                     new_nbtrials)

        # Update the treeview
        updated_values = (pseudo, exercise, date_hour, new_duration, new_nbok, new_nbtrials,
                          self.calculate_percentage(int(new_nbok), int(new_nbtrials)))
        
        self.tree.item(selected_item, values=updated_values)

        self.refresh_treeview()

        self.update_window.destroy()        

    def delete_results(self):
        try:
            selected_item = self.tree.selection()[0]  # Select the item
        except IndexError:
            messagebox.showwarning("Attention", "Veuillez sélectionner la ligne à supprimer.")
            return

        current_values = self.tree.item(selected_item, 'values')

        pseudo = current_values[0]  # pour pseudo
        date_hour = current_values[1]
        duration = current_values[2]
        exercise = current_values[3]
        nbok = current_values[4]
        nbtrials = current_values[5]
        
        # Delete the result from the database
        database.remove_match_record(pseudo, exercise, date_hour, duration, nbok, nbtrials)
        self.tree.delete(selected_item)
        
    def refresh_treeview(self):
        # Clear all existing data in the treeview
        self.tree.delete(*self.tree.get_children())

        # Fetch updated data from the database
        results, _ = database.fetch_game_statistics()  # Adapt this to your actual database call

        # Populate the treeview with the new data
        for result in results:
            if isinstance(result, (list, tuple)):
                nbok = result[4]
                nbtrials = result[5]
                percentage = self.calculate_percentage(nbok, nbtrials)
                self.insert_data_into_treeview(result, percentage)
            else:
                self.insert_data_into_treeview(result, 0)
                
    def calculate_percentage(self, nbok, nbtrials):
        if isinstance(nbtrials, int) and nbtrials > 0:
            return round((nbok / nbtrials) * 100, 2)
        else:
            return 0

    def convert_time_to_seconds(self, time_str):
        """ Convert a given time string (HH:MM:SS) to seconds. """
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def colorize_percentage(self, percentage):
        """ Define colors based on the percentage. """
        if percentage < 25:
            return ('#800000', 'white')  # At the bottom... please do better
        elif percentage < 50:
            return ('#cc5500', 'white')  # Below average
        elif percentage < 75:
            return ('#add8e6', 'black')  # Average results
        else:
            return ('#228b22', 'white')  # Excellent
        
    def add_results(self):
        # Create a new window for adding a result
        self.add_window = ctk.CTkToplevel()
        self.add_window.title("Ajouter un résultat")
        self.add_window.geometry("400x250+700+350")
        self.add_window.grab_set()  # Focus on this window

        # Input for "pseudo"
        pseudo_label = ctk.CTkLabel(self.add_window, text="Pseudo:")
        pseudo_label.pack()
        self.pseudo_entry = ctk.CTkEntry(self.add_window)
        self.pseudo_entry.pack()

        # Input for 'Exercice'
        exercise_label = ctk.CTkLabel(self.add_window, text="Exercice:")
        exercise_label.pack()
        self.exercise_entry = ctk.CTkEntry(self.add_window)
        self.exercise_entry.pack()

        # Input for 'Temps'
        time_label = ctk.CTkLabel(self.add_window, text="Temps:")
        time_label.pack()
        self.time_entry = ctk.CTkEntry(self.add_window)
        self.time_entry.pack()

        # Input for 'NB OK'
        nbok_label = ctk.CTkLabel(self.add_window, text="NB OK:")
        nbok_label.pack()
        self.nbok_entry = ctk.CTkEntry(self.add_window)
        self.nbok_entry.pack()

        # Input for 'NB Trial'
        nbtrials_label = ctk.CTkLabel(self.add_window, text="NB Trials:")
        nbtrials_label.pack()
        self.nbtrial_entry = ctk.CTkEntry(self.add_window)
        self.nbtrial_entry.pack()

        # Button to add the new result
        add_result_button = ctk.CTkButton(self.add_window, text="Ajouter résultat", command=self.save_results)
        add_result_button.pack()    
    
    def save_results(self):
        pseudo = self.pseudo_entry.get()
        exercise = self.exercise_entry.get()
        temps = self.time_entry.get()
        nbok = self.nbok_entry.get()
        nbtrials = self.nbtrial_entry.get()

        # Verify if the exercise exists
        if not self.check_exercise_exists(exercise):
            existing_exercises = retrieve_exercise_catalog()
            messagebox.showwarning("Erreur",
                                   f"Cet exercise n'existe pas. Les exercices disponibles dans la BD sont: {', '.join(existing_exercises)}")
            return

        # Verify the time format
        if not self.time_format(temps):
            messagebox.showwarning("Erreur", "Format de temps invalide. Veuillez entrer le format HH:MM:SS.")
            return

        # Send data to the database
        database.save_game_result(pseudo, exercise, temps, nbok, nbtrials)
        self.refresh_treeview()

        # Display a success message
        messagebox.showinfo("Succès", "Données ajoutées avec succès !")

        # Close the add result window
        self.add_window.destroy()    
        
    def check_exercise_exists(self, exercise):
        """
        Checks if a given exercise exists in the database.
        """
        results = fetch_game_statistics(exercise=exercise)  # Adapt to actual database call
        return len(results) > 0

    def time_format(self, temps_str):
        """
        Verifies if the given time string is in the correct format (HH:MM:SS).
        """
        try:
            heures, minutes, secondes = map(int, temps_str.split(':'))
            assert 0 <= heures <= 23 and 0 <= minutes <= 59 and 0 <= secondes <= 59
            return True
        except (ValueError, AssertionError):
            return False
        
if __name__ == "__main__":
    window = ctk.CTk()  # or ctk.CTk() if you are using customtkinter for the main window
    app = Statistics(window)
    app.pack(expand=True, fill="both")
    window.mainloop()