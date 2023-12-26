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

import datetime
from tkinter import *
import customtkinter as ctk
from database import *
import tkinter.ttk as ttk




class ResultDisplay():
    def __init__(self):
        # Create the main window 
        self.root = ctk.CTk()
        self.root.title("Statisques")
        self.root.geometry("1300x390")
        
        title_label = ctk.CTkLabel(self.root, text="Statistiques", font=ctk.CTkFont(size=15, weight="bold"))
        title_label.grid(row=0, column=0, ipady=20, padx=40, pady=40)
        title_label.pack()
        
        # Create and configure the filter options
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.pack()

        student_label = ctk.CTkLabel(filter_frame, text="Student:")
        student_label.grid(row=0, column=0, padx=5, pady=5)

        student_entry = ctk.CTkEntry(filter_frame)
        student_entry.grid(row=0, column=1, padx=5, pady=5)

        exercise_label = ctk.CTkLabel(filter_frame, text="Exercise:")
        exercise_label.grid(row=0, column=2, padx=5, pady=5)

        exercise_entry = ctk.CTkEntry(filter_frame)
        exercise_entry.grid(row=0, column=3, padx=5, pady=5)

        start_date_label = ctk.CTkLabel(filter_frame, text="Start Date:")
        start_date_label.grid(row=0, column=4, padx=5, pady=5)

        start_date_entry = ctk.CTkEntry(filter_frame)
        start_date_entry.grid(row=0, column=5, padx=5, pady=5)

        end_date_label = ctk.CTkLabel(filter_frame, text="End Date:")
        end_date_label.grid(row=0, column=6, padx=5, pady=5)

        end_date_entry = ctk.CTkEntry(filter_frame)
        end_date_entry.grid(row=0, column=7, padx=5, pady=5)

        # Create the result table
        self.result_table = ttk.Treeview(self.root, columns=("Student", "Exercise", "Date", "Duration", "Trials", "Success"), show="headings")
        self.result_table.heading("Student", text="Student") 
        self.result_table.heading("Exercise", text="Exercise")
        self.result_table.heading("Date", text="Date")
        self.result_table.heading("Duration", text="Duration")
        self.result_table.heading("Trials", text="Trials")
        self.result_table.heading("Success", text="Success")
        self.result_table.pack()

        # Configure the treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Apply the configured style to the result_table treeview widget
        self.result_table.configure(style="Treeview")

        # Create the summary section
        self.summary_label = ctk.CTkLabel(self.root, text="Total: 0 rows")
        self.summary_label.pack()

        # Create the pagination buttons
        self.prev_button = ctk.CTkButton(self.root, text="Previous", command=self.show_previous_results)
        self.prev_button.pack(side=LEFT)

        self.next_button = ctk.CTkButton(self.root, text="Next", command=self.show_next_results)
        self.next_button.pack(side=RIGHT)

        # Initialize variables
        self.page_size = 20
        self.current_page = 1
        self.total_rows = 0
        self.filtered_results = []

    def query_results(self, student, exercise, start_date, end_date):
        # Query the database based on the filter options
        results = []
        return results

    def update_results(self):
        student = self.student_entry.get()
        exercise = self.exercise_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        # Query the database based on the filter options
        self.filtered_results = self.query_results(student, exercise, start_date, end_date)

        # Update the total rows count
        self.total_rows = len(self.filtered_results)
        self.summary_label.config(text=f"Total: {self.total_rows} rows")

        # Reset the current page to 1
        self.current_page = 1

        # Show the results for the current page
        self.show_current_results()

    def show_current_results(self):
        # Calculate the start and end indices for the current page
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size

        # Get the results for the current page
        current_results = self.filtered_results[start_index:end_index]

        # Clear the table
        self.result_table.clear() # self.result_table.delete(*self.result_table.get_children())

        # Populate the table with the current results
        for result in current_results:
            self.result_table.add_row(result) # self.result_table.insert("", "end", values=result)     


    def show_previous_results(self):
        # Decrease the current page by 1
        self.current_page -= 1

        # Check if the current page is out of bounds
        if self.current_page < 1:
            self.current_page = 1

        # Show the results for the current page
        self.show_current_results()

    def show_next_results(self):
        # Calculate the total number of pages
        total_pages = (self.total_rows + self.page_size - 1) // self.page_size

        # Increase the current page by 1
        self.current_page += 1

        # Check if the current page is out of bounds
        if self.current_page > total_pages:
            self.current_page = total_pages

        # Show the results for the current page
        self.show_current_results()
    
    # It will be put under the total rows displaying the number of rows, the total duration, the total number of trials that were successful and the total number of trials
    # for e.g. Total: 10 rows, 00:00:00 duration, 5 successful trials, 10 trials, 50% success rate
    #            12             
        

    def run(self):
        # Run the main event loop
        self.root.mainloop()

# Create an instance of ResultDisplay and run it
result_display = ResultDisplay()
result_display.run()
        
