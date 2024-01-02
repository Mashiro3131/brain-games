import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import CTkTable 
from customtkinter import *
import database


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
        