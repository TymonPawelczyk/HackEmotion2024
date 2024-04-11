import customtkinter as ctk
from customtkinter import E, LEFT, N, S
import os
import random
import pandas as pd
import tkinter as tk
import tkinter.messagebox as tk_messagebox
import time as t
from PIL import Image, ImageTk

start_time = None
base_folder = os.getcwd() + "/HackEmotion2024/dataset"
subdirs = os.listdir(base_folder)
user = pd.DataFrame(
    {
        "id": pd.Series(dtype=int),
        "Name": [],
        "Surname": [],
        "Gender": [],
        "Age": [],
        "Text": [],
    }
)
user_sessions = pd.DataFrame(
    {"id_user": pd.Series(dtype=int),
      "id_session": pd.Series(dtype=int)}
)
session = pd.DataFrame(
    {
        "id_session": pd.Series(dtype=int),
        "guess": pd.Series(dtype=int),
        "correct": pd.Series(dtype=int),
        "response_time": pd.Series(dtype=float),
    }
)
emotion = pd.DataFrame({"id": list(range(1, len(subdirs) + 1)), "label": subdirs})


def show_start_screen():
    global root, name_entry, surname_entry, gender_var, age_entry, text_entry
    root.withdraw()
    start_screen = ctk.CTkToplevel(root)
    start_screen.title("Start Screen")
    start_screen.geometry("800x600")

    def is_numeric(input_string):
        if input_string.isdecimal():
            return True
        else:
            tk_messagebox.showerror("Invalid Input", "Age must be a numeric value.")
            return False

    validate_numeric = root.register(is_numeric)
    name_label = ctk.CTkLabel(start_screen, text="Name:")
    name_label.pack()
    name_entry = ctk.CTkEntry(start_screen)
    name_entry.pack()
    surname_label = ctk.CTkLabel(start_screen, text="Surname:")
    surname_label.pack()
    surname_entry = ctk.CTkEntry(start_screen)
    surname_entry.pack()
    gender_label = ctk.CTkLabel(start_screen, text="Gender:")
    gender_label.pack()
    gender_options = ["Male", "Female", "Other"]
    gender_var = tk.StringVar()
    gender_var.set(gender_options[0])
    gender_entry = tk.OptionMenu(start_screen, gender_var, *gender_options)
    gender_entry.pack()
    age_label = ctk.CTkLabel(start_screen, text="Age:")
    age_label.pack()
    age_entry = tk.Entry(
        start_screen, validate="key", validatecommand=(validate_numeric, "%P")
    )
    age_entry.pack()
    text_label = ctk.CTkLabel(start_screen, text="Text:")
    text_label.pack()
    text_entry = ctk.CTkEntry(start_screen)
    text_entry.pack()
    submit_button = tk.Button(
        start_screen, text="Submit", command=lambda: on_submit(start_screen)
    )
    submit_button.pack()


def on_submit(start_screen):
    global user, user_id, session_id, start_time, user_sessions
    name = name_entry.get()
    surname = surname_entry.get()
    gender = gender_var.get()
    age = age_entry.get()
    text = text_entry.get()
    if user.empty:
        user_id = 1
    else:
        user_id = user.iloc[-1:]["id"].values[-1] + 1
    new_data = pd.DataFrame(
        {
            "id": [user_id],
            "Name": [name.title()],
            "Surname": [surname.title()],
            "Gender": [gender],
            "Age": [age],
            "Text": [text],
        }
    )
    if user_sessions.empty:
        session_id = 1
    else:
        session_id = user_sessions.iloc[-1:]["id"].values[-1] + 1
    new_user_session = pd.DataFrame({"id_user": [user_id], "id_session": [session_id]})
    user_sessions = pd.concat([user_sessions, new_user_session])
    user = pd.concat([user, new_data], ignore_index=True)
    root.deiconify()
    start_screen.destroy()
    start_time = t.time()
    print(user)


def on_button_click(button_number):
    global user, start_time, session
    if start_time is not None:
        response_time = t.time() - start_time
        print(
            f"Button {button_number} clicked! Response time: {response_time:.2f} seconds"
        )
    new_session_record = pd.DataFrame(
        {
            "id_session": [session_id],
            "guess": [button_number + 1],
            "correct": [actual_emotion],
            "response_time": [response_time],
        }
    )
    session = pd.concat([session, new_session_record], ignore_index=True)
    print(session)
    change_image()


def load_random_image():
    global actual_emotion

    selected_subdir_enum = random.choice(list(enumerate(subdirs)))
    selected_subdir = selected_subdir_enum[1]
    actual_emotion = selected_subdir_enum[0] + 1

    image_files = [
        f
        for f in os.listdir(os.path.join(base_folder, selected_subdir))
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    selected_image_file = random.choice(image_files)
    image_path = os.path.join(base_folder, selected_subdir, selected_image_file)
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


def change_image():
    global image_label, current_image, start_time
    (tk_image, _) = load_random_image()
    current_image = tk_image
    image_label.configure(image=tk_image)  # Update the CTkLabel with the CTkImage
    image_label.image = tk_image
    start_time = t.time()


root = ctk.CTk()
root.title("MyAcousticOrNot")
root.geometry("800x600")
show_start_screen()
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)
for (ind, subdir) in enumerate(subdirs):
    button = tk.Button(
        button_frame, text=f"{subdir}", command=lambda i=ind: on_button_click(i)
    )
    button.pack(side=tk.LEFT, padx=5)
(current_image, _) = load_random_image()
image_label = ctk.CTkLabel(root, image=current_image, text=None)
image_label.pack()
root.mainloop()
