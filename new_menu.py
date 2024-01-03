import os
from customtkinter import *
import customtkinter as ctk
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from tkinter import font
import matplotlib.pyplot as plt
import geo01, info02, info05
from new_display_results import Statistics



script_directory = os.path.dirname(os.path.abspath(__file__))

assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


os.chdir(script_directory)

app = CTk()
app.title("Brain Games")
app.iconbitmap(os.path.join(assets_folder,"braingames_dark_ico.ico"))
app.geometry("856x645")
app.resizable(0,0)
app.configure(fg_color="#00002E")

braingames_title_font = CTkFont(family="Test Söhne Kräftig", size=40, weight="bold")
braingames_subtitle_font = CTkFont(family="Test Söhne", size=40)
braingames_regular_font = CTkFont(family="Test Söhne", size=14)
braingames_sidebar_button_font = CTkFont(family="Test Söhne ", size=15, weight="bold")
set_appearance_mode("dark")


""" --- Fonts --- """
# Sidebar Font --> Sharp Grotesk Medium 20
# Title Font --> Söhne Kräftig Bold
# Regular Text Font --> Söhne  20

""" --- Colors --- """
# Purple --> #400241
# Dull Lime --> #51d743
# Background Blue --> #00002E
# Text Light Lavender --> #d292ff
# Button Color --> #0000ff
# Button Hover Color --> #3c46ff

# TODO Créer les images dans adobe illustrator et ajouter les images den light et dark si possible ainsi que le texte en blanc et noir
# TODO Couleurs : Loulou purple (#400241) for the BG and Dull Lime (#51d743) for text and logos, Gris --> #E5E5E5, Blanc --> #FFFFFF, Noir --> #000000

""" Images """ # TODO if needed, add the dark mode images if the switch theme is still on the app

# Main Brain Games Logo in Sidebar
braingames_img_light_data = Image.open(os.path.join(assets_folder, "braingames_logo.png"))
# braingames_img_dark_data = Image.open(os.path.join(assets_folder, "braingames_dark.png"))
braingames_img = CTkImage(dark_image=braingames_img_light_data, light_image=braingames_img_light_data, size=(87.68, 83,78))

# Home (Menu) Icon in Sidebar
home_img_light_data = Image.open(os.path.join(assets_folder, "home_light.png"))
home_img_dark_data = Image.open(os.path.join(assets_folder, "home_light.png")) # home_dark.png
home_img = CTkImage(dark_image=home_img_dark_data, light_image=home_img_light_data)

# Geo01 (GeoGame) Icon in Home Frame
geo01_img_light_data = Image.open(os.path.join(img_folder, "geo01_button.png"))
geo01_img_dark_data = Image.open(os.path.join(img_folder, "geo01_button.png"))
geo01_img = CTkImage(dark_image=geo01_img_dark_data, light_image=geo01_img_light_data, size=(236, 283))

# Info02 (InfoGame) Icon in Home Frame
info02_img_light_data = Image.open(os.path.join(img_folder, "info02_button.png"))
info02_img_dark_data = Image.open(os.path.join(img_folder, "info02_button.png"))
info02_img = CTkImage(dark_image=info02_img_dark_data, light_image=info02_img_light_data, size=(315, 122))

# Info05 (InfoGame) Icon in Home Frame
info05_img_light_data = Image.open(os.path.join(img_folder, "info05_button.png"))
info05_img_dark_data = Image.open(os.path.join(img_folder, "info05_button.png"))
info05_img = CTkImage(dark_image=info05_img_dark_data, light_image=info05_img_light_data,  size=(315, 122))

# Statistics (display_results) Icon in Sidebar
statistics_img_light_data = Image.open(os.path.join(assets_folder, "analytics_icon.png"))
statistics_img_dark_data = Image.open(os.path.join(assets_folder, "analytics_icon.png")) # TODO Changer l'image
statistics_img = CTkImage(dark_image=statistics_img_light_data, light_image=statistics_img_light_data)

# Orders (user_list_icon) Icon in Sidebar (it will only be visible for the admin and the teachers that have a role number "2", from there we can CRUD the users (students)))
users_img_light_data = Image.open(os.path.join(assets_folder, "user_list_icon.png"))
users_img_dark_data = Image.open(os.path.join(assets_folder, "user_list_icon.png")) # TODO Changer l'image
users_img = CTkImage(dark_image=users_img_light_data, light_image=users_img_light_data)

# Settings Icon in Sidebar (the user can then change his password, his username, his name, his profile picture, etc...)
settings_img_light_data = Image.open(os.path.join(assets_folder, "settings_icon.png"))
settings_img_dark_data = Image.open(os.path.join(assets_folder, "settings_icon.png")) # TODO Changer l'image
settings_img = CTkImage(dark_image=settings_img_light_data, light_image=settings_img_light_data)

# Account Icon in Sidebar (the user can then visualize his profile, his username, his profile picture, and his average score that he got in the games)
person_img_light_data = Image.open(os.path.join(assets_folder, "account_icon.png"))
person_img_dark_data = Image.open(os.path.join(assets_folder, "account_icon.png")) # TODO Changer l'image
person_img = CTkImage(dark_image=person_img_light_data, light_image=person_img_light_data)


""" --- Frames --- """


def select_frame_by_name(frame_name):
    frames = {
        "home": (home_frame, "856x645"),
        "geo01": (game_geo01_frame, "1200x645"),
        "info02": (game_info02_frame, "1200x645"),
        "info05": (game_info05_frame, "1200x645"),
        "statistics": (statistics_frame, "856x645"),
        "users": (users_frame, "856x645"),
        "settings": (settings_frame, "856x645"),
        "account": (account_frame, "856x645")
    }

    for name, (frame, size) in frames.items():
        if name == frame_name:
            frame.configure(fg_color=("gray75", "#00002E"))
            app.geometry(size)
            frame.pack(fill="both", expand=True)
        else:
            frame.configure(fg_color="transparent")
            frame.pack_forget()



# def select_frame_by_name (frame_name):
#     home_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "home" else "transparent")
#     game_geo01_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "geo01" else "transparent")
#     game_info02_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "info02" else "transparent")
#     game_info05_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "info05" else "transparent")
#     statistics_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "statistics" else "transparent")
#     users_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "users" else "transparent")
#     settings_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "settings" else "transparent")
#     account_frame.configure(fg_color=("gray75", "#00002E") if frame_name == "account" else "transparent")
    
#     if frame_name == "home":
#         app.geometry("856x645")
#         home_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         home_frame.pack_forget()

#     if frame_name == "geo01":
#         app.geometry("1200x645")
#         game_geo01_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         game_geo01_frame.pack_forget()
        
#     if frame_name == "info02":
#         app.geometry("1200x645")
#         game_info02_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         game_info02_frame.pack_forget()
        
#     if frame_name == "info05":
#         game_info05_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         game_info05_frame.pack_forget()
        
#     if frame_name == "statistics":
#         app.geometry("856x645")
#         statistics_frame.pack(fill="both", expand=True)
#     else:
#         statistics_frame.pack_forget()
        
#     if frame_name == "users":
#         app.geometry("856x645")
#         users_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         users_frame.pack_forget()
        
#     if frame_name == "settings":
#         app.geometry("856x645")
#         settings_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         settings_frame.pack_forget()
        
#     if frame_name == "account":
#         app.geometry("856x645")
#         account_frame.pack(fill="both", expand=True)
#     else:
#         app.geometry("856x645")
#         account_frame.pack_forget()

"""  Sidebar  """

# Sidebar Frame
sidebar_frame = CTkFrame(master=app, fg_color="#400241",  width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")


# App Theme
# def switch_theme():
#     if sidebar_switch_theme_changer.get() == 1:
#         set_appearance_mode("dark") # Dark Mode
#         sidebar_switch_theme_changer.configure(progress_color="#663466", text_color="#51d743", button_color="#393939", button_hover_color="#5C5C5C")
#     else:
#         set_appearance_mode("light") # Light Mode
#         sidebar_switch_theme_changer.configure(fg_color="#663466", text_color="#fff", button_color="#393939", button_hover_color="#5C5C5C")


# Main Logo in Sidebar
sidebar_frame_label = CTkLabel(master=sidebar_frame, text="", image=braingames_img)
sidebar_frame_label.pack(pady=(38, 0), anchor="center")


# --- Sidebar Buttons --- # TODO Ajouter les command= pour les boutons

# Home (Menu) Button in Sidebar
def home_button_event():
    select_frame_by_name("home")
    
sidebar_frame_home_button = CTkButton(master=sidebar_frame, image=home_img, text="Home", fg_color="transparent", text_color=("white","white"), font=braingames_sidebar_button_font, hover_color=("#000000"), anchor="w", command=home_button_event)
sidebar_frame_home_button.pack(anchor="center", ipady=5, pady=(60, 0))

# Create the Statistics Frame
statistics_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)
# Statistics (display_results) Button in Sidebar
def statistics_button_event():
    select_frame_by_name("statistics")
    for widget in statistics_frame.winfo_children():
        widget.destroy()
    statistics_instance = Statistics(statistics_frame)
    statistics_instance.pack(expand=True, fill='both')

sidebar_frame_statistics_button = CTkButton(master=sidebar_frame, image=statistics_img, text="Statistics", fg_color="transparent", text_color=("white","white"), font=braingames_sidebar_button_font, hover_color="#000000", anchor="w", command=statistics_button_event)
sidebar_frame_statistics_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Orders (User List)
def users_button_event():
    select_frame_by_name("users")
    
sidebar_frame_users_button = CTkButton(master=sidebar_frame, image=users_img, text="Users", fg_color="transparent", text_color=("white","white"), font=braingames_sidebar_button_font, hover_color="#000000", anchor="w", command=users_button_event)
sidebar_frame_users_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Settings Button in Sidebar
def settings_button_event():
    select_frame_by_name("settings")
    
sidebar_frame_settings_button = CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent", text_color=("white","white"), font=braingames_sidebar_button_font, hover_color="#000000", anchor="w", command=settings_button_event)
sidebar_frame_settings_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Account Button in Sidebar
def account_button_event():
    select_frame_by_name("account")
    
sidebar_frame_account_button = CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color="transparent", text_color=("white","white"), font=braingames_sidebar_button_font, hover_color="#000000", anchor="w", command=account_button_event)
sidebar_frame_account_button.pack(anchor="center", ipady=5, pady=(160, 0))


# Switch Theme Button in Sidebar
# sidebar_switch_theme_changer = CTkSwitch(master=sidebar_frame, command=switch_theme, fg_color="#663466", bg_color="transparent", button_color="#393939", button_hover_color="#5C5C5C", corner_radius=10, border_width=1, border_color="black", width=50, height=25, text_color="#fff", text="Dark Mode", font=braingames_sidebar_button_font)
# sidebar_switch_theme_changer.pack(anchor="center", padx=(0,30), pady=(16, 0))

# Author Label in Sidebar at the level as the switch but the switch ins't there for now
sidebar_frame_author_label = CTkLabel(master=sidebar_frame, text="Made by Nico Mengisen", font=CTkFont(family="Sharp Grotesk Medium 20", size=12), text_color="#50d142")
sidebar_frame_author_label.pack(anchor="center",  pady=(16, 0))


"""# --- Main View (Right Side) Frames ---"""


""" Home Frame"""

home_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)
home_frame.pack_propagate(0)

home_frame_title = CTkLabel(master=home_frame, fg_color="transparent", text="Welcome to Brain Games", font=braingames_title_font, text_color="#d292ff")
home_frame_title.pack(anchor="w", padx=(63, 0), pady=(25, ))

# Container for the statistics in Home Frame
home_frame_stats_container = CTkFrame(master=home_frame, fg_color="transparent", width=464, height=70)
home_frame_stats_container.pack_propagate(0)
home_frame_stats_container.pack(anchor="center", padx=(0, 0), pady=(0, 0))

# Time Played Frame
home_frame_stats_time_played = CTkFrame(master=home_frame_stats_container, fg_color="#0000ff", width=132, height=70, corner_radius=7)
home_frame_stats_time_played.pack_propagate(0)
home_frame_stats_time_played.pack(side="left", padx=(0, 10))  # Use side="left" and add some padding if you want space between the frames

# Time Played Title
home_frame_stats_time_played_title_label = CTkLabel(master=home_frame_stats_time_played, text="Time Played", font=(braingames_regular_font, 10), text_color="#fff")
home_frame_stats_time_played_title_label.pack(anchor="nw", padx=(14, 0))

# Time Played Value
home_frame_stats_time_played_value_label = CTkLabel(master=home_frame_stats_time_played, text=(f"70 min."), justify="left",  font=(braingames_title_font, 25), text_color="#fff")
home_frame_stats_time_played_value_label.pack(anchor="nw", padx=(14, 0))


# Number of Games Played Frame
# Game Played Frame
home_frame_stats_game_played = CTkFrame(master=home_frame_stats_container, fg_color="#0000ff", width=132, height=70, corner_radius=7)
home_frame_stats_game_played.pack_propagate(0)
home_frame_stats_game_played.pack(anchor="center", side="left", padx=(0, 10), pady=(0,0))

# Game Played Title
home_frame_stats_game_played_title_label = CTkLabel(master=home_frame_stats_game_played, text="Game Played", font=(braingames_regular_font, 10), text_color="#fff")
home_frame_stats_game_played_title_label.pack(anchor="nw", padx=(14, 0))

# Game Played Value #TODO Change the value to the number of games played by the user from the display_results.py view_total() function
home_frame_stats_game_played_value_label = CTkLabel(master=home_frame_stats_game_played, text=(f"10"), justify="left",  font=(braingames_title_font, 25), text_color="#fff")
home_frame_stats_game_played_value_label.pack(anchor="nw", padx=(14, 0))


# Average Score Frame
home_frame_stats_avg_score = CTkFrame(master=home_frame_stats_container, fg_color="#0000ff", width=132, height=70, corner_radius=7)
home_frame_stats_avg_score.pack_propagate(0)
home_frame_stats_avg_score.pack(anchor="center", side="left", padx=(0, 10), pady=(0,0))

# Average Score Title
home_frame_stats_game_avg_score_title_label = CTkLabel(master=home_frame_stats_avg_score, text="Average Score", font=(braingames_regular_font, 10), text_color="#fff")
home_frame_stats_game_avg_score_title_label.pack(anchor="nw", padx=(14, 0))

#TODO Change the value to the average score of the user from the display_results.py view_total() function
home_frame_stats_game_avg_score_value_label = CTkLabel(master=home_frame_stats_avg_score, text=(f"30%"), justify="left",  font=(braingames_title_font, 25), text_color="#fff")
home_frame_stats_game_avg_score_value_label.pack(anchor="nw", padx=(14, 0))



""" Home Games Frame"""
# Home Frame Subtitle
home_frame_subtitle = CTkLabel(master=home_frame, text="Choose a game", font=braingames_subtitle_font, text_color="#d292ff")
home_frame_subtitle.pack(anchor="n", pady=(40, 0), padx=(0, 290)) 

# Game Menu in Home Frame
home_frame_games = CTkFrame(master=home_frame, fg_color="transparent")
home_frame_games.pack(pady=(5,0), padx=(0, 0), anchor="center")

# Home Frame Games Buttons
# Geo01 Game
def geo01_button_event():
    select_frame_by_name("geo01")
    for widget in game_geo01_frame.winfo_children():
        widget.destroy()
    geo_game_instance = geo01.GeoGame(game_geo01_frame)
    geo_game_instance.pack(fill="both", expand=True)
    
home_frame_game_geo01_button = CTkButton(master=home_frame_games, text="", fg_color="transparent", image=geo01_img, hover_color="#393939", corner_radius=7, command=geo01_button_event)
home_frame_game_geo01_button.grid(row=0, column=0, rowspan=2, sticky="w")

# Info02 Game
def info02_button_event():
    select_frame_by_name("info02")
    for widget in game_info02_frame.winfo_children():
        widget.destroy()
    info_game_instance = info02.Info02Game(game_info02_frame)
    info_game_instance.pack(fill="both", expand=True)
    
home_frame_game_info02_button = CTkButton(master=home_frame_games, text="", fg_color="transparent",image=info02_img, hover_color="#393939", corner_radius=7, command=info02_button_event)
home_frame_game_info02_button.grid(row=0, column=1, sticky="w", pady=(7, 0))

# Info05 Game
def info05_button_event():
    select_frame_by_name("info05")
    for widget in game_info05_frame.winfo_children():
        widget.destroy()
    # info_game_instance = info05.InfoGame(game_info05_frame)
    # info_game_instance.pack(fill="both", expand=True)
    
home_frame_game_info05_button = CTkButton(master=home_frame_games, text="", fg_color="transparent", image=info05_img, hover_color="#393939", corner_radius=7, command=info05_button_event)
home_frame_game_info05_button.grid(row=1, column=1, sticky="w", pady=(7, 0))

# View Statistics From Home Frame
home_view_statistics_button = CTkButton(master=home_frame_games, text="View Statistics", fg_color="#0000ff",font=braingames_regular_font, text_color="#fff", hover_color="#3c46ff", corner_radius=7, command=statistics_button_event)
home_view_statistics_button.grid(row=3, column=0, columnspan=2, sticky="s", pady=(20, 0), padx=(0,80))


# Create the Geo01 Frame
game_geo01_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)
game_geo01_frame.pack_propagate(0)

# Create the Info02 Frame
game_info02_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)
game_info02_frame.pack_propagate(0)

# Create the Info05 Frame
game_info05_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)
game_info05_frame.pack_propagate(0)





# Create the Users Frame

users_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)

# Create the Settings Frame

settings_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)

# Create the Account Frame

account_frame = CTkFrame(master=app, fg_color="transparent", width=680, height=650, corner_radius=0)


""" Select Home Frame by default """
select_frame_by_name("home")


""" Launch App"""
app.mainloop()