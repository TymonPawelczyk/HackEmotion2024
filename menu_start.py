import customtkinter as ctk
import customtkinter_main

root = ctk.CTk()
root.title("Menu Start")
root.geometry("400x200")

def confirm_selection():
    selected_option = option_menu.get()
    print(f'Buttno confirm clicked. You choose: {selected_option}')
    if selected_option == 'GameMode 1':
        print('gamemode1')
    elif selected_option == 'GameMode 2':
        print('gamemode2')


options = ["GameMode 1", "GameMode 2", "GameMode 3"]


label = ctk.CTkLabel(root, text="Choose an option:")
label.pack(pady=(20, 0))

selected_option = ctk.StringVar()
selected_option.set("")

option_menu = ctk.CTkOptionMenu(root, values=options, corner_radius=5, variable=selected_option)
option_menu.pack(pady=(0, 20))

confirm_button = ctk.CTkButton(root, text="Confirm", command=confirm_selection)
confirm_button.pack(pady=(0, 20))

root.mainloop()

