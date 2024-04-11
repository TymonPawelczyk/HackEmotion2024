import os
import random
import pandas as pd
import tkinter as tk
import tkinter.messagebox as tk_messagebox
import time as t
from PIL import Image, ImageTk

start_time = None  # Add a global variable to store the start time of the current image display


# Folder containing the images
base_folder = os.getcwd() + "/dataset/"

# Get a list of all subdirectories in the base folder
subdirs = os.listdir(base_folder)

# Init DataFrame with the user stat
path_to_csv = os.getcwd() + "/csv"
csv_file_names = os.listdir(path_to_csv)
if len(csv_file_names) == 0:
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
        {"id_user": pd.Series(dtype=int), "id_session": pd.Series(dtype=int)}
    )
    session = pd.DataFrame(
        {
            "id": pd.Series(dtype=int),
            "guess": pd.Series(dtype=int),  # id of the guess not
            "correct": pd.Series(dtype=int),  # id of correct
            "response_time": pd.Series(dtype=float),
        }
    )
    emotion = pd.DataFrame({"id": list(range(1, len(subdirs) + 1)), "label": subdirs})
else:
    user = pd.read_csv(path_to_csv + "/user.csv", sep=" ")
    user_sessions = pd.read_csv(path_to_csv + "/user_sessions.csv", sep=" ")
    session = pd.read_csv(path_to_csv + "/session.csv", sep=" ")
    emotion = pd.read_csv(path_to_csv + "/emotion.csv", sep=" ")

print(user)

def show_start_screen():
    global root, name_entry, surname_entry, gender_var, age_entry, text_entry

    # Hide the main application frame
    root.withdraw()

    # Create a new window for the start screen
    start_screen = tk.Toplevel(root)
    start_screen.title("Start Screen")
    start_screen.geometry("800x600")

    # Create a validation function for numeric input
    def is_numeric(input_string):
        if input_string.isdecimal():
            return True
        else:
            tk_messagebox.showerror("Invalid Input", "Age must be a numeric value.")
            return False

    validate_numeric = root.register(is_numeric)

    # Create entry fields for name, surname, age, and text
    name_label = tk.Label(start_screen, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(start_screen)
    name_entry.pack()

    surname_label = tk.Label(start_screen, text="Surname:")
    surname_label.pack()
    surname_entry = tk.Entry(start_screen)
    surname_entry.pack()

    gender_label = tk.Label(start_screen, text="Gender:")
    gender_label.pack()
    gender_options = ["Male", "Female", "Other"]  # List of gender options
    gender_var = tk.StringVar()
    gender_var.set(gender_options[0])  # Default value
    gender_entry = tk.OptionMenu(start_screen, gender_var, *gender_options)
    gender_entry.pack()

    age_label = tk.Label(start_screen, text="Age:")
    age_label.pack()
    age_entry = tk.Entry(
        start_screen, validate="key", validatecommand=(validate_numeric, "%P")
    )
    age_entry.pack()

    text_label = tk.Label(start_screen, text="Text:")
    text_label.pack()
    text_entry = tk.Entry(start_screen)
    text_entry.pack()

    # Create a submit button to save the user's information and show the main application
    submit_button = tk.Button(
        start_screen, text="Submit", command=lambda: on_submit(start_screen)
    )
    submit_button.pack()


def on_submit(start_screen):
    global user, user_id, session_id, start_time, user_sessions

    # Get the user's information from the entry fields
    name = name_entry.get()
    surname = surname_entry.get()
    gender = gender_var.get()
    age = age_entry.get()
    text = text_entry.get()
    if user.empty:
        user_id = 1
    else:
        # adding using last record
        user_id = user.iloc[-1:]["id"].values[-1] + 1

    # Add the user's information to the user DataFrame
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
        print(user_sessions.iloc[-1:])
        session_id = user_sessions.iloc[-1:]["id_session"].values[-1] + 1

    # add user's session to table user_sessions
    new_user_session = pd.DataFrame({"id_user": [user_id], "id_session": [session_id]})

    user_sessions = pd.concat([user_sessions, new_user_session])
    user = pd.concat([user, new_data], ignore_index=True)

    # Show the main application and destroy the start screen
    root.deiconify()
    start_screen.destroy()
    start_time = t.time()


def on_button_click(button_number):
    global user, start_time, session

    if start_time is not None:
        response_time = t.time() - start_time  # Calculate the response time
        print(
            f"Button {button_number} clicked! Response time: {response_time:.2f} seconds"
        )

    new_session_record = pd.DataFrame(
        {
            "id": [session_id],
            "guess": [button_number + 1],  # id of the guess not
            "correct": [actual_emotion],  # id of correct
            "response_time": [response_time],
        }
    )
    session = pd.concat([session, new_session_record], ignore_index=True)
    print(session)
    change_image()


def load_random_image():
    global actual_emotion
    # Randomly select a subdirectory
    selected_subdir_enum = random.choice(list(enumerate(subdirs)))
    selected_subdir = selected_subdir_enum[1]
    actual_emotion = selected_subdir_enum[0] + 1
    # Get a list of all image files in the selected subdirectory
    image_files = [
        f
        for f in os.listdir(os.path.join(base_folder, selected_subdir))
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # Randomly select an image file
    selected_image_file = random.choice(image_files)

    # Open the image and create a Tkinter-compatible photo image
    image_path = os.path.join(base_folder, selected_subdir, selected_image_file)
    pil_image = Image.open(image_path)

    # Calculate the aspect ratio of the image
    aspect_ratio = float(pil_image.height) / float(pil_image.width)

    # Resize the image to fit inside the 800x600 window while maintaining the aspect ratio
    if pil_image.width > pil_image.height:
        new_width = 800
        new_height = int(new_width * aspect_ratio)
    else:
        new_height = 600
        new_width = int(new_height / aspect_ratio)

    pil_image = pil_image.resize((new_width, new_height), Image.ADAPTIVE)

    tk_image = ImageTk.PhotoImage(pil_image)

    return tk_image, selected_subdir


def change_image():
    global image_label, current_image, start_time
    tk_image, _ = load_random_image()
    current_image = tk_image
    image_label.configure(image=current_image)
    image_label.image = current_image
    start_time = t.time()  # Record the start time when the image is displayed


# Create the main window
root = tk.Tk()
root.title("MyAcousticOrNot")
root.geometry("800x600")  # Set the window size to 800x600 pixels

# Show the start screen
show_start_screen()

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create 5 buttons
for ind, subdir in enumerate(subdirs):
    button = tk.Button(
        button_frame, text=f"{subdir}", command=lambda i=ind: on_button_click(i)
    )
    button.pack(side=tk.LEFT, padx=5)

# Load and display a random image
current_image, _ = load_random_image()
image_label = tk.Label(root, image=current_image)
image_label.pack()

# Run the tkinter event loop
root.mainloop()

# create folder with csv's if not in directory
csv_dir = os.path.join(os.getcwd(), "csv")
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

session.to_csv(csv_dir + "/session.csv", sep=" ", index=False)
user.to_csv(csv_dir + "/user.csv", sep=" ", index=False)
user_sessions.to_csv(csv_dir + "/user_sessions.csv", sep=" ", index=False)
emotion.to_csv(csv_dir + "/emotion.csv", sep=" ", index=False)
