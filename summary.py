import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

set_appearance_mode = ("dark")

# Przykładowe dane
labels = ['Label1', 'Label2', 'Label3']
sizes = [30, 40, 30]
colors = ['#ef233c', '#27a300', 'blue']

# Tworzenie wykresu kołowego
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')

# Ustawienie koloru tła wykresu
fig.set_facecolor('#f4f0bb')

# Tworzenie okna CustomTkinter
summary = ctk.CTk()
summary.title("Summary")
summary.geometry("600x400")


# Dodawanie wykresu do okna CustomTkinter
canvas = FigureCanvasTkAgg(fig, master=summary)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Uruchamianie pętli głównej okna
summary.mainloop()
