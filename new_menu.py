import os
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import displayResult


script_directory = os.path.dirname(os.path.abspath(__file__))

assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


os.chdir(script_directory)

app = CTk()
app.title("Brain Games")
app.iconbitmap(os.path.join(assets_folder,"braingames.ico"))
app.geometry("856x645")
app.resizable(0,0)

set_appearance_mode("light")



# TODO Créer les images dans adobe illustrator et ajouter les images den light et dark si possible ainsi que le texte en blanc et noir
# TODO Couleurs : Violet --> #700070, Vert --> #2A8C55, Gris --> #E5E5E5, Blanc --> #FFFFFF, Noir --> #000000

""" Images """

# Main Brain Games Logo in Sidebar
braingames_img_data = Image.open(os.path.join(assets_folder, "braingames_logo.png"))
braingames_img = CTkImage(dark_image=braingames_img_data, light_image=braingames_img_data, size=(87.68, 83,78))

# Home (Menu) Icon in Sidebar
home_img_light_data = Image.open(os.path.join(assets_folder, "home_light.png"))
home_img_dark_data = Image.open(os.path.join(assets_folder, "home_dark.png"))
home_img = CTkImage(dark_image=home_img_dark_data, light_image=home_img_light_data)

# Statistics (displayResult) Icon in Sidebar
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


""" Frames """

# --- Sidebar ---

# Sidebar Frame
sidebar_frame = CTkFrame(master=app, fg_color="#700070",  width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

# Main Logo in Sidebar
sidebar_frame_label = CTkLabel(master=sidebar_frame, text="", image=braingames_img)
sidebar_frame_label.pack(pady=(38, 0), anchor="center")


# --- Sidebar Buttons --- # TODO Ajouter les command= pour les boutons

# Home (Menu) Button in Sidebar
frame_home_button = CTkButton(master=sidebar_frame, image=home_img, text="Home", fg_color="transparent", text_color=("white","white"), font=("Arial Bold", 14), hover_color=("#000000", "gray70"), anchor="w")#, command=home_button_event)
frame_home_button.pack(anchor="center", ipady=5, pady=(60, 0))


# Statistics (displayResult) Button in Sidebar
frame_statistics_button = CTkButton(master=sidebar_frame, image=statistics_img, text="Statistics", fg_color="transparent", text_color=("white","white"), font=("Arial Bold", 14), hover_color="#000000", anchor="w")#, command=statistics_button_event)
frame_statistics_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Orders (User List)
frame_users_button = CTkButton(master=sidebar_frame, image=users_img, text="Users", fg_color="transparent", text_color=("white","white"), font=("Arial Bold", 14), hover_color="#000000", anchor="w")#, command=users_button_event)
frame_users_button.pack(anchor="center", ipady=5, pady=(16, 0))


# Settings Button in Sidebar


























# Statistics Button in Sidebar
# statistics_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=650, corner_radius=0)
# statistics_frame.pack_propagate(0)
# statistics_frame.pack(side="left")

# Orders Frame
orders_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=650, corner_radius=0)
orders_frame.pack_propagate(0)
orders_frame.pack(side="left")

# Returns Frame

account_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=650, corner_radius=0)
account_frame.pack_propagate(0)
account_frame.pack(side="left")

settings_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=650, corner_radius=0)
settings_frame.pack_propagate(0)
settings_frame.pack(side="left")



""" Switching Frames from Sidebar """

def switch_frame(frame_name):
    # Hide all frames
    frame_statistics_button.configure(fg_color="#fff") if frame_name == "statistics" else "transparent"
    orders_frame.configure(fg_color="#fff") if frame_name == "orders" else "transparent"
    
    # Show the selected frame
    if frame_name == 'statistics':
        displayResult.display_results(frame_statistics_button)
        frame_statistics_button.pack(fill='both', expand=True)
    else:
        frame_statistics_button.pack_forget()
        
    if frame_name == "orders":
        orders_frame.pack(fill='both', expand=True)
    elif frame_name == 'orders':
        orders_frame.pack(fill='both', expand=True)
    # ... add other conditions for other frames


# Bind the buttons to the switch_frame function to use them as commands
def statistics_button_event():
    switch_frame('statistics')
    
def orders_button_event():
    switch_frame('orders')

def returns_button_event():
    switch_frame('returns')






""" Sidebar Buttons """

# # Main Logo in Sidebar
# braingames_img_data = Image.open(os.path.join(assets_folder, "braingames_logo.png"))
# braingames_img = CTkImage(dark_image=braingames_img_data, light_image=braingames_img_data, size=(77.68, 73,78))
# CTkLabel(master=sidebar_frame, text="", image=braingames_img).pack(pady=(38, 0), anchor="center")


# Statistics Button in Sidebar
statistics_img_data = Image.open(os.path.join(assets_folder, "analytics_icon.png"))
statistics_img = CTkImage(dark_image=statistics_img_data, light_image=statistics_img_data)
frame_statistics_button = CTkButton(master=sidebar_frame, image=statistics_img, text="Statistics", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w", command=statistics_button_event).pack(anchor="center", ipady=5, pady=(60, 0))


# Package Button in Sidebar
package_img_data = Image.open(os.path.join(assets_folder, "package_icon.png"))
package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
CTkButton(master=sidebar_frame, image=package_img, text="Orders", fg_color="transparent", font=("Arial Bold", 14), text_color="#eee", hover_color="#000000", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))


# List Button in Sidebar
list_img_data = Image.open(os.path.join(assets_folder, "user_list_icon.png"))
list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
CTkButton(master=sidebar_frame, image=list_img, text="Orders", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))


# Returns Button in Sidebar
returns_img_data = Image.open(os.path.join(assets_folder, "returns_icon.png"))
returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
CTkButton(master=sidebar_frame, image=returns_img, text="Returns", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))


# Settings Button in Sidebar
settings_img_data = Image.open(os.path.join(assets_folder, "settings_icon.png"))
settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))


# Account Button in Sidebar
person_img_data = Image.open(os.path.join(assets_folder, "person_icon.png"))
person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w").pack(anchor="center", ipady=5, pady=(160, 0))








# Function to load the statistics page
def load_statistics():
    for widget in main_view.winfo_children():
        widget.destroy()
    displayResult.display_results(main_view)  # Load content from displayResult.py

# statistics Button in Sidebar
statistics_button = CTkButton(master=sidebar_frame, image=statistics_img, text="Statistics", fg_color="transparent", font=("Arial Bold", 14), hover_color="#000000", anchor="w")
statistics_button.pack(anchor="center", ipady=5, pady=(60, 0))
statistics_button.bind("<Button-1>", lambda e: load_statistics())


# Main View (Right Side)
main_view = CTkFrame(master=app, fg_color="#fff", width=680, height=650, corner_radius=0)
main_view.pack_propagate(0)
main_view.pack(side="left")

title_frame = CTkFrame(master=main_view, fg_color="transparent")
title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

CTkLabel(master=title_frame, text="Orders", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

CTkButton(master=title_frame, text="+ New Order",  font=("Arial Black", 15), text_color="#fff", fg_color="#2A8C55", hover_color="#207244").pack(anchor="ne", side="right")

# Metrics Frame
metrics_frame = CTkFrame(master=main_view, fg_color="transparent")
metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

# Orders Metric
orders_metric = CTkFrame(master=metrics_frame, fg_color="#53D74D", width=200, height=60)
orders_metric.grid_propagate(0)
orders_metric.pack(side="left")

logitics_img_data = Image.open(os.path.join("assets", "logistics_icon.png"))
logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
CTkLabel(master=orders_metric, text="Orders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=orders_metric, text="123", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

# Shipped Metric
shipped_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
shipped_metric.grid_propagate(0)
shipped_metric.pack(side="left",expand=True, anchor="center")

shipping_img_data = Image.open(os.path.join("assets","shipping_icon.png"))
shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))

CTkLabel(master=shipped_metric, image=shipping_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
CTkLabel(master=shipped_metric, text="Shipping", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=shipped_metric, text="91", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

# Delivered Metric
delivered_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
delivered_metric.grid_propagate(0)
delivered_metric.pack(side="right",)

delivered_img_data = Image.open(os.path.join("assets", "delivered_icon.png"))
delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))

CTkLabel(master=delivered_metric, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
CTkLabel(master=delivered_metric, text="Delivered", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=delivered_metric, text="23", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


app.mainloop()