import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkFont, CTkButton, CTkImage
from PIL import Image, ImageTk
import os
from new_database import Database

class Login(CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setup_window()
        self.setup_assets()
        self.create_left_side_frame()
        self.create_login_frame()

        # self.db = Database(host='localhost', port='3306', user='root', password='root', database='brain_games_db')

    def setup_window(self):
        self.parent.title("Brain Games - Login")
        self.parent.geometry("600x480")
        self.parent.resizable(False, False)

    def setup_assets(self):
        
        assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "login")
        
        self.braingames_logo_data = Image.open(os.path.join(assets_folder, "BrainGames-logo.png"))
        self.account_icon_data = Image.open(os.path.join(assets_folder, "account-login-icon.png"))
        self.password_icon_data = Image.open(os.path.join(assets_folder, "password-icon.png"))
        self.eye_open_img = ImageTk.PhotoImage(Image.open(os.path.join(assets_folder, "eye-show-password-icon.png")))
        self.eye_closed_img = ImageTk.PhotoImage(Image.open(os.path.join(assets_folder, "eye-hide-password-icon.png")))

    def create_left_side_frame(self):
        self.left_side_frame = ctk.CTkFrame(self, width=300, height=480, fg_color="#00002E")
        self.left_side_frame.pack_propagate(0)
        self.left_side_frame.pack(expand=True, side="left")

        brain_games_logo = ctk.CTkImage(dark_image=self.braingames_logo_data, light_image=self.braingames_logo_data, size=(150, 150))
        ctk.CTkLabel(self.left_side_frame, text="", image=brain_games_logo).pack(expand=True, side="top")

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, width=300, height=480, fg_color="#000")
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(expand=True, side="right")

        # Login title
        login_title_label = ctk.CTkLabel(self.login_frame, text="Welcome back !", text_color="#d292ff", 
                                         anchor="w", justify="left", font=ctk.CTkFont(family="Test Söhne Kräftig", size=26, weight="bold"))
        login_title_label.pack(anchor="w", pady=(55, 25), padx=(25, 0))

        self.create_username_entry()
        self.create_password_entry()
        self.setup_button_frame()

    def create_username_entry(self):
        account_icon = ctk.CTkImage(dark_image=self.account_icon_data, light_image=self.account_icon_data, size=(20,20))
        self.username_label = ctk.CTkLabel(self.login_frame, text="  Username:", text_color="#FFF", anchor="w", justify="left", 
                                           font=ctk.CTkFont(family="Test Söhne", size=14), image=account_icon, compound="left")
        self.username_label.pack(anchor="w", pady=(38, 0), padx=(25, 0))
        
        self.username_entry = ctk.CTkEntry(self.login_frame, width=225, fg_color="#EEEEEE", border_color="#d292ff", 
                                           border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

    def create_password_entry(self):
        password_icon = ctk.CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data, size=(17,17))
        self.password_label = ctk.CTkLabel(self.login_frame, text="  Password:", text_color="#FFF", anchor="w", justify="left", 
                                           font=ctk.CTkFont(family="Test Söhne", size=14), image=password_icon, compound="left")
        self.password_label.pack(anchor="w", pady=(21, 0), padx=(25, 0))
        
        password_entry_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        password_entry_frame.pack(anchor="w", padx=(25, 0))

        self.password_entry = ctk.CTkEntry(password_entry_frame, width=205, fg_color="#EEEEEE", border_color="#d292ff", 
                                           border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(side="left")

        self.toggle_password_button = ctk.CTkButton(password_entry_frame, image=self.eye_closed_img, 
                                                    command=self.toggle_password, fg_color="transparent", text="")
        self.toggle_password_button.pack(side="left")
        self.toggle_password_button.configure(width=5, height=5)

        self.password_showing = False

    def toggle_password(self):
        if self.password_showing:
            self.password_entry.configure(show="*")
            self.toggle_password_button.configure(image=self.eye_closed_img, width=15, height=15)
            self.password_showing = False
        else:
            self.password_entry.configure(show="")
            self.toggle_password_button.configure(image=self.eye_open_img, width=15, height=15)
            self.password_showing = True
            
            
    def setup_button_frame(self):
        self.button_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.button_frame.pack(anchor="w", pady=(20, 0), padx=(25, 0))

        # Login button
        self.login_as_user_button = ctk.CTkButton(self.button_frame, text="Login", fg_color="#3c46ff", hover_color="#0000ff", 
                                                  font=ctk.CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=110, 
                                                  command=self.login_as_user)
        self.login_as_user_button.pack(side="left", padx=(0, 5))
        
        # Register button
        self.register_new_user_button = ctk.CTkButton(self.button_frame, text="Register", fg_color="#3c46ff", hover_color="#0000ff", 
                                                      font=ctk.CTkFont(family="Test Söhne", size=12), text_color="#ffffff", width=110, 
                                                      command=self.register_frame)
        self.register_new_user_button.pack(side="right", padx=(0, 5))
        
        # Continue as guest button
        self.guest_login_button = ctk.CTkButton(self.login_frame, text="Continue as guest", fg_color="transparent", hover_color="#000000", 
                                                font=ctk.CTkFont(family="Test Söhne", size=12), text_color="#d292ff", width=110, 
                                                command=self.login_as_guest)
        self.guest_login_button.pack(anchor="w", pady=(7,0), padx=(140, 0))
        
    
    """ Login Functions """
        
    def login_as_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if Database.login_user(username, password):  # Assuming login_user returns True on successful login
            print(f"User {username} logged in successfully")
            # Proceed with user login actions
        else:
            print("Login failed. Incorrect username or password.")

    def register_new_user(self):
        # Placeholder for the registration logic
        # You should collect user information like username, password, and possibly other details
        username = self.username_entry.get()
        password = self.password_entry.get()

        if Database.register_user(username, password, role_id=1):  # Assuming role_id=1 for regular users
            print(f"User {username} registered successfully")
            # Proceed with post-registration actions
        else:
            print("Registration failed")

    def login_as_guest(self):
        username, password = Database.continue_as_guest()  # Assuming this method returns guest credentials
        if username and password:
            print(f"Logged in as guest: {username}")
            # Proceed with guest login actions
        else:
            print("Failed to continue as guest.")

    def register_frame(self):
        # Display the registration frame
        # Here you can create a similar structure as the login frame for user registration
        # For simplicity, this is just a placeholder
        print("Displaying registration frame.")

# To run the Login frame standalone for testing
if __name__ == "__main__":
    root = ctk.CTk()
    app = Login(root)
    app.pack()
    root.mainloop()