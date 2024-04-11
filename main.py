import os
import random
import pandas as pd
import tkinter as tk
import tkinter.messagebox as tk_messagebox
from PIL import Image, ImageTk

# Folder containing the images
base_folder = os.getcwd() + "/dataset/"

# Get a list of all subdirectories in the base folder
subdirs = os.listdir(base_folder)
print(subdirs)

# Init DataFrame with the user stat
user = pd.DataFrame()


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
    global user

    # Get the user's information from the entry fields
    name = name_entry.get()
    surname = surname_entry.get()
    gender = gender_var.get()
    age = age_entry.get()
    text = text_entry.get()

    # Add the user's information to the user DataFrame
    new_data = pd.DataFrame(
        {
            "Name": [name.title()],
            "Surname": [surname.title()],
            "Gender": [gender],
            "Age": [age],
            "Text": [text],
        }
    )
    user = pd.concat([user, new_data], ignore_index=True)

    # Show the main application and destroy the start screen
    root.deiconify()
    start_screen.destroy()
    print(user)


def on_button_click(button_number):
    print(f"Button {button_number} clicked!")
    change_image()


def load_random_image():

    # Randomly select a subdirectory
    selected_subdir = random.choice(subdirs)

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
    global image_label, current_image
    tk_image, _ = load_random_image()
    current_image = tk_image
    image_label.configure(image=current_image)
    image_label.image = current_image


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
for subdir in subdirs:
    button = tk.Button(
        button_frame, text=f"{subdir}", command=lambda i=subdir: on_button_click(i)
    )
    button.pack(side=tk.LEFT, padx=5)

# Load and display a random image
current_image, _ = load_random_image()
image_label = tk.Label(root, image=current_image)
image_label.pack()

# Run the tkinter event loop
root.mainloop()
