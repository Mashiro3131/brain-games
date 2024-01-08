"""Login / Register pour tous 

Dans la base de données, on ajoute une table avec le pseudo des utilisateurs, leur niveau de droit (1=eleve, 2=prof) et leur mot de passe (on va stocker un hash et pas l’ensemble). Préparer les écrans et fonctions permettant : 

de s’enregistrer (register), tout le monde peut s’enregistrer au niveau élève. 

de se loguer (login), et déloguer (logout). 

d’attribuer le niveau 2 (prof) à un utilisateur (seul un prof pourra le faire). 

Modifier le programme pour que le CRUD sur les résultats ne soit possible que pour les enseignants. 

Modifier le programme pour qu’une fois loggé, un utilisateur n’ait pas besoin de taper son pseudo et qu’il ne puisse voir que ses résultats (et pas ceux des autres).

"""

import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkFont, CTk, CTkButton, CTkImage
from CTkMessagebox import CTkMessagebox
from new_database import Database
from PIL import Image, ImageTk
import os



class Login(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("LogIn")
        self.parent.geometry("600x480")
        self.parent.resizable(False, False)

        # Fonts
        # self.login_title_font = CTkFont(family="Test Söhne Kräftig", size=40, weight="bold")
        # self.login_impact_font = CTkFont(family="Test Söhne", size=14)

        # Directories for images and assets
        img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
        assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

        # Load images
        #self.side_img_data = Image.open(os.path.join(img_folder, "login_background_cropped.jpg"))
        self.braingames_logo_data = Image.open(os.path.join(assets_folder, "BrainGames.png"))
        self.account_icon_data = Image.open(os.path.join(assets_folder, "account_icon.png"))
        self.password_icon_data = Image.open(os.path.join(assets_folder, "password-icon.png"))
        # self.google_icon_data = Image.open(os.path.join(assets_folder, "google-icon.png"))

        # Initialize login_frame as an instance attribute
        self.left_side_frame = CTkFrame(self, width=300, height=480, fg_color="#00002E")
        self.left_side_frame.pack_propagate(0)
        
        self.login_frame = CTkFrame(self, width=300, height=480, fg_color="#000")
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(expand=True, side="right")

        # Create UI components
        #self.create_side_image()
        self.create_left_side_frame()
        self.create_login_frame()

    # def create_side_image(self):
    #     side_img = CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(300, 480))
    #     side_img_label = CTkLabel(self, text="", image=side_img)
    #     side_img_label.pack(expand=True, side="left")

    # left side frame with the brain games logo and a #0000ff witht the logo on top in the center
    def create_left_side_frame(self):
        self.left_side_frame.pack_propagate(0)
        self.left_side_frame.pack(expand=True, side="left")

        # Brain Games logo
        brain_games_logo = CTkImage(dark_image=self.braingames_logo_data, light_image=self.braingames_logo_data, size=(100, 100))
        CTkLabel(self.left_side_frame, text="", image=brain_games_logo).pack(expand=True, side="top")




# The user will land on this first page
    def create_login_page(self):
        self.login_page.pack_propagate(0)
        self.login_page.pack(expand=True, side="right")

        # Getting Started title
        getting_started_title_label = CTkLabel(self.login_page, text="Getting Started", text_color="#d292ff", anchor="w", justify="left", font=(self.login_title_font, 24))


    def create_login_frame(self):
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(expand=True, side="right")


        # Login title
        login_title_label = CTkLabel(self.login_frame, text="Welcome back !", text_color="#d292ff", anchor="w", justify="left", font=CTkFont(family="Test Söhne Kräftig", size=24, weight="bold"))
        login_title_label.pack(anchor="w", pady=(40, 0), padx=(25, 0))
        
        # Username label and entry
        account_icon = CTkImage(dark_image=self.account_icon_data, light_image=self.account_icon_data, size=(20,20))
        CTkLabel(self.login_frame, text="  Username:", text_color="#d292ff", anchor="w", justify="left", font=CTkFont(family="Test Söhne", size=14), image=account_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#d292ff", border_width=1, text_color="#000000").pack(anchor="w", padx=(25, 0))

        """Password"""
        # Image
        password_icon = CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(17,17))
        
        # Password label
        self.password_label = CTkLabel(self.login_frame, text="  Password:", text_color="#d292ff", anchor="w", justify="left", font=CTkFont(family="Test Söhne", size=14), image=password_icon, compound="left")
        self.password_label.pack(anchor="w", pady=(21, 0), padx=(25, 0))
        
        # Password entry
        self.password_entry = CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#d292ff", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))
       
       
        # Login button
        self.login_as_user_button = CTkButton(self.login_frame, text="Login", fg_color="#3c46ff", hover_color="#0000ff", font=CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=225, command=self.login_as_user)
        self.login_as_user_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))
        
        # Register and Guest buttons frame
        self.button_frame = CTkFrame(self.login_frame, fg_color="transparent")
        self.button_frame.pack(anchor="w", pady=(20, 0), padx=(25, 0))
        
        # Register button
        self.register_new_user_button = CTkButton(self.button_frame, text="Register", fg_color="#3c46ff", hover_color="#0000ff", font=CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=110, command=self.register_frame)
        self.register_new_user_button.pack(side="left", padx=(0, 5))
        
        # Continue as guest button
        self.guest_login_button = CTkButton(self.button_frame, text="Guest", fg_color="#3c46ff", hover_color="#0000ff", font=CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=110, command=self.login_as_guest)
        self.guest_login_button.pack(side="right", padx=(0, 0))
        
        # Quit button
        # quit_app_button = CTkButton(self.login_frame, text="Quit", fg_color="#3c46ff", hover_color="#0000ff", font=CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=225, command=self.exit_application_messagebox)
        # quit_app_button.pack(anchor="w", pady=(20, 0), padx=(25, 0))

        # # Google login button
        # google_icon = CTkImage(dark_image=self.google_icon_data, light_image=self.google_icon_data, size=(17,17))
        # login_with_google_button = CTkButton(self.login_frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#E44982", font=self.login_impact_font, text_color="#d292ff", width=225, image=google_icon)
        # login_with_google_button.pack(anchor="w", pady=(20, 0), padx=(25, 0))

        
            
    def register_frame(self):
        self.register_frame = CTkFrame(self, bg_color="#00002E")
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Register title
        self.register_title_label = CTkLabel(self.register_frame, text="Register", font=self.login_title_font, bg_color="white")
        self.register_title_label.pack()
        
        # Register entry
        self.register_entry = CTkEntry(self.register_frame, width=30, font=self.login_impact_font)
        self.register_entry.pack()
        
        # Password entry
        self.password_entry = CTkEntry(self.register_frame, width=30, font=self.login_impact_font)
        self.password_entry.pack()
        
        # Eye icon to show password
        self.eye_icon = CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(17,17))
        self.eye_icon_label = CTkLabel(self.register_frame, image=self.eye_icon)
        
        
        
        
        # Register button
        self.register_button = CTkButton(self.register_frame, text="Sign Up", font=self.login_impact_font, bg_color="transparent", command=Database.register_user)
        self.register_button.pack()
        

            
    # def exit_application_messagebox(self):
    #     question_message_box = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
    #                                          icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        
    #     response = question_message_box.get()

    #     if response == "Yes":
    #         self.destroy()
    #     else:
    #         print("Click 'Yes' to exit!")

    #     CTkButton(self, text="Ask Question", command=question_message_box).pack(padx=20, pady=(10, 20), fill="both")


    # here we will add the query from the database to check if the user is in the database and then log him in
    def login_as_user(self): # continue button #10a37f and title color #2d333a
        pass
    
    def login_as_teacher(self):
        pass
    
    def login_as_admin(self):
        pass
    
    def register_new_user(self):    
        pass

    def login_as_guest(self):
        pass
        
        

    def show_password(self):
        self.password_entry.config(show="")
        self.eye_icon_label.pack()
    
    def hide_password(self):
        self.password_entry.config(show="*")
        self.eye_icon_label.pack_forget()
    
    
    def show_or_hide_password(self):
        if self.eye_icon_label.winfo_ismapped():
            self.hide_password()
        else:
            self.show_password()










# class Login(CTkFrame):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.parent = parent
#         self.parent.title("LogIn")
#         self.assets_folder = os.path.join(os.path.dirname(__file__), "assets")
#         self.img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
#         self.assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
#         self.parent.geometry("600x480")
#         self.login_title_font = CTkFont(family="Test Söhne Kräftifg", size=40)
        
#         # Fonts
#         self.login_impact_font = CTkFont(family="Test Söhne", size=14)
#         self.login_impact_font = CTkFont(family="Test Söhne", size=14)
#         self.theme = "dark"
        
        
#         self.login_frame()
        
#     def login_frame(self): # If you want to change the icon for light mode, change it downbelow
        
#         self.login_entry_frame = CTkFrame(self, fg_color="#00002E")
        
#         img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
#         assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        
#         # Image data
#         self.login_background_side_img_data = Image.open(os.path.join(img_folder, "login_background.jpg"))
#         self.login_password_icon_data = Image.open(os.path.join(assets_folder, "password_icon.png"))
        
#         self.login_backgournd_side_img = CTkImage(dark_image=self.login_background_side_img_data, 
#                                                 light_image=self.login_background_side_img_data, 
#                                                 size=(300, 480))
#         self.login_password_icon = CTkImage(dark_image=self.login_password_icon_data, 
#                                             light_image=self.login_password_icon_data, 
#                                             size=(20, 20))
        
#         self.login_backgournd_side_img_label = CTkLabel(self.login_entry_frame, image=self.login_backgournd_side_img)
#         self.login_backgournd_side_img_label.pack(expand=True, side="left")

                                     
        

        
        
#     def continue_as_guest(self):
#         self.continue_as_guest_button = CTkButton(self.login_entry_frame, text="Continue as guest", font=self.login_impact_font, bg_color="transparent", command=self.login_frame)
#         self.continue_as_guest_button.pack()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #     # Login title
    #     self.login_title_label = CTkLabel(self.login_entry_frame, text="Login", font=self.login_title_font, bg_color="white")
    #     self.login_title_label.pack()
        
    #     # Login entry
    #     self.login_entry = CTkEntry(self.login_entry_frame, width=30, font=self.login_impact_font)
    #     self.login_entry.pack()
        
    #     # Password entry
    #     self.password_entry = CTkEntry(self.login_entry_frame, width=30, font=self.login_impact_font)
    #     self.password_entry.pack()
        
    #     # Login button
    #     self.login_button = CTkButton(self.login_entry_frame, text="Login", font=self.login_impact_font, bg_color="transparent", command=Database.login_user)
    #     self.login_button.pack()
        
    #     # Register button
    #     self.register_button = CTkButton(self.login_entry_frame, text="Register", font=self.login_impact_font, bg_color="transparent", command=self.register_frame)
    #     self.register_button.pack()
        
    # def register_frame(self):
        
    #     self.register_frame = CTkFrame(self, bg_color="#00002E")
    #     self.register_frame.place(relx=0.5, rely=0.5, anchor="center")
        
    #     # Register title
    #     self.register_title_label = CTkLabel(self.register_frame, text="Register", font=self.login_title_font, bg_color="white")
    #     self.register_title_label.pack()
        
    #     # Register entry
    #     self.register_entry = CTkEntry(self.register_frame, width=30, font=self.login_impact_font)
    #     self.register_entry.pack()
        
    #     # Password entry
    #     self.password_entry = CTkEntry(self.register_frame, width=30, font=self.login_impact_font)
    #     self.password_entry.pack()
        
    #     # Register button
    #     self.register_button = CTkButton(self.register_frame, text="Register", font=self.login_impact_font, bg_color="transparent", command=Database.register_user)
    #     self.register_button.pack()
    
    
    # #La frame register devra ecraser la frame login et si le user veut revenir en arriere, il pourra le faire avec un bouton back qui rechargera la frame login
    # def login_register_pagination_between_frame_button(self):
        
    #     self.back_button = CTkButton(self.register_frame, text="Back", font=self.login_impact_font, bg_color="transparent", command=self.login_frame)
    #     self.back_button.pack()
        
    # def quit_application(self):
    #     confirm = CTkMessagebox.askyesno("Confirmation", "Are you sure you want to quit?")
    #     if confirm:
    #         self.quit()
        
        
    
    

    
    
    
    
    
    
    
# test the current app

if __name__ == "__main__":
    root = CTk()
    app = Login(root)
    app.pack()
    root.mainloop()