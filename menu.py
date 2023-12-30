from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, set_appearance_mode
from PIL import Image, ImageTk
import os

# Assuming GeoGame, Info02Game, and Info05Game are correctly defined in their respective files
from geo01 import GeoGame  
from info02 import Info02Game  
# from info05 import Info05Game  

def create_menu():
    app = CTk()
    app.title("Inventory Management")
    app.geometry("1200x800")
    app.resizable(0, 0)

    set_appearance_mode("light")

    assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

    # Sidebar
    sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=176, height=800, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", side="left")

    # Logo
    braingames_img_data = Image.open(os.path.join(assets_folder, "logo.png"))
    logo_img_photo = ImageTk.PhotoImage(braingames_img_data)
    logo_label = CTkLabel(master=sidebar_frame, image=logo_img_photo, text="")
    logo_label.image = logo_img_photo  # Keep a reference so it's not garbage collected
    logo_label.pack(pady=20)

    # Function to create sidebar buttons
    def create_sidebar_button(image_path, text, command):
        img_data = Image.open(os.path.join(assets_folder, image_path))
        img_photo = ImageTk.PhotoImage(img_data)
        button = CTkButton(
            master=sidebar_frame,
            image=img_photo,
            text=text,
            fg_color="transparent",
            hover_color="#207244",
            text_color="white",
            compound="left",
            font=("Arial", 14),
            width=160,
            height=32,
            corner_radius=8,
            command=command
        )
        button.image = img_photo  # Keep a reference so it's not garbage collected
        button.pack(pady=10)
        return button

    # Main content area
    main_frame = CTkFrame(master=app, fg_color="#fff", width=680, height=800, corner_radius=0)
    main_frame.pack_propagate(0)
    main_frame.pack(side="left", fill="both", expand=True)

    # Game Frames
    geo_game_frame = GeoGame(main_frame)
    info02_game_frame = Info02Game(main_frame)
    # info05_game_frame = Info05Game(main_frame)

    # Dashboard Frame is the displayResult.py file
    dashboard_frame = CTkFrame(main_frame, fg_color="#fff", corner_radius=0)
    dashboard_frame.pack(fill="both", expand=True)
    
    
    # Function to raise frames to the top
    def show_frame(frame):
        frame.tkraise()

    # Dashboard Button
    dashboard_button = create_sidebar_button("analytics_icon.png", "Dashboard", lambda: show_frame(dashboard_frame))

    # Games Button (will raise a frame with game options)
    games_button = create_sidebar_button("games_icon.png", "Games", lambda: show_frame(games_frame))

    # Other buttons can be created in a similar manner
    # ...

    # Frame that will contain game options
    games_frame = CTkFrame(main_frame, fg_color="#fff", corner_radius=0)
    games_frame.pack(fill="both", expand=True)

    # Function to create game option buttons inside the games frame
    def create_game_button(img_filename, game_frame):
        game_img = Image.open(os.path.join(img_folder, img_filename))
        game_photo = ImageTk.PhotoImage(game_img)
        game_button = CTkButton(
            master=games_frame,
            image=game_photo,
            text="",
            fg_color="transparent",
            hover_color="#207244",
            width=150,
            height=150,
            corner_radius=10,
            command=lambda: show_frame(game_frame)
        )
        game_button.image = game_photo  # Keep a reference
        game_button.pack(pady=20)
        return game_button

    # Create buttons for each game
    geo_game_button = create_game_button("geo01.gif", geo_game_frame)
    info02_game_button = create_game_button("info02.gif", info02_game_frame)
    #info05_game_button = create_game_button("info05.gif", info05_game_frame)

    # Initially, show the games frame
    show_frame(games_frame)

    app.mainloop()

if __name__ == "__main__":
    create_menu()