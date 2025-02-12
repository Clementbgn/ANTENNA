import time
import os
from PIL import Image
from tkinter import filedialog
import threading 
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from skyfield.api import load, EarthSatellite, wgs84

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Configuration de la fenêtre principale
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("dark-blue")  

# Données des satellites
SATELLITES = {
    "ISS (Zarya)": ["1", "1", "1", "1", "1"],
    "Hubble Space Telescope": ["1", "1", "1", "1", "1"],
    "NOAA 19": ["1", "1", "1", "1", "1"]
}

# Création de la fenêtre principale
root = ctk.CTk()
root.title("Satellite Tracker")
root.geometry("800x600")

# Conteneur principal avec marge
main_frame = ctk.CTkFrame(root, fg_color="#001f3f", corner_radius=15)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Titre
title_label = ctk.CTkLabel(main_frame, text="ESTACA SATELLITE TRACKER", font=("DengXian", 24, "bold"))
title_label.pack(pady=15)

# Barre de recherche
search_var = tk.StringVar()
search_entry = ctk.CTkEntry(main_frame, textvariable=search_var, width=400, placeholder_text="Rechercher un satellite", corner_radius=10)
search_entry.pack(pady=10)

# Fonction de recherche
def search_satellites(*args):
    search_term = search_var.get().lower()
    for item in satellite_tree.get_children():
        satellite_tree.delete(item)
    for sat, details in SATELLITES.items():
        if search_term in sat.lower():
            satellite_tree.insert("", "end", values=[sat] + details)

search_var.trace("w", search_satellites)

# Tableau des satellites
columns = ("Nom", "ID", "Fréquence", "Prochaine Fenêtre", "Visibilité", "Station au Sol")
satellite_tree = ttk.Treeview(main_frame, columns=columns, show="headings")

# Style du tableau
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#002b5c",  # Fond bleu clair pour contraster
                fieldbackground="#002b5c",
                foreground="white",  # Texte en blanc
                rowheight=30,
                bordercolor="white",  # Bordures en blanc
                borderwidth=1)
style.configure("Treeview.Heading",
                font=("DengXian", 12),
                background="#004080",  # En-têtes plus visibles
                foreground="white",
                bordercolor="white",
                borderwidth=1)
style.map("Treeview",
          background=[('selected', '#00509E')],
          foreground=[('selected', 'white')])

# Configuration des colonnes
for col in columns:
    satellite_tree.heading(col, text=col)
    satellite_tree.column(col, width=120, anchor="center")

# Insertion des données initiales
for sat, details in SATELLITES.items():
    satellite_tree.insert("", "end", values=[sat] + details)

# Encadrement pour ajouter des coins arrondis au tableau
frame_container = ctk.CTkFrame(main_frame, fg_color="#001f3f", corner_radius=15)
frame_container.pack(pady=15, padx=15, fill="both", expand=True)

satellite_tree.pack(in_=frame_container, fill="both", expand=True)

# Fonction de sélection d'un satellite
def on_satellite_selected(event):
    selected_item = satellite_tree.selection()
    if selected_item:
        sat_name = satellite_tree.item(selected_item, "values")[0]
        print(f"Satellite sélectionné : {sat_name}")

satellite_tree.bind("<<TreeviewSelect>>", on_satellite_selected)

root.mainloop()


