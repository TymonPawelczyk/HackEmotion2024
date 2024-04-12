import customtkinter as ctk
import os
import random
import pandas as pd
import tkinter as tk
import tkinter.messagebox as tk_messagebox
import time as t
from PIL import Image



class GameApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.options = ["10", "20"]
        

        self.start_time = None
        self.base_folder = os.getcwd() + "/dataset"
        self.subdirs = os.listdir(self.base_folder)
        self.path_to_csv = os.getcwd() + "/csv"
        self.csv_file_names = os.listdir(self.path_to_csv)
        if len(self.csv_file_names) == 0:
            self.user = pd.DataFrame(
                {
                    "id": pd.Series(dtype=int),
                    "Name": [],
                    "Surname": [],
                    "Gender": [],
                    "Age": [],
                    "Text": [],
                }
            )
            self.user_sessions = pd.DataFrame(
                {"id_user": pd.Series(dtype=int),
                "id_session": pd.Series(dtype=int)}
            )
            self.session = pd.DataFrame(
                {
                    "id": pd.Series(dtype=int),
                    "guess": pd.Series(dtype=int),
                    "correct": pd.Series(dtype=int),
                    "response_time": pd.Series(dtype=float)
                }
            )
            self.emotion = pd.DataFrame({"id": list(range(1, len(self.subdirs) + 1)), "label": self.subdirs})
        else:
            self.user = pd.read_csv(self.path_to_csv + "/user.csv", sep=" ")
            self.user_sessions = pd.read_csv(self.path_to_csv + "/user_sessions.csv", sep=" ")
            self.session = pd.read_csv(self.path_to_csv + "/session.csv", sep=" ")
            self.emotion = pd.read_csv(self.path_to_csv + "/emotion.csv", sep=" ")

    def make_option_menu(self):
        self.root.withdraw()
        self.main_menu = ctk.CTkToplevel(self.root)
        self.main_menu.geometry("400x200")
        self.main_menu.title("Menu Start")
        label = ctk.CTkLabel(self.main_menu, text="Choose game length:")
        label.pack(pady=(20, 0))

        selected_option = ctk.StringVar()
        selected_option.set("")

        self.option_menu = ctk.CTkOptionMenu(self.main_menu, values=self.options, corner_radius=5, variable=selected_option)
        self.option_menu.pack(pady=(0, 20))

        confirm_button = ctk.CTkButton(self.main_menu, text="Confirm", command=self.confirm_selection)
        confirm_button.pack(pady=(0, 20))
        # self.root.deiconify()
        self.main_menu.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def confirm_selection(self):
        selected_option = self.option_menu.get()
        print(f'Buttno confirm clicked. You choose: {selected_option}')
        if selected_option == '10':
            self.game_length = 10
            self.main_menu.withdraw()
            self.show_start_screen()
            print('gamemode1')
        elif selected_option == '20':
            self.game_length = 20
            self.main_menu.withdraw()
            self.show_start_screen()
            print('gamemode2')

    def show_start_screen(self):
        self.root.withdraw()
        self.start_screen = ctk.CTkToplevel(self.root)
        self.start_screen.title("Start Screen")
        self.start_screen.geometry("800x600")

        def is_numeric(input_string):
            if input_string.isdecimal():
                return True
            else:
                tk_messagebox.showerror("Invalid Input", "Age must be a numeric value.")
                return False

        validate_numeric = self.root.register(is_numeric)
        name_label = ctk.CTkLabel(self.start_screen, text="Name:")
        name_label.pack()
        self.name_entry = ctk.CTkEntry(self.start_screen)
        self.name_entry.pack()
        surname_label = ctk.CTkLabel(self.start_screen, text="Surname:")
        surname_label.pack()
        self.surname_entry = ctk.CTkEntry(self.start_screen)
        self.surname_entry.pack()
        gender_label = ctk.CTkLabel(self.start_screen, text="Gender:")
        gender_label.pack()
        gender_options = ["Male", "Female", "Other"]
        self.gender_var = tk.StringVar()
        self.gender_var.set(gender_options[0])
        gender_entry = tk.OptionMenu(self.start_screen,  self.gender_var, *gender_options)
        gender_entry.pack()
        age_label = ctk.CTkLabel(self.start_screen, text="Age:")
        age_label.pack()
        self.age_entry = tk.Entry(
            self.start_screen, validate="key", validatecommand=(validate_numeric, "%P")
        )
        self.age_entry.pack()
        text_label = ctk.CTkLabel(self.start_screen, text="Text:")
        text_label.pack()
        self.text_entry = ctk.CTkEntry(self.start_screen)
        self.text_entry.pack()
        submit_button = tk.Button(
            self.start_screen, text="Submit", command=lambda: self.on_submit(self.start_screen)
        )
        submit_button.pack()
        self.start_screen.protocol("WM_DELETE_WINDOW", self.root.destroy)


    def on_submit(self, start_screen):
        # global user, user_id, session_id, self.start_time, user_sessions
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        gender =  self.gender_var.get()
        age =  self.age_entry.get()
        text =  self.text_entry.get()
        if  self.user.empty:
            self.user_id = 1
        else:
            self.user_id = self.user.iloc[-1:]["id"].values[-1] + 1
        new_data = pd.DataFrame(
            {
                "id": [self.user_id],
                "Name": [name.title()],
                "Surname": [surname.title()],
                "Gender": [gender],
                "Age": [age],
                "Text": [text],
            }
        )
        if self.user_sessions.empty:
            self.session_id = 1
        else:
            print(self.user_sessions.iloc[-1:])
            self.session_id = self.user_sessions.iloc[-1:]["id_session"].values[-1] + 1
        new_user_session = pd.DataFrame({"id_user": [self.user_id], "id_session": [self.session_id]})
        self.user_sessions = pd.concat([self.user_sessions, new_user_session])
        self.user = pd.concat([self.user, new_data], ignore_index=True)
        self.gameplay_screen()
        start_screen.withdraw()
        self.start_time = t.time()
        print(self.user)


    def on_button_click(self, button_number):
        self.current_idx += 1
        print(self.current_idx)
        if(self.current_idx > self.game_length):
            self.gameplay_screen.destroy()
            self.root.destroy()
            return
        if self.start_time is not None:
            response_time = t.time() - self.start_time
            print(
                f"Button {button_number} clicked! Response time: {response_time:.2f} seconds"
            )
        new_session_record = pd.DataFrame(
            {
                "id": [self.session_id],
                "guess": [button_number + 1],
                "correct": [self.actual_emotion],
                "response_time": [response_time]
            }
        )
        self.session = pd.concat([self.session, new_session_record], ignore_index=True)
        print(self.session)
        self.change_image()


    def load_random_image(self):

        selected_subdir_enum = random.choice(list(enumerate(self.subdirs)))
        selected_subdir = selected_subdir_enum[1]
        self.actual_emotion = selected_subdir_enum[0] + 1

        image_files = [
            f
            for f in os.listdir(os.path.join(self.base_folder, selected_subdir))
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        selected_image_file = random.choice(image_files)
        image_path = os.path.join(self.base_folder, selected_subdir, selected_image_file)
        pil_image = Image.open(image_path)
        aspect_ratio = float(pil_image.height) / float(pil_image.width)
        if pil_image.width > pil_image.height:
            new_width = 800
            new_height = int(new_width * aspect_ratio)
        else:
            new_height = 600
            new_width = int(new_height / aspect_ratio)
        pil_image = pil_image.resize((new_width, new_height), Image.ADAPTIVE)
        tk_image = ctk.CTkImage(
            pil_image, size=(new_width, new_height)
        )  # Use CTkImage instead of ImageTk.PhotoImage
        return (tk_image, selected_subdir)


    def change_image(self):
        # global image_label, current_image, self.start_time
        (tk_image, _) = self.load_random_image()
        self.current_image = tk_image
        self.image_label.configure(image=tk_image)  # Update the CTkLabel with the CTkImage
        self.image_label.image = tk_image
        self.start_time = t.time()

    def gameplay_screen(self):
        self.current_idx = 1
        self.gameplay_screen=ctk.CTkToplevel(self.root)
        self.gameplay_screen.title("Gameplay Screen")
        self.gameplay_screen.geometry("1200x700")
        button_frame = ctk.CTkFrame(self.gameplay_screen)
        button_frame.pack(pady=10)
        for (ind, subdir) in enumerate(self.subdirs):
            button = tk.Button(
                button_frame, text=f"{subdir}", command=lambda i=ind: self.on_button_click(i)
            )
            button.pack(side=tk.LEFT, padx=5)
        (self.current_image, _) = self.load_random_image()
        self.image_label = ctk.CTkLabel(self.gameplay_screen, image=self.current_image, text=None)
        self.image_label.pack()    
        self.gameplay_screen.protocol("WM_DELETE_WINDOW", self.root.destroy)
    

    def save_data(self):
        # create folder with csv's if not in directory
        csv_dir = os.path.join(os.getcwd(), "csv")
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        app.session.to_csv(csv_dir + "/session.csv", sep=" ", index=False)
        app.user.to_csv(csv_dir + "/user.csv", sep=" ", index=False)
        app.user_sessions.to_csv(csv_dir + "/user_sessions.csv", sep=" ", index=False)
        app.emotion.to_csv(csv_dir + "/emotion.csv", sep=" ", index=False)

    def main(self):
        # self.show_start_screen()
        self.make_option_menu()
        self.root.mainloop()
        self.save_data()
        

app = GameApp()
app.main()